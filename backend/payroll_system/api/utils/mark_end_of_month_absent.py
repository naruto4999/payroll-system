from ..models import WeeklyOffHolidayOff, EmployeeAttendance, LeaveGrade, EmployeeShifts
from dateutil.relativedelta import relativedelta
from .paid_days_count_for_past_six_days import paid_days_count_for_past_six_days
from django.db.models import Q
from .get_complete_working_days_queryset import get_complete_working_days_queryset
from datetime import date, datetime, timedelta
from .get_complete_working_days_queryset import get_complete_working_days_queryset
from .get_half_working_days_queryset import get_half_working_days_queryset


def mark_end_of_month_absent(from_date, to_date, employee, company_id, user, halves_to_convert, mark_full_working_day_to_half_working_day=False, half_to_mark_absent_in="first_half"):
    """
    Marks the entire day absent at the end of the month when there are no weekly off (WO) or holiday off (HD) references.
    This is for days that do not have a weekly off (WO) or holiday off (HD) at the end of the same month.
    """
    absent = LeaveGrade.objects.get(user=user, company_id=company_id, name='A')
    weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(company_id=company_id, user=user)

    filtered_wo_hd_records = EmployeeAttendance.objects.filter(
        employee=employee,
        company_id=company_id,
        user=user,
        date__gte=from_date,
        date__lte=to_date,
    ).filter(
        (Q(first_half__name='WO') & Q(second_half__name='WO')) |
        (Q(first_half__name='HD') & Q(second_half__name='HD')) |
        (Q(first_half__name='WO*') & Q(second_half__name='WO*')) |
        (Q(first_half__name='HD*') & Q(second_half__name='HD*'))
    ).order_by('-date')

    last_wo_hd = filtered_wo_hd_records.first()
    converted_halves = 0

    if halves_to_convert-converted_halves>=1 and mark_full_working_day_to_half_working_day == True:
        complete_working_days = get_complete_working_days_queryset(from_date=last_wo_hd.date + relativedelta(days=1), to_date=to_date, employee_id=employee.id, company_id=company_id, user=user)
        print(f"mark_end_of_month_queryset: {complete_working_days}")
        for mark_absent_day in complete_working_days:
            if halves_to_convert-converted_halves<1:
                break
            #Marking P day to A
            if (halves_to_convert-converted_halves)%2==1: #Marking Full Working Day to Half WOrking day
                print(f"marking half day absent")
                employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=employee, from_date__lte=mark_absent_day.date, to_date__gte=mark_absent_day.date)
                if not employee_shift_on_current_date.exists():
                    raise ValueError(f'Shift Not Found on {mark_absent_day.date.strftime("%Y-%m-%d")}')
                else:
                    employee_shift_on_current_date = employee_shift_on_current_date.first()
                shift = employee_shift_on_current_date.shift
                
                changed_time = False
                if half_to_mark_absent_in == "first_half":
                    if mark_absent_day.manual_in != None:
                        manual_in_old_datetime = datetime.combine(mark_absent_day.date, mark_absent_day.manual_in)
                        mark_absent_day.manual_in = (manual_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()
                        changed_time = True
                    elif mark_absent_day.machine_in != None:
                        machine_in_old_datetime = datetime.combine(mark_absent_day.date, mark_absent_day.machine_in)
                        mark_absent_day.machine_in = (machine_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()
                        changed_time = True
                    if changed_time==True:
                        mark_absent_day.first_half = absent
                        mark_absent_day.save()
                        converted_halves+=1
            else:
                mark_absent_day.first_half = absent
                mark_absent_day.second_half = absent
                mark_absent_day.manual_in = None
                mark_absent_day.manual_out = None
                mark_absent_day.machine_in = None
                mark_absent_day.machine_out = None
                mark_absent_day.save()
                converted_halves+=2

    if halves_to_convert-converted_halves==1:
        if mark_full_working_day_to_half_working_day == False:
            partial_working_days = get_half_working_days_queryset(from_date=last_wo_hd.date + relativedelta(days=1), to_date=to_date, employee_id=employee.id, company_id=company_id, user=user)
            for mark_absent_day in partial_working_days:
                if halves_to_convert-converted_halves<=0:
                    break
                mark_absent_day.first_half = absent
                mark_absent_day.second_half = absent
                mark_absent_day.manual_in = None
                mark_absent_day.manual_out = None
                mark_absent_day.machine_in = None
                mark_absent_day.machine_out = None
                mark_absent_day.save()
                converted_halves+=1
                break

    
    if converted_halves > halves_to_convert:
        raise ValueError("Converted More Halves than required")
    elif converted_halves > 0:
        return "marked", converted_halves
    else:
        return "not_marked", converted_halves
