from ..models import WeeklyOffHolidayOff, EmployeeAttendance, EmployeeShifts, LeaveGrade
from dateutil.relativedelta import relativedelta
from .paid_days_count_for_past_six_days import paid_days_count_for_past_six_days
from django.db.models import Q
from .get_half_working_days_queryset import get_half_working_days_queryset
from .get_complete_working_days_queryset import get_complete_working_days_queryset
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from datetime import date


def mark_half_day_absent_without_wo_hd_skipping(from_date, to_date, employee, company_id, user, mark_full_working_day_to_half_working_day=False, half_to_mark_absent_in="first_half"):
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
        if day.date == date(year=from_date.year, month=from_date.month, day=1):
            continue

        working_days_list = None
        if (day.first_half.name=='WO' and day.second_half.name=='WO') or (day.first_half.name=='HD' and day.second_half.name=='HD'):
            paid_days_count = paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)
            if paid_days_count>=((weekly_off_holiday_off.min_days_for_weekly_off * 2)+1) or paid_days_count>=((weekly_off_holiday_off.min_days_for_holiday_off * 2)+1): #paid days should be atleast P more
                #Ensure the Working Days being retrieved are in the same month
                from_date_for_working_days = day.date - relativedelta(days=6)
                to_date_for_working_days = day.date - relativedelta(days=1)
                if from_date_for_working_days.month != day.date.month:
                    from_date_for_working_days = day.date.replace(day=1)
                if to_date_for_working_days.month != day.date.month:
                    to_date_for_working_days = day.date.replace(day=1)

                if mark_full_working_day_to_half_working_day == False:
                    working_days_list = get_half_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                    if not working_days_list.exists():
                        continue
                    mark_absent_day = working_days_list.first()
                    mark_absent_day.first_half = absent
                    mark_absent_day.second_half = absent
                    mark_absent_day.manual_in = None
                    mark_absent_day.manual_out = None
                    mark_absent_day.machine_in = None
                    mark_absent_day.machine_out = None
                    mark_absent_day.save()
                    converted_halves+=1
                    break

                else:
                    working_days_list = get_complete_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                    if not working_days_list.exists():
                        continue
                    mark_absent_day = working_days_list.first()
                    employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=employee, from_date__lte=mark_absent_day.date, to_date__gte=mark_absent_day.date)
                    if not employee_shift_on_current_date.exists():
                        raise ValueError(f'Shift Not Found on {day.date.strftime("%Y-%m-%d")}')
                    else:
                        employee_shift_on_current_date = employee_shift_on_current_date.first()
                    shift = employee_shift_on_current_date.shift
                    
                    changed_time = False
                    if half_to_mark_absent_in=="first_half": #Code the Else block when needed
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
                            break

        elif (day.first_half.name=='WO*' and day.second_half.name=='WO*') or (day.first_half.name=='HD*' and day.second_half.name=='HD*'):
            #Ensure the Working Days being retrieved are in the same month
            from_date_for_working_days = day.date - relativedelta(days=6)
            to_date_for_working_days = day.date - relativedelta(days=1)
            if from_date_for_working_days.month != day.date.month:
                from_date_for_working_days = day.date.replace(day=1)
            if to_date_for_working_days.month != day.date.month:
                to_date_for_working_days = day.date.replace(day=1)

            if mark_full_working_day_to_half_working_day == False:
                working_days_list = get_half_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                if not working_days_list.exists():
                    continue
                mark_absent_day = working_days_list.first()
                mark_absent_day.first_half = absent
                mark_absent_day.second_half = absent
                mark_absent_day.manual_in = None
                mark_absent_day.manual_out = None
                mark_absent_day.machine_in = None
                mark_absent_day.machine_out = None
                mark_absent_day.save()
                converted_halves+=1
                break
            else:
                working_days_list = get_complete_working_days_queryset(from_date=from_date_for_working_days, to_date=to_date_for_working_days, employee_id=employee.id, company_id=company_id, user=user)
                if not working_days_list.exists():
                    continue
                mark_absent_day = working_days_list.first()
                employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=employee, from_date__lte=mark_absent_day.date, to_date__gte=mark_absent_day.date)
                if not employee_shift_on_current_date.exists():
                    return False, f'Shift Not Found on {att.date.strftime("%Y-%m-%d")}'
                else:
                    employee_shift_on_current_date = employee_shift_on_current_date.first()
                shift = employee_shift_on_current_date.shift
                
                changed_time = False
                if half_to_mark_absent_in=="first_half":
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
                        break

    if converted_halves >1:
        raise ValueError("Converted halves must be 1 or 0")
    elif converted_halves==1:
        return "marked", converted_halves
    else:
        return "not_marked", converted_halves



