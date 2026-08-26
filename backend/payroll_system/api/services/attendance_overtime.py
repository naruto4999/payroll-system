from collections.abc import Mapping
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from api.models import (
    EmployeeAttendance,
    EmployeeAttendanceOvertimeDetail,
    EmployeeProfessionalDetail,
    Holiday,
    OvertimePolicyDayRule,
)


_MISSING = object()
OVERTIME_DETAIL_CREATE_BATCH_SIZE = 500
OVERTIME_UPDATE_BATCH_SIZE = 500


def _attendance_key(attendance):
    return (attendance.id, attendance.date)


def _attendance_key_filter(keys):
    if not keys:
        return Q(id__in=[])
    query = Q()
    for attendance_id, attendance_date in keys:
        query |= Q(id=attendance_id, date=attendance_date)
    return query


def _entry_value(entry, name, default=None):
    if isinstance(entry, Mapping):
        return entry.get(name, default)
    return getattr(entry, name, default)


def _effective_source(*, entry, fallback):
    source = _entry_value(entry, 'source', _MISSING)
    if source is None:
        raise ValidationError({'source': 'Entry source cannot be None.'})
    if source is _MISSING:
        source = fallback
    if source not in dict(EmployeeAttendanceOvertimeDetail.SOURCE_CHOICES):
        raise ValidationError({'source': 'Invalid overtime detail source.'})
    return source


def _guard_unbackfilled_overtime(*, attendance, has_details):
    if attendance.ot_min and not has_details:
        raise ValidationError({
            'unbackfilled_overtime': 'Positive attendance overtime requires overtime detail rows.',
        })


def _owner_for_actor(actor):
    if actor is None or not getattr(actor, 'is_authenticated', False):
        raise ValidationError({'actor': 'An authenticated actor is required.'})
    if actor.role == 'OWNER':
        return actor
    if actor.role != 'REGULAR':
        raise ValidationError({'actor': 'Unsupported actor role.'})
    try:
        return actor.regular_to_owner.owner
    except ObjectDoesNotExist as exc:
        raise ValidationError({'actor': 'Regular account is not linked to an owner.'}) from exc


def _validate_master_scope(*, owner, company, employee):
    if company.user_id != owner.id or employee.user_id != owner.id or employee.company_id != company.id:
        raise ValidationError({'employee': 'Owner, company, and employee scope must agree.'})


def _validate_attendance_scope(*, attendance, actor):
    owner = _owner_for_actor(actor)
    if actor.role == 'REGULAR' and attendance.user_id != actor.id:
        raise ValidationError({'attendance': 'Regular accounts can only replace their own attendance overtime.'})
    _validate_master_scope(owner=owner, company=attendance.company, employee=attendance.employee)
    attendance_owner = attendance.user
    if attendance_owner.role == 'REGULAR':
        try:
            attendance_owner = attendance_owner.regular_to_owner.owner
        except ObjectDoesNotExist as exc:
            raise ValidationError({'attendance': 'Attendance account is not linked to an owner.'}) from exc
    if attendance_owner.id != owner.id:
        raise ValidationError({'attendance': 'Attendance does not belong to the actor scope.'})
    return owner


def classify_work_date(*, owner, company, employee, work_date, context=None):
    _validate_master_scope(owner=owner, company=company, employee=employee)
    key = (company.id, employee.id)
    if context is None:
        try:
            professional_detail = EmployeeProfessionalDetail.objects.get(
                user=owner,
                company=company,
                employee=employee,
            )
        except EmployeeProfessionalDetail.DoesNotExist as exc:
            raise ValidationError({'employee': 'Employee professional configuration is required.'}) from exc
        holiday = Holiday.objects.filter(user=owner, company=company, date=work_date).exists()
    else:
        professional_detail = context['professional_details'].get(key)
        if professional_detail is None:
            raise ValidationError({'employee': 'Employee professional configuration is required.'})
        holiday = (company.id, work_date) in context['holidays']

    if holiday:
        return OvertimePolicyDayRule.DAY_TYPE_HOLIDAY

    weekday = work_date.strftime('%a').lower()
    weekday_occurrence = f'{weekday}{(work_date.day - 1) // 7 + 1}'
    if professional_detail.weekly_off == weekday or professional_detail.extra_off == weekday_occurrence:
        return OvertimePolicyDayRule.DAY_TYPE_WEEKLY_OFF
    return OvertimePolicyDayRule.DAY_TYPE_REGULAR


def split_interval_at_payroll_midnights(*, start_datetime, end_datetime, payroll_timezone):
    if not isinstance(start_datetime, datetime) or not isinstance(end_datetime, datetime):
        raise ValidationError('Exact overtime start and end must be datetimes.')
    if timezone.is_naive(start_datetime) or timezone.is_naive(end_datetime):
        raise ValidationError('Exact overtime datetimes must be timezone-aware.')
    if end_datetime <= start_datetime:
        raise ValidationError({'end_datetime': 'End datetime must be after start datetime.'})
    try:
        payroll_tz = ZoneInfo(payroll_timezone)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValidationError({'payroll_timezone': 'A valid IANA payroll timezone is required.'}) from exc

    local_start = start_datetime.astimezone(payroll_tz)
    local_end = end_datetime.astimezone(payroll_tz)
    if (local_end - local_start).total_seconds() % 60:
        raise ValidationError('Exact overtime intervals must use whole-minute boundaries.')

    segments = []
    segment_start = local_start
    while segment_start < local_end:
        next_midnight = datetime.combine(
            segment_start.date() + timedelta(days=1),
            time.min,
            tzinfo=payroll_tz,
        )
        segment_end = min(local_end, next_midnight)
        gross_minutes = int((segment_end - segment_start).total_seconds() // 60)
        if gross_minutes <= 0:
            raise ValidationError('Exact overtime segments must have positive whole-minute durations.')
        segments.append({
            'start_datetime': segment_start,
            'end_datetime': segment_end,
            'work_date': segment_start.date(),
            'gross_minutes': gross_minutes,
        })
        segment_start = segment_end
    return segments


def _validate_exclusion_state(*, excluded_minutes, reason, note, allow_legacy=False):
    try:
        excluded_minutes = int(excluded_minutes)
    except (TypeError, ValueError) as exc:
        raise ValidationError({'excluded_minutes': 'Excluded minutes must be an integer.'}) from exc
    note = (note or '').strip()
    valid_reasons = dict(EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES)
    if reason not in valid_reasons:
        raise ValidationError({'exclusion_reason': 'Invalid exclusion reason.'})
    if reason == EmployeeAttendanceOvertimeDetail.EXCLUSION_LEGACY_UNSPECIFIED and not allow_legacy:
        raise ValidationError({'exclusion_reason': 'LEGACY_UNSPECIFIED is reserved for migrated data.'})
    if excluded_minutes == 0:
        if reason != EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE or note:
            raise ValidationError('Zero excluded minutes require NONE and an empty note.')
    else:
        if excluded_minutes < 0 or reason == EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE:
            raise ValidationError('Positive excluded minutes require a non-NONE reason.')
        if reason in (
            EmployeeAttendanceOvertimeDetail.EXCLUSION_MANUAL_ADJUSTMENT,
            EmployeeAttendanceOvertimeDetail.EXCLUSION_OTHER,
        ) and not note:
            raise ValidationError({'exclusion_note': 'This exclusion reason requires a note.'})
    if len(note) > 255:
        raise ValidationError({'exclusion_note': 'Ensure this value has at most 255 characters.'})
    return excluded_minutes, reason, note


def _normalize_timed_exclusions(*, exclusions, interval_start, interval_end, payroll_timezone):
    normalized = []
    for exclusion in exclusions:
        start = _entry_value(exclusion, 'start_datetime')
        end = _entry_value(exclusion, 'end_datetime')
        if not isinstance(start, datetime) or not isinstance(end, datetime) or timezone.is_naive(start) or timezone.is_naive(end):
            raise ValidationError({'exclusions': 'Timed exclusions require aware start and end datetimes.'})
        start = start.astimezone(payroll_timezone)
        end = end.astimezone(payroll_timezone)
        if start < interval_start or end > interval_end or end <= start:
            raise ValidationError({'exclusions': 'Timed exclusions must be contained within the overtime interval.'})
        seconds = (end - start).total_seconds()
        if seconds % 60:
            raise ValidationError({'exclusions': 'Timed exclusions must use whole-minute boundaries.'})
        minutes, reason, note = _validate_exclusion_state(
            excluded_minutes=int(seconds // 60),
            reason=_entry_value(exclusion, 'exclusion_reason'),
            note=_entry_value(exclusion, 'exclusion_note', ''),
        )
        normalized.append((start, end, minutes, reason, note))
    normalized.sort(key=lambda item: (item[0], item[1]))
    for previous, current in zip(normalized, normalized[1:]):
        if current[0] < previous[1]:
            raise ValidationError({'exclusions': 'Timed exclusions cannot overlap.'})
    return normalized


def _build_exact_details(*, attendance, owner, interval, source, payroll_timezone, classification_context=None):
    start = _entry_value(interval, 'start_datetime')
    end = _entry_value(interval, 'end_datetime')
    segments = split_interval_at_payroll_midnights(
        start_datetime=start,
        end_datetime=end,
        payroll_timezone=payroll_timezone.key,
    )
    exclusions = _entry_value(interval, 'exclusions', ()) or ()
    aggregate_excluded = _entry_value(interval, 'excluded_minutes', 0)
    aggregate_reason = _entry_value(
        interval,
        'exclusion_reason',
        EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE,
    )
    aggregate_note = _entry_value(interval, 'exclusion_note', '')

    timed_exclusions = []
    if exclusions:
        timed_exclusions = _normalize_timed_exclusions(
            exclusions=exclusions,
            interval_start=start.astimezone(payroll_timezone),
            interval_end=end.astimezone(payroll_timezone),
            payroll_timezone=payroll_timezone,
        )
        timed_total = sum(item[2] for item in timed_exclusions)
        if _entry_value(interval, 'excluded_minutes') is not None and int(aggregate_excluded) != timed_total:
            raise ValidationError({'excluded_minutes': 'Excluded minutes must equal timed exclusion duration.'})
    else:
        aggregate_excluded, aggregate_reason, aggregate_note = _validate_exclusion_state(
            excluded_minutes=aggregate_excluded,
            reason=aggregate_reason,
            note=aggregate_note,
        )
        if len(segments) > 1 and aggregate_excluded:
            raise ValidationError({'excluded_minutes': 'Cross-midnight exclusions require timed allocation data.'})

    details = []
    for segment in segments:
        excluded_minutes = 0
        reason = EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE
        note = ''
        if timed_exclusions:
            segment_metadata = set()
            for exclusion_start, exclusion_end, _, exclusion_reason, exclusion_note in timed_exclusions:
                overlap_start = max(segment['start_datetime'], exclusion_start)
                overlap_end = min(segment['end_datetime'], exclusion_end)
                if overlap_end > overlap_start:
                    excluded_minutes += int((overlap_end - overlap_start).total_seconds() // 60)
                    segment_metadata.add((exclusion_reason, exclusion_note))
            if len(segment_metadata) > 1:
                raise ValidationError({'exclusions': 'A segment cannot store multiple exclusion reasons or notes.'})
            if segment_metadata:
                reason, note = segment_metadata.pop()
        elif len(segments) == 1:
            excluded_minutes, reason, note = aggregate_excluded, aggregate_reason, aggregate_note

        if excluded_minutes >= segment['gross_minutes']:
            raise ValidationError({'excluded_minutes': 'Excluded minutes must leave positive eligible minutes.'})
        details.append(EmployeeAttendanceOvertimeDetail(
            attendance=attendance,
            work_date=segment['work_date'],
            day_type=classify_work_date(
                owner=owner,
                company=attendance.company,
            employee=attendance.employee,
            work_date=segment['work_date'],
            context=classification_context,
        ),
            source=source,
            start_datetime=segment['start_datetime'],
            end_datetime=segment['end_datetime'],
            gross_minutes=segment['gross_minutes'],
            excluded_minutes=excluded_minutes,
            eligible_minutes=segment['gross_minutes'] - excluded_minutes,
            exclusion_reason=reason,
            exclusion_note=note,
        ))
    return details


def _build_duration_detail(*, attendance, owner, entry, source, classification_context=None):
    work_date = _entry_value(entry, 'work_date')
    gross_minutes = _entry_value(entry, 'gross_minutes')
    try:
        gross_minutes = int(gross_minutes)
    except (TypeError, ValueError) as exc:
        raise ValidationError({'gross_minutes': 'Gross minutes must be an integer.'}) from exc
    excluded_minutes, reason, note = _validate_exclusion_state(
        excluded_minutes=_entry_value(entry, 'excluded_minutes', 0),
        reason=_entry_value(entry, 'exclusion_reason', EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE),
        note=_entry_value(entry, 'exclusion_note', ''),
    )
    if not work_date or gross_minutes <= 0 or excluded_minutes >= gross_minutes:
        raise ValidationError('Duration entries require a work date and positive eligible whole minutes.')
    return EmployeeAttendanceOvertimeDetail(
        attendance=attendance,
        work_date=work_date,
        day_type=classify_work_date(
            owner=owner,
            company=attendance.company,
            employee=attendance.employee,
            work_date=work_date,
            context=classification_context,
        ),
        source=source,
        gross_minutes=gross_minutes,
        excluded_minutes=excluded_minutes,
        eligible_minutes=gross_minutes - excluded_minutes,
        exclusion_reason=reason,
        exclusion_note=note,
    )


def _normalize_replacement(
    *, attendance, intervals, duration_entries, source, actor, classification_context=None,
):
    owner = _validate_attendance_scope(attendance=attendance, actor=actor)
    try:
        payroll_timezone = ZoneInfo(attendance.company.company_details.payroll_timezone)
    except (ObjectDoesNotExist, ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValidationError({'company': 'Company requires a valid payroll timezone.'}) from exc

    details = []
    for interval in intervals or ():
        details.extend(_build_exact_details(
            attendance=attendance,
            owner=owner,
            interval=interval,
            source=_effective_source(entry=interval, fallback=source),
            payroll_timezone=payroll_timezone,
            classification_context=classification_context,
        ))
    for entry in duration_entries or ():
        details.append(_build_duration_detail(
            attendance=attendance,
            owner=owner,
            entry=entry,
            source=_effective_source(entry=entry, fallback=source),
            classification_context=classification_context,
        ))

    exact_details = sorted(
        (detail for detail in details if detail.start_datetime is not None),
        key=lambda detail: (detail.start_datetime, detail.end_datetime),
    )
    for previous, current in zip(exact_details, exact_details[1:]):
        if current.start_datetime < previous.end_datetime:
            raise ValidationError('Exact overtime intervals cannot overlap or duplicate each other.')
    for detail in details:
        detail.clean_fields(exclude=['attendance'])
        if detail.eligible_minutes != detail.gross_minutes - detail.excluded_minutes:
            raise ValidationError({'eligible_minutes': 'Eligible minutes must equal gross minutes minus excluded minutes.'})
    return details


def _persist_replacement(*, attendance, details):
    EmployeeAttendanceOvertimeDetail.objects.filter(attendance=attendance).delete()
    created = EmployeeAttendanceOvertimeDetail.objects.bulk_create(details)
    total = sum(detail.eligible_minutes for detail in created)
    attendance.ot_min = total or None
    EmployeeAttendance.objects.filter(id=attendance.id, date=attendance.date).update(ot_min=attendance.ot_min)
    return created


def _persist_many_replacements(normalized):
    attendances = [attendance for attendance, _ in normalized]
    EmployeeAttendanceOvertimeDetail.objects.filter(
        attendance__in=attendances,
    ).delete()
    EmployeeAttendanceOvertimeDetail.objects.bulk_create(
        [
            detail
            for _, details in normalized
            for detail in details
        ],
        batch_size=OVERTIME_DETAIL_CREATE_BATCH_SIZE,
    )
    for attendance, details in normalized:
        total = sum(detail.eligible_minutes for detail in details)
        attendance.ot_min = total or None
    EmployeeAttendance.objects.bulk_update(
        attendances,
        ['ot_min'],
        batch_size=OVERTIME_UPDATE_BATCH_SIZE,
    )


def _build_bulk_classification_context(*, replacements, locked, actor):
    if not any(
        (_entry_value(replacement, 'intervals', ()) or ())
        or (_entry_value(replacement, 'duration_entries', ()) or ())
        for replacement in replacements
    ):
        return None

    owner = _owner_for_actor(actor)
    company_ids = set()
    employee_ids = set()
    work_dates = set()
    for replacement in replacements:
        attendance = locked[_attendance_key(_entry_value(replacement, 'attendance'))]
        company_ids.add(attendance.company_id)
        employee_ids.add(attendance.employee_id)
        for interval in _entry_value(replacement, 'intervals', ()) or ():
            start = _entry_value(interval, 'start_datetime')
            end = _entry_value(interval, 'end_datetime')
            if not isinstance(start, datetime) or not isinstance(end, datetime):
                continue
            first_date = min(start.date(), end.date()) - timedelta(days=1)
            last_date = max(start.date(), end.date()) + timedelta(days=1)
            work_dates.update(
                first_date + timedelta(days=offset)
                for offset in range((last_date - first_date).days + 1)
            )
        for entry in _entry_value(replacement, 'duration_entries', ()) or ():
            work_date = _entry_value(entry, 'work_date')
            if isinstance(work_date, datetime):
                work_date = work_date.date()
            if isinstance(work_date, date):
                work_dates.add(work_date)

    professional_details = {
        (detail.company_id, detail.employee_id): detail
        for detail in EmployeeProfessionalDetail.objects.filter(
            user=owner,
            company_id__in=company_ids,
            employee_id__in=employee_ids,
        )
    }
    holidays = set(
        Holiday.objects.filter(
            user=owner,
            company_id__in=company_ids,
            date__in=work_dates,
        ).values_list('company_id', 'date')
    )
    return {
        'professional_details': professional_details,
        'holidays': holidays,
    }


@transaction.atomic
def replace_attendance_overtime(*, attendance, intervals=(), duration_entries=(), source=None, actor):
    locked = EmployeeAttendance.objects.select_for_update().get(id=attendance.id, date=attendance.date)
    details = _normalize_replacement(
        attendance=locked,
        intervals=intervals,
        duration_entries=duration_entries,
        source=source,
        actor=actor,
    )
    return _persist_replacement(attendance=locked, details=details)


@transaction.atomic
def clear_attendance_overtime(*, attendance, actor):
    replace_attendance_overtime(
        attendance=attendance,
        intervals=(),
        duration_entries=(),
        source=EmployeeAttendanceOvertimeDetail.SOURCE_MANUAL,
        actor=actor,
    )


@transaction.atomic
def replace_many_attendance_overtime(*, replacements, actor):
    replacements = list(replacements)
    attendance_keys = [_attendance_key(_entry_value(item, 'attendance')) for item in replacements]
    if len(attendance_keys) != len(set(attendance_keys)):
        raise ValidationError({'replacements': 'Each attendance may appear only once.'})
    locked = {
        _attendance_key(attendance): attendance
        for attendance in EmployeeAttendance.objects.select_for_update(of=('self',))
        .select_related(
            'user',
            'user__regular_to_owner__owner',
            'company__company_details',
            'employee',
        )
        .filter(_attendance_key_filter(attendance_keys)).order_by('id', 'date')
    }
    if len(locked) != len(attendance_keys):
        raise ValidationError({'replacements': 'One or more attendance records do not exist.'})

    classification_context = _build_bulk_classification_context(
        replacements=replacements,
        locked=locked,
        actor=actor,
    )
    normalized = []
    for replacement in replacements:
        attendance = locked[_attendance_key(_entry_value(replacement, 'attendance'))]
        details = _normalize_replacement(
            attendance=attendance,
            intervals=_entry_value(replacement, 'intervals', ()),
            duration_entries=_entry_value(replacement, 'duration_entries', ()),
            source=_entry_value(replacement, 'source'),
            actor=actor,
            classification_context=classification_context,
        )
        normalized.append((attendance, details))
    _persist_many_replacements(normalized)


def _prepare_reclassification(*, attendance, actor):
    owner = _validate_attendance_scope(attendance=attendance, actor=actor)
    details = list(
        EmployeeAttendanceOvertimeDetail.objects.select_for_update()
        .filter(attendance=attendance).order_by('id', 'attendance_date')
    )
    _guard_unbackfilled_overtime(attendance=attendance, has_details=bool(details))
    changed = []
    for detail in details:
        day_type = classify_work_date(
            owner=owner,
            company=attendance.company,
            employee=attendance.employee,
            work_date=detail.work_date,
        )
        if detail.day_type != day_type:
            detail.day_type = day_type
            changed.append(detail)
    return details, changed


@transaction.atomic
def reclassify_attendance_overtime(*, attendance, actor):
    locked = EmployeeAttendance.objects.select_for_update().get(id=attendance.id, date=attendance.date)
    details, changed = _prepare_reclassification(attendance=locked, actor=actor)
    EmployeeAttendanceOvertimeDetail.objects.bulk_update(
        changed,
        ['day_type'],
        batch_size=OVERTIME_UPDATE_BATCH_SIZE,
    )
    return details


@transaction.atomic
def reclassify_many(*, attendances, actor):
    attendances = list(attendances)
    attendance_keys = [_attendance_key(attendance) for attendance in attendances]
    if len(attendance_keys) != len(set(attendance_keys)):
        raise ValidationError({'attendances': 'Each attendance may appear only once.'})
    locked = list(
        EmployeeAttendance.objects.select_for_update()
        .filter(_attendance_key_filter(attendance_keys)).order_by('id', 'date')
    )
    if len(locked) != len(attendance_keys):
        raise ValidationError({'attendances': 'One or more attendance records do not exist.'})

    prepared = [_prepare_reclassification(attendance=attendance, actor=actor) for attendance in locked]
    changed = [detail for _, attendance_changed in prepared for detail in attendance_changed]
    EmployeeAttendanceOvertimeDetail.objects.bulk_update(
        changed,
        ['day_type'],
        batch_size=OVERTIME_UPDATE_BATCH_SIZE,
    )
    return [detail for attendance_details, _ in prepared for detail in attendance_details]


@transaction.atomic
def sync_attendance_ot_min(*, attendance):
    locked = EmployeeAttendance.objects.select_for_update().get(id=attendance.id, date=attendance.date)
    total = locked.overtime_details.aggregate(total=Sum('eligible_minutes'))['total']
    _guard_unbackfilled_overtime(attendance=locked, has_details=total is not None)
    EmployeeAttendance.objects.filter(id=locked.id, date=locked.date).update(ot_min=total)
    attendance.ot_min = total
    return total
