from ..models import EmployeeAttendance, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, EmployeeMonthlyAttendanceDetails, EmployeeSalaryEarning, Calculations, EmployeeAttendance, EmployeeGenerativeLeaveRecord, EmployeeSalaryPrepared, WeeklyOffHolidayOff, LeaveGrade, EmployeeShifts
import calendar
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import random
from django.db.models import Q
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from ..utils.paid_days_count_for_past_six_days import paid_days_count_for_past_six_days
from ..utils.get_complete_working_days_queryset import get_complete_working_days_queryset 
from ..utils.mark_whole_day_absent_with_wo_hd_skipping import mark_whole_day_absent_with_wo_hd_skipping
from ..utils.mark_half_day_absent_with_wo_hd_skipping import mark_half_day_absent_with_wo_hd_skipping
from ..utils.mark_whole_day_absent_without_wo_hd_skipping import mark_whole_day_absent_without_wo_hd_skipping
from ..utils.mark_half_day_absent_without_wo_hd_skipping import mark_half_day_absent_without_wo_hd_skipping
from ..utils.calculate_each_head_earnings_from_paid_days import calculate_each_head_earnings_from_paid_days
from ..utils.mark_end_of_month_absent import mark_end_of_month_absent


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


def re_evaluate_weekly_holiday_off(from_date, to_date, employee, company_id, user):
    # attendance_records = EmployeeAttendance.objects.filter(employee=employee, company_id=company_id, user=user, date__gte=from_date, date__lte=to_date)
    weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(company_id=company_id, user=user)
    weekly_off = LeaveGrade.objects.get(user=user, company_id=company_id, name='WO')
    weekly_off_skip = LeaveGrade.objects.get(user=user, company_id=company_id, name='WO*')
    holiday_off = LeaveGrade.objects.get(user=user, company_id=company_id, name='HD')
    holiday_off_skip = LeaveGrade.objects.get(user=user, company_id=company_id, name='HD*')

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


def calculate_ot_attendance_using_total_earned(user, company_id, employee_ids, manually_inserted_total_earned, from_date, to_date, year, month, mark_attendance=True):
    """
    Function to calculate OT and attendance based on total earned. Deductions are subtracted from the manually_inserted_total_earned.
    Overtime is not marked on weekly off or holidy off days.
    Tweak the tweaking parameters later to modify the end result
   """
    #Tweaking parameters, Later get them from the frontend
    upper_buffer_manually_inserted_total_earned = 100 
    max_ot_in_a_single_working_day = 2

    # Mock logic
    EmployeeAttendance.objects.bulk_autofill(from_date=from_date, to_date=to_date, company_id=company_id, user=user, employee_ids=employee_ids)
    print(f"From Date: {from_date}")
    print(f"To Date: {to_date}")
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
            employee_monthly_attendance_detail = employee_monthly_attendance_detail.first()
            total_salary_rate = 0
            days_in_month = calendar.monthrange(year, month)[1]
            for salary_earning in employee_salary_earnings_for_each_head:
                total_salary_rate += salary_earning.value
            max_earned_possible_without_ot = total_salary_rate
            if employee_monthly_attendance_detail.not_paid_days_count != 0:
                earned_amount_dict = calculate_each_head_earnings_from_paid_days(month=month, year=year, employee=current_employee.employee, company_id=company_id, user=user, paid_days_count=(employee_monthly_attendance_detail.paid_days_count))
                projected_total_earned_amount = sum(entry['earned_amount'] for entry in earned_amount_dict.values())
                if projected_total_earned_amount < max_earned_possible_without_ot:
                    max_earned_possible_without_ot = projected_total_earned_amount

            if manually_inserted_total_earned > max_earned_possible_without_ot:
                print(f"yes amount is greater, marking OT")
                if employee_salary_detail.first().overtime_type != 'all_days':
                    return False, "Employee's overtime type is 'No Overtime'"
                amount_to_fill_with_ot = manually_inserted_total_earned - max_earned_possible_without_ot

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
                queryset_of_complete_working_days = get_complete_working_days_queryset(from_date=from_date, to_date=to_date, employee_id=current_employee.employee, company_id=company_id, user=user if user.role=='OWNER' else user.regular_to_owner.owner).order_by('?')
                if not queryset_of_complete_working_days.exists():
                    return False, "Employee has no complete Working Day"
                list_of_complete_working_days = list(queryset_of_complete_working_days)
                available_days = len(list_of_complete_working_days)


                list_of_ot_hrs_for_each_day = []
                total_ot_hrs_tmp = float(total_ot_hrs_to_fill)
                max_possible_ot = available_days * max_ot_in_a_single_working_day
                if total_ot_hrs_tmp > max_possible_ot:
                    return False, f"Not enough working days. Max possible OT: {max_possible_ot}hrs, Requested: {total_ot_hrs_tmp}hrs"

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
                    print(ot_hr)
                    if ot_hr==0.5:
                        """
                        Handling the case when the punch out time is 10-15 min beofore the shift end time due to buffer but 
                        adding ot to that results in no overtime in time updation so adding  to the shift end time instead.
                        """
                        employee_shift_on_current_date = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=current_employee.employee, from_date__lte=random_day_to_fill_ot.date, to_date__gte=random_day_to_fill_ot.date)
                        if not employee_shift_on_current_date.exists():
                            raise ValueError(f'Shift Not Found on {random_day_to_fill_ot.date.strftime("%Y-%m-%d")}')
                        else:
                            employee_shift_on_current_date = employee_shift_on_current_date.first()
                        shift = employee_shift_on_current_date.shift
                        shift_end_datetime = datetime.combine(random_day_to_fill_ot.date, shift.end_time)
                        random_day_to_fill_ot.manual_out = max(((existing_manual_out_datetime + timedelta(minutes=round(ot_hr*60)))), shift_end_datetime + timedelta(minutes=round(ot_hr*60))).time()
                        random_day_to_fill_ot.save()
                        continue
                    random_day_to_fill_ot.manual_out = (existing_manual_out_datetime + timedelta(hours=round(ot_hr))).time() if (ot_hr*60)%60==0 else (existing_manual_out_datetime + timedelta(minutes=round(ot_hr*60))).time()
                    random_day_to_fill_ot.save()

                #Updating monthly attendance record
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)
        
            elif manually_inserted_total_earned < max_earned_possible_without_ot: #Creating Less Salary then Salary Rate
                amount_to_deduct = total_salary_rate - manually_inserted_total_earned
                month_days = calendar.monthrange(year, month)[1]
                print(f"Amount To Deduct: {amount_to_deduct}, Month Days: {month_days}")
                #required_unpaid_halves = (amount_to_deduct * Decimal(month_days * 2) / total_salary_rate).quantize(Decimal('1.'), rounding=ROUND_CEILING)

                required_unpaid_halves = (amount_to_deduct * Decimal(month_days * 2) / total_salary_rate).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                if employee_monthly_attendance_detail.not_paid_days_count != 0:
                    required_unpaid_halves-=employee_monthly_attendance_detail.not_paid_days_count
                earned_amount_dict = calculate_each_head_earnings_from_paid_days(month=month, year=year, employee=current_employee.employee, company_id=company_id, user=user, paid_days_count=(employee_monthly_attendance_detail.paid_days_count)-required_unpaid_halves)
                projected_total_earned_amount = sum(entry['earned_amount'] for entry in earned_amount_dict.values())
                if projected_total_earned_amount > (manually_inserted_total_earned+upper_buffer_manually_inserted_total_earned):
                    required_unpaid_halves+=1

                print(f"Required Halves: {required_unpaid_halves}")
                
                #Add parameter for random absentes
                # Track converted halves
                converted_halves = 0
                print(required_unpaid_halves)
                loop_count = 0
                """
                Start New Method From Here
                """
                while required_unpaid_halves>converted_halves and loop_count<=200:
                    loop_count +=1
                    print(f"Loop Count: {loop_count}, required_unpaid_halves: {required_unpaid_halves}, Converted Halves: {converted_halves}")
                    status, marked_count = "not_marked", 0
                    if required_unpaid_halves-converted_halves>=4:
                        status, marked_count = mark_whole_day_absent_with_wo_hd_skipping(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user)
                        # print(f"Method mark_whole_day_absent_with_wo_hd_skipping returned: {status}, marked_count, {marked_count}")
                        if status=="marked":
                            converted_halves+=marked_count
                            continue
                    if required_unpaid_halves-converted_halves==3:
                        status, marked_count = mark_half_day_absent_with_wo_hd_skipping(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, mark_full_working_day_to_half_working_day=True)
                        # print(f"Method mark_half_day_absent_with_wo_hd_skipping returned: {status}, marked_count, {marked_count}")
                        if status=="marked":
                            converted_halves+=marked_count
                            continue
                    if required_unpaid_halves-converted_halves>=2:
                        status, marked_count = mark_whole_day_absent_without_wo_hd_skipping(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user)
                        # print(f"Method mark_whole_day_absent_without_wo_hd_skipping returned: {status}, marked_count, {marked_count}")
                        if status=="marked":
                            converted_halves+=marked_count
                            continue
                    if required_unpaid_halves-converted_halves==1:
                        status, marked_count = mark_half_day_absent_without_wo_hd_skipping(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, mark_full_working_day_to_half_working_day=True)
                        # print(f"Method mark_half_day_absent_without_wo_hd_skipping returned: {status}, marked_count, {marked_count}")

                        if status=="marked":
                            converted_halves+=marked_count
                            continue
                    if required_unpaid_halves-converted_halves!=0:
                        status, marked_count = mark_end_of_month_absent(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user, halves_to_convert=required_unpaid_halves-converted_halves, mark_full_working_day_to_half_working_day=True)
                        print(f"Method mark_end_of_month_absent returned: {status}, marked_count, {marked_count}, required haves passed: {required_unpaid_halves-converted_halves}")
                        if status=="marked":
                            converted_halves+=marked_count
                            continue
                    if (loop_count>200):
                        break

                converted_halves_in_reevaluation = re_evaluate_weekly_holiday_off(from_date=from_date, to_date=to_date, employee=current_employee.employee, company_id=company_id, user=user)
                if converted_halves_in_reevaluation>0:
                    return False, "Attendance Miss-Match on Weekly Off and Holiday Off"
                print(f"Final Converted halves: {converted_halves}")
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)

            print(f"Preparing Salary")

            EmployeeSalaryPrepared.objects.bulk_prepare_salaries(user=user, month=month, year=year, company_id=company_id, employee_ids=employee_ids)
            if manually_inserted_total_earned==total_salary_rate and employee_monthly_attendance_detail.not_paid_days_count!=0:
                return True, "Full salary marked using OT due attendance in previous month"

        return True, "Operation successful"

