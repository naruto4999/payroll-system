from ..models import WeeklyOffHolidayOff, EmployeeAttendance, LeaveGrade
from dateutil.relativedelta import relativedelta
from datetime import date
from .paid_days_count_for_past_six_days import paid_days_count_for_past_six_days
from django.db.models import Q
from .get_complete_working_days_queryset import get_complete_working_days_queryset


def mark_whole_day_absent_without_wo_hd_skipping(from_date, to_date, employee, company_id, user):
    """
    Marks the entire day absent without changing weekly off (WO) or holiday off (HD).
    Meaning either mark absent in the week where paid_days_count_for_past_six_days(WO or HD)>weekly_off_holiday_off.min_days_for_weekly_off * 2 or weekly_off_holiday_off.min_days_for_holiday_off * 2.
    Or mark absent in the week where it's already WO* or HD*.
    Should not mark absent in odd number of halves
    """
    absent= LeaveGrade.objects.get(user=user, company_id=company_id, name='A')
    weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(company_id=company_id, user=user)
    filtered_attendance_records = EmployeeAttendance.objects.filter(
        employee=employee,
        company_id=company_id,
        user=user,
        date__gte=from_date,
        date__lte=to_date,
    ).filter(
        (Q(first_half__name='WO') & Q(second_half__name='WO')) |
        (Q(first_half__name='WO*') & Q(second_half__name='WO*')) |
        (Q(first_half__name='HD') & Q(second_half__name='HD')) |
        (Q(first_half__name='HD*') & Q(second_half__name='HD*')) 
    ).order_by('?') 
    converted_halves = 0
    for day in filtered_attendance_records:
        complete_working_days_list = None
        if day.first_half.name=='WO' and day.second_half.name=='WO':
            if day.date == date(year=from_date.year, month=from_date.month, day=1):
                continue
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)>=((weekly_off_holiday_off.min_days_for_weekly_off * 2)+2): #paid days count should be at least a whole Working day (P-P) more
                #Ensure the Working Days being retrieved are in the same month
                from_date_for_working_days = day.date - relativedelta(days=6)
                to_date_for_working_days = day.date - relativedelta(days=1)
                if from_date_for_working_days.month != day.date.month:
                    from_date_for_working_days = day.date.replace(day=1)
                if to_date_for_working_days.month != day.date.month:
                    to_date_for_working_days = day.date.replace(day=1)

                complete_working_days_list = get_complete_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                if not complete_working_days_list.exists():
                    continue
                mark_absent_day = complete_working_days_list.first()
                mark_absent_day.first_half = absent
                mark_absent_day.second_half = absent
                mark_absent_day.manual_in = None
                mark_absent_day.manual_out = None
                mark_absent_day.machine_in = None
                mark_absent_day.machine_out = None
                mark_absent_day.save()
                converted_halves+=2
                break
        elif day.first_half.name=='HD' and day.second_half.name=='HD':
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)>=((weekly_off_holiday_off.min_days_for_holiday_off * 2)+2):
                #Ensure the Working Days being retrieved are in the same month
                from_date_for_working_days = day.date - relativedelta(days=6)
                to_date_for_working_days = day.date - relativedelta(days=1)
                if from_date_for_working_days.month != day.date.month:
                    from_date_for_working_days = day.date.replace(day=1)
                if to_date_for_working_days.month != day.date.month:
                    to_date_for_working_days = day.date.replace(day=1)
                
                complete_working_days_list = get_complete_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                if not complete_working_days_list.exists():
                    continue
                mark_absent_day = complete_working_days_list.first()
                mark_absent_day.first_half = absent
                mark_absent_day.second_half = absent
                mark_absent_day.manual_in = None
                mark_absent_day.manual_out = None
                mark_absent_day.machine_in = None
                mark_absent_day.machine_out = None
                mark_absent_day.save()
                converted_halves+=2
                break
        elif (day.first_half.name=='WO*' and day.second_half.name=='WO*') or (day.first_half.name=='HD*' and day.second_half.name=='HD*'):
            #Ensure the Working Days being retrieved are in the same month
            from_date_for_working_days = day.date - relativedelta(days=6)
            to_date_for_working_days = day.date - relativedelta(days=1)
            if from_date_for_working_days.month != day.date.month:
                from_date_for_working_days = day.date.replace(day=1)
            if to_date_for_working_days.month != day.date.month:
                to_date_for_working_days = day.date.replace(day=1)

            complete_working_days_list = get_complete_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
            if not complete_working_days_list.exists():
                continue
            mark_absent_day = complete_working_days_list.first()
            mark_absent_day.first_half = absent
            mark_absent_day.second_half = absent
            mark_absent_day.manual_in = None
            mark_absent_day.manual_out = None
            mark_absent_day.machine_in = None
            mark_absent_day.machine_out = None
            mark_absent_day.save()
            converted_halves+=2
            break
    if converted_halves % 2 != 0:
        raise ValueError("Converted halves must be even, but an odd number was encountered.")
    elif converted_halves>=2:
        return "marked", converted_halves
    else:
        return "not_marked", converted_halves


