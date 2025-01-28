from ..models import EmployeeAttendance, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, EmployeeMonthlyAttendanceDetails, EmployeeSalaryEarning, Calculations, EmployeeAttendance, EmployeeGenerativeLeaveRecord, EmployeeSalaryPrepared, WeeklyOffHolidayOff, LeaveGrade, EmployeeShifts
import calendar
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import random
from django.db.models import Q
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

def get_list_of_complete_working_days(from_date, to_date, employee_id, company_id, user):
    attendance_records = EmployeeAttendance.objects.filter(
        Q(first_half__name='P') & Q(second_half__name='P'),
        employee_id=employee_id,
        date__gte=from_date,
        date__lte=to_date,
        company_id=company_id,
        user=user
    )
    return attendance_records

def get_list_of_working_days_including_partial(from_date, to_date, employee_id, company_id, user):
    attendance_records = EmployeeAttendance.objects.filter(
        Q(first_half__name='P') | Q(second_half__name='P'),
        employee_id=employee_id,
        date__gte=from_date,
        date__lte=to_date,
        company_id=company_id,
        user=user
    )
    return attendance_records

# def get_paid_days_in_week(week_start, employee):
#     """Count paid days in a week"""
#     week_end = week_start + timedelta(days=6)
#     return EmployeeAttendance.objects.filter(
#         employee=employee,
#         date__gte=week_start,
#         date__lte=week_end,
#         pay_multiplier__gt=0
#     ).count()

def paid_days_count_for_past_six_days(attendance_date, company_id, user, employee): #multi the weeklyoffholidayoff rules by 2 to use this
    attendance_records = EmployeeAttendance.objects.filter(
        Q(first_half__paid=True) | Q(second_half__paid=True),
        employee=employee,
        date__range=[attendance_date - relativedelta(days=6), attendance_date - timedelta(days=1)],
        company_id=company_id,
        user=user
    )
    #Counting number of present/on duty
    paid_leave_count = 0
    if attendance_records.exists():
        for attendance in attendance_records:
            paid_leave_count += 1 if attendance.first_half.paid == True else 0
            paid_leave_count += 1 if attendance.second_half.paid == True else 0
    # print(paid_leave_count)
    return paid_leave_count

def re_evaluate_weekly_holiday_off(from_date, to_date, employee, company_id, user, weekly_off, holiday_off, weekly_off_skip, holiday_off_skip, weekly_off_holiday_off):
    # attendance_records = EmployeeAttendance.objects.filter(employee=employee, company_id=company_id, user=user, date__gte=from_date, date__lte=to_date)
    attendance_records = EmployeeAttendance.objects.filter(
        employee=employee,
        company_id=company_id,
        user=user,
        date__gte=from_date,
        date__lte=to_date,
    ).filter(
        Q(first_half=weekly_off) | Q(second_half=weekly_off) |
        Q(first_half=holiday_off) | Q(second_half=holiday_off)
    )
    converted_halves_weekly_holiday = 0
    for day in attendance_records:
        if day.first_half==weekly_off or day.second_half==weekly_off:
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)<(weekly_off_holiday_off.min_days_for_weekly_off * 2):
                both_halves_updated=False
                if day.first_half==weekly_off and day.second_half==weekly_off:
                    both_halves_updated=True
                day.first_half = weekly_off_skip
                day.second_half = weekly_off_skip
                day.save()
                converted_halves_weekly_holiday+= 2 if both_halves_updated==True else 1
        elif day.first_half==holiday_off or day.second_half==holiday_off:
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)<(weekly_off_holiday_off.min_days_for_holiday_off * 2):
                both_halves_updated=False
                if day.first_half==holiday_off and day.second_half==holiday_off:
                    both_halves_updated=True
                day.first_half = holiday_off_skip
                day.second_half = holiday_off_skip
                day.save()
                converted_halves_weekly_holiday+=2 if both_halves_updated==True else 1
    return converted_halves_weekly_holiday

def mark_absents_during_unpaid_weekly_holiday_off(from_date, to_date, employee, company_id, user, weekly_off, holiday_off, weekly_off_skip, holiday_off_skip, absent, converted_aim):
#use this if required_unpaid_halves-converted_halves == 2:
#basically mark absents in the week where weekly off or holiday off is already unpaid
    attendance_records = EmployeeAttendance.objects.filter(
        employee=employee,
        company_id=company_id,
        user=user,
        date__gte=from_date,
        date__lte=to_date,
    ).filter(
        Q(first_half=weekly_off_skip) & Q(second_half=weekly_off_skip) |
        Q(first_half=holiday_off_skip) & Q(second_half=holiday_off_skip)
    )

    converted_halves_weekly_holiday = 0
    for day in attendance_records:
        if day.first_half==weekly_off_skip and day.second_half==weekly_off_skip:
            attendance_date_for_weekly_off_skip = day.date
            for countdown in range(1,7):
                query_date = attendance_date_for_weekly_off_skip - timedelta(days=countdown)
                weekday = EmployeeAttendance.objects.get(user=user, employee=employee, date=query_date, company_id=company_id)
                if weekday.date.month == day.date.month and weekday.date.year == day.date.year and weekday.first_half != weekly_off_skip and weekday.first_half != holiday_off_skip and weekday.first_half !=weekly_off and weekday.first_half != holiday_off and weekday.second_half != weekly_off_skip and weekday.second_half != holiday_off_skip and weekday.second_half != weekly_off and weekday.second_half != holiday_off and weekday.first_half != absent and weekday.second_half != absent:
                    if weekday.first_half==absent or weekday.second_half==absent:
                        continue #Employee is already absent in half of the attendance
                    weekday.first_half = absent
                    weekday.second_half = absent
                    weekday.machine_in = None
                    weekday.machine_out = None
                    weekday.manual_in = None
                    weekday.manual_out = None
                    weekday.save()
                    converted_halves_weekly_holiday += 2
                    if(converted_aim==converted_halves_weekly_holiday):
                        break
        if converted_aim==converted_halves_weekly_holiday:
            break

    
    return converted_halves_weekly_holiday

def mark_absent_which_causes_weekly_off_skip_or_holiday_off_skip(from_date, to_date, employee, company_id, user, weekly_off, holiday_off, weekly_off_skip, holiday_off_skip, weekly_off_holiday_off, absent, aim):#aim should be multiple of 4
    # attendance_records = EmployeeAttendance.objects.filter(employee=employee, company_id=company_id, user=user, date__gte=from_date, date__lte=to_date)
    attendance_records = EmployeeAttendance.objects.filter(
        employee=employee,
        company_id=company_id,
        user=user,
        date__gte=from_date,
        date__lte=to_date,
    ).filter(
        Q(first_half=weekly_off) & Q(second_half=weekly_off) |
        Q(first_half=holiday_off) & Q(second_half=holiday_off)
    )
    converted_halves_to_cause_wo_skip_hd_skip = 0
    for day in attendance_records:
        if day.first_half==weekly_off and day.second_half==weekly_off:
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)==(weekly_off_holiday_off.min_days_for_weekly_off * 2):
                attendance_records_to_mark_absent = EmployeeAttendance.objects.filter(
                    Q(first_half__paid=True) & Q(second_half__paid=True),
                    employee=employee,
                    date__range=[day.date - relativedelta(days=6), day.date - timedelta(days=1)],
                    company_id=company_id,
                    user=user
                )
                if not attendance_records_to_mark_absent.exists():
                    continue
                attendance_records_to_mark_absent = attendance_records_to_mark_absent.first()
                attendance_records_to_mark_absent.first_half = absent
                attendance_records_to_mark_absent.second_half = absent
                attendance_records_to_mark_absent.manual_in = None
                attendance_records_to_mark_absent.manual_out = None
                attendance_records_to_mark_absent.machine_in = None
                attendance_records_to_mark_absent.machine_out = None
                attendance_records_to_mark_absent.save()

                day.first_half = weekly_off_skip
                day.second_half = weekly_off_skip
                day.save()
                converted_halves_to_cause_wo_skip_hd_skip+=4         
        elif day.first_half==holiday_off and day.second_half==holiday_off:
            if paid_days_count_for_past_six_days(day.date, company_id=company_id, user=user, employee=employee)==(weekly_off_holiday_off.min_days_for_holiday_off * 2):
                attendance_records_to_mark_absent = EmployeeAttendance.objects.filter(
                    Q(first_half__paid=True) & Q(second_half__paid=True),
                    employee=employee,
                    date__range=[day.date - relativedelta(days=6), day.date - timedelta(days=1)],
                    company_id=company_id,
                    user=user
                )
                if not attendance_records_to_mark_absent.exists():
                    continue
                attendance_records_to_mark_absent = attendance_records_to_mark_absent.first()
                attendance_records_to_mark_absent.first_half = absent
                attendance_records_to_mark_absent.second_half = absent
                attendance_records_to_mark_absent.manual_in = None
                attendance_records_to_mark_absent.manual_out = None
                attendance_records_to_mark_absent.machine_in = None
                attendance_records_to_mark_absent.machine_out = None
                attendance_records_to_mark_absent.save()

                day.first_half = holiday_off_skip
                day.second_half = holiday_off_skip
                day.save()
                converted_halves_to_cause_wo_skip_hd_skip+=4
        if aim==converted_halves_to_cause_wo_skip_hd_skip:
                break
    return converted_halves_to_cause_wo_skip_hd_skip







def calculate_ot_attendance_using_total_earned(user, company_id, employee_ids, manually_inserted_total_earned, from_date, to_date, year, month, mark_attendance=True):
    """
    Mock function to calculate OT attendance based on total earned.

    Args:
        employee_id (int): The ID of the employee.
        total_earned (float): Total earned amount for the employee.

    Returns:
        dict: A mock result with employee ID, total earned, and OT attendance hours.
    """
    # Mock logic
    EmployeeAttendance.objects.bulk_autofill(from_date=from_date, to_date=to_date, company_id=company_id, user=user, employee_ids=employee_ids)
    employees = EmployeeProfessionalDetail.objects.filter(employee__id__in=employee_ids, company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner)
    print(f"Employee Ids: {employee_ids}, Manually Inserted Amount: {manually_inserted_total_earned}")
    if employees.exists():
        for current_employee in employees: 
            employee_pf_esi_detail = EmployeePfEsiDetail.objects.filter(company_id=company_id, employee=current_employee.employee)
            employee_salary_detail = EmployeeSalaryDetail.objects.filter(company_id=company_id, employee=current_employee.employee)
            employee_monthly_attendance_detail = EmployeeMonthlyAttendanceDetails.objects.filter(user=user, company_id=company_id, employee=current_employee.employee, date=from_date)
            employee_salary_earnings_for_each_head = EmployeeSalaryEarning.objects.filter(company_id=company_id, from_date__lte=from_date, to_date__gte=from_date, employee=current_employee.employee)
            company_calculations = Calculations.objects.get(user=user if user.role=="OWNER" else user.regular_to_owner.owner, company_id=company_id)

            if not employee_pf_esi_detail.exists() or not employee_salary_detail.exists() or not employee_monthly_attendance_detail.exists() or not employee_salary_earnings_for_each_head.exists():
                #Return error that details are not filled for this employee
                return False, "Empoyee Details are not complete"
                continue
            elif employee_salary_detail.first().overtime_type != 'all_days':
                if employee_salary_detail.first().overtime_type == 'no_overtime':
                    return False, "Employee's Overtime Type is 'No Overtime'"
                else:
                    return False, "Employee's Overtime Type is Weekly/Holiday Off"
            total_salary_rate = 0
            days_in_month = calendar.monthrange(year, month)[1]
            for salary_earning in employee_salary_earnings_for_each_head:
                total_salary_rate += salary_earning.value
            max_ot_in_a_single_working_day = 6 #ask this limit because there has to be an upper limit above which this employee can't earn with their current rate
            if manually_inserted_total_earned > total_salary_rate:
                print(f"yes amount is greater, marking OT")
                if employee_salary_detail.first().overtime_type != 'all_days':
                    return False, "Employee's overtime type is 'No Overtime'"
                amount_to_fill_with_ot = manually_inserted_total_earned - total_salary_rate

                overtime_rate_multiplier = 2 if employee_salary_detail.first().overtime_rate == 'D' or user.role=='REGULAR' else 1
                overtime_divisor = Decimal(26)
                if user.role=='OWNER':
                    if company_calculations.ot_calculation == 'month_days':
                        overtime_divisor = Decimal(days_in_month)
                    else:
                        overtime_divisor = Decimal(company_calculations.ot_calculation)
                ot_rate_per_hour = Decimal(total_salary_rate) * Decimal(overtime_rate_multiplier) / overtime_divisor / Decimal(8)
                total_ot_hrs_to_fill = amount_to_fill_with_ot/ot_rate_per_hour
                
                # Extract the integer and decimal parts
                integer_part = int(total_ot_hrs_to_fill)
                decimal_part = total_ot_hrs_to_fill - integer_part

                if decimal_part >= Decimal('0.5'):
                    total_ot_hrs_to_fill = integer_part + Decimal('0.5')
                else:
                    total_ot_hrs_to_fill = Decimal(integer_part)

                #List of Complete Working Days
                queryset_of_complete_working_days = get_list_of_complete_working_days(from_date=from_date, to_date=to_date, employee_id=current_employee.employee, company_id=company_id, user=user if user.role=='OWNER' else user.regular_to_owner.owner).order_by('?')
                if not queryset_of_complete_working_days.exists():
                    return False, "Employee has no complete Working Day"
                list_of_complete_working_days = list(queryset_of_complete_working_days)
                available_days = len(list_of_complete_working_days)


                list_of_ot_hrs_for_each_day = []
                total_ot_hrs_tmp = float(total_ot_hrs_to_fill)
                max_possible_ot = available_days * max_ot_in_a_single_working_day
                if total_ot_hrs_tmp > max_possible_ot:
                    return False, f"Not enough working days. Max possible OT: {max_possible_ot}hrs, Requested: {total_ot_hrs_tmp}hrs"


                # while total_ot_hrs_tmp>0 and len(list_of_ot_hrs_for_each_day)<available_days:
                #     random_ot_hrs = random.randint(1, max_ot_in_a_single_working_day)
                #     hrs_to_append = min(random_ot_hrs, total_ot_hrs_tmp)
                #     list_of_ot_hrs_for_each_day.append(hrs_to_append)
                #     total_ot_hrs_tmp -= hrs_to_append
                remaining_hours = total_ot_hrs_tmp

                while remaining_hours > 0 and len(list_of_ot_hrs_for_each_day) < available_days:
                    days_left = available_days - len(list_of_ot_hrs_for_each_day)
                    
                    # Calculate dynamic range for valid hours
                    max_hours = min(float(max_ot_in_a_single_working_day), remaining_hours)
                    min_hours = max(0.5, remaining_hours - (days_left - 1) * max_ot_in_a_single_working_day)
                    
                    # Generate random hours within valid range
                    random_hrs = random.uniform(min_hours, max_hours)
                    
                    # Round to nearest 0.5 without changing total
                    random_hrs = round(random_hrs * 2) / 2
                    
                    # Final clamp to prevent overshooting
                    random_hrs = min(random_hrs, remaining_hours)
                    random_hrs = max(random_hrs, 0.5)
                    
                    list_of_ot_hrs_for_each_day.append(random_hrs)
                    remaining_hours -= random_hrs
                    remaining_hours = round(remaining_hours * 2) / 2  # Maintain 0.5 precision

                # Verify exact allocation
                if abs(remaining_hours) > 0.01:  # Allow floating point tolerance
                    return False, f"OT allocation failed. Remaining hours: {remaining_hours:.1f}"

                # Convert back to Decimal for database operations
                list_of_ot_hrs_for_each_day = [Decimal(str(h)) for h in list_of_ot_hrs_for_each_day]
                
                print(queryset_of_complete_working_days)
                print(f"Lenght of queryset: {len(queryset_of_complete_working_days)}")
                for record in queryset_of_complete_working_days:
                    print(record.date)
                for ot_hr in list_of_ot_hrs_for_each_day:
                    random_day_to_fill_ot = list_of_complete_working_days.pop()
                    random_day_to_fill_ot.ot_min = ot_hr*60
                    existing_manual_out_datetime = datetime.combine(random_day_to_fill_ot.date, random_day_to_fill_ot.manual_out) #This does not take into account if the employee is leave the next day
                    random_day_to_fill_ot.manual_out = (existing_manual_out_datetime + timedelta(hours=round(ot_hr))).time() if (ot_hr*60)%60==0 else  (existing_manual_out_datetime + timedelta(minutes=round(ot_hr*60))).time()
                    random_day_to_fill_ot.save()

                #Updating monthly attendance record
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)
        
            else:
                amount_to_deduct = total_salary_rate - manually_inserted_total_earned
                month_days = calendar.monthrange(year, month)[1]
                required_unpaid_halves = (amount_to_deduct * Decimal(month_days * 2) / total_salary_rate).quantize(Decimal('1.'), rounding=ROUND_CEILING)
                print(f"Required Halves: {required_unpaid_halves}")
                
                #Already randomly arranged
                queryset_of_working_days_including_partial = get_list_of_working_days_including_partial(from_date=from_date, to_date=to_date, employee_id=current_employee.employee, company_id=company_id, user=user if user.role=='OWNER' else user.regular_to_owner.owner).order_by('?')
                
                # Get company's weekly/holiday off rules
                weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(company_id=company_id, user=user)

                # Get leave grade instances
                weekly_off = LeaveGrade.objects.get(user=user, company_id=company_id, name='WO')
                weekly_off_skip = LeaveGrade.objects.get(user=user, company_id=company_id, name='WO*')
                holiday_off = LeaveGrade.objects.get(user=user, company_id=company_id, name='HD')
                holiday_off_skip = LeaveGrade.objects.get(user=user, company_id=company_id, name='HD*')
                absent= LeaveGrade.objects.get(user=user, company_id=company_id, name='A')

                # Track converted halves
                converted_halves = 0
                
                # while required_unpaid_halves>converted_halves:
                for att in queryset_of_working_days_including_partial:
                    if required_unpaid_halves<=converted_halves:
                        break

                    if required_unpaid_halves-converted_halves<=10:
                        print(f"Top weekly reevaluation")
                        converted_halves_in_reevaluation = 0
                        converted_halves_in_reevaluation = re_evaluate_weekly_holiday_off(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, weekly_off_holiday_off=weekly_off_holiday_off)
                        converted_halves += converted_halves_in_reevaluation
                    week_start = att.date - timedelta(days=att.date.weekday())

                    if (required_unpaid_halves-converted_halves)%2==1: #or (required_unpaid_halves-converted_halves)%2>0:
                        print(f"Marking Half day absent")
                        employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=current_employee.employee, from_date__lte=att.date, to_date__gte=att.date)
                        if not employee_shift_on_current_date.exists():
                            return False, f'Shift Not Found on {att.date.strftime("%Y-%m-%d")}'
                        else:
                            employee_shift_on_current_date = employee_shift_on_current_date.first()
                        shift = employee_shift_on_current_date.shift
                        if att.machine_in != None:
                            machine_in_old_datetime = datetime.combine(att.date, att.machine_in)
                            att.machine_in = (machine_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()
                        else:
                            manual_in_old_datetime = datetime.combine(att.date, att.manual_in)
                            att.manual_in = (manual_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()

                        att.first_half = absent
                        att.save()
                        converted_halves+=1
                        continue
                    if required_unpaid_halves>4 and ((required_unpaid_halves-converted_halves)==2 or (required_unpaid_halves-converted_halves)==4 or (required_unpaid_halves-converted_halves)==3) :
                        print(f"Marking absents within WO skip and HD skip week")
                        converted_halves_weekly_holiday_skip = mark_absents_during_unpaid_weekly_holiday_off(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, absent=absent, converted_aim=2)
                        converted_halves += converted_halves_weekly_holiday_skip
                    if required_unpaid_halves-converted_halves>4:
                        print(f"Marking Absent")
                        att.first_half = absent
                        att.second_half = absent
                        att.manual_in = None
                        att.manual_out = None
                        att.machine_in = None
                        att.machine_out = None
                        att.save()
                        converted_halves+=2
                        print(f"Converted Halves after marking absent: {converted_halves}")
                    # if required_unpaid_halves-converted_halves==4:
                    #     print(f"Making a WO Skip by marking one absent")
                    #     converted_halves_to_cause_wo_skip_hd_skip = mark_absent_which_causes_weekly_off_skip_or_holiday_off_skip(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, weekly_off_holiday_off=weekly_off_holiday_off, absent=absent, aim=4)
                    #     converted_halves += converted_halves_to_cause_wo_skip_hd_skip

                    # elif required_unpaid_halves-converted_halves==1:
                    #     employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=current_employee.employee, from_date__lte=att.date, to_date__gte=att.date)
                    #     if not employee_shift_on_current_date.exists():
                    #         return False, f'Shift Not Found on {att.date.strftime("%Y-%m-%d")}'
                    #     else:
                    #         employee_shift_on_current_date = employee_shift_on_current_date.first()
                    #     shift = employee_shift_on_current_date.shift
                    #     if att.machine_in != None:
                    #         machine_in_old_datetime = datetime.combine(att.date, att.machine_in)
                    #         att.machine_in = (machine_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()
                    #     else:
                    #         manual_in_old_datetime = datetime.combine(att.date, att.manual_in)
                    #         att.manual_in = (manual_in_old_datetime + timedelta(minutes=shift.max_late_allowed_min + 20)).time()
                    #
                    #     att.first_half = absent
                    #     att.save()
                    #     converted_halves+=1
                    if required_unpaid_halves-converted_halves<=10:
                        #Re evaluating WeeklyOffHolidayOff for safety
                        converted_halves_in_reevaluation = 0
                        converted_halves_in_reevaluation = re_evaluate_weekly_holiday_off(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, weekly_off_holiday_off=weekly_off_holiday_off)
                        converted_halves += converted_halves_in_reevaluation
                    if required_unpaid_halves-converted_halves==4:
                        print(f"Making a WO Skip by marking one absent")
                        converted_halves_to_cause_wo_skip_hd_skip = mark_absent_which_causes_weekly_off_skip_or_holiday_off_skip(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, weekly_off_holiday_off=weekly_off_holiday_off, absent=absent, aim=4)
                        converted_halves += converted_halves_to_cause_wo_skip_hd_skip


                    print(f"End Date: {att.date}, Converted Halves: {converted_halves}")


                converted_halves_in_reevaluation = re_evaluate_weekly_holiday_off(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, weekly_off=weekly_off, holiday_off=holiday_off, weekly_off_skip=weekly_off_skip, holiday_off_skip=holiday_off_skip, weekly_off_holiday_off=weekly_off_holiday_off)
                if converted_halves_in_reevaluation>0:
                    return False, "Attendance Miss-Match on Weekly Off and Holiday Off"
                print(f"Final Converted halves: {converted_halves}")
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)


            EmployeeSalaryPrepared.objects.bulk_prepare_salaries(user=user, month=month, year=year, company_id=company_id, employee_ids=employee_ids)

        return True, "Operation successful"

