from django.db import models
# from api.models import EmployeePersonalDetail, EmployeeProfessionalDetail
from django.db.models import Q
from django.apps import apps
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import random
import time
import calendar
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING





class ActiveEmployeeManager(models.Manager):
    def active_employees_between_dates(self, from_date, to_date, company_id, user):
        return self.filter(
            Q(resigned=False) | Q(resignation_date__gte=from_date),
            date_of_joining__lte=to_date,
            company_id=company_id,
            user=user
        )

class EmployeeAttendanceManager(models.Manager):

    def generate_random_time(self, reference_time, start_buffer, end_buffer):
        reference_datetime = datetime.combine(datetime.today(), reference_time)
        reference_datetime -= relativedelta(minutes=start_buffer)
        random_time_difference = timedelta(minutes=random.randint(0, start_buffer+end_buffer))
        random_time = (reference_datetime+random_time_difference).time()
        return random_time.replace(second=0)

    def weekday_occurrence_in_month(self, date):
        weekday = date.strftime('%a').lower()
        ordinal_number = (date.day - 1) // 7 + 1
        return f"{weekday}{ordinal_number}"
    
    def paid_days_count_for_past_six_days(self, attendance_date, company_id, user, employee):
        attendance_records = self.filter(
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
    
    # def get_employee_shift_on_date(self, user, company_id, employee, date_to_find):
    #     EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
    #     employee_shift_on_particular_date = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date).first()

        

    def bulk_autofill(self, from_date, to_date, company_id, user):
        AUTO_SHIFT_BEGINNING_BUFFER_BEFORE = 10
        AUTO_SHIFT_ENDING_BUFFER_BEFORE = 10
        AUTO_SHIFT_ENDING_BUFFER_AFTER = 10

        WeeklyOffHolidayOff = apps.get_model('api', 'WeeklyOffHolidayOff')
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        EmployeeSalaryDetail = apps.get_model('api', 'EmployeeSalaryDetail')
        EmployeeGenerativeLeaveRecord = apps.get_model('api', 'EmployeeGenerativeLeaveRecord')
        EmployeeMonthlyAttendanceDetails = apps.get_model('api', 'EmployeeMonthlyAttendanceDetails')
        LeaveGrade = apps.get_model('api', 'LeaveGrade')
        Holiday = apps.get_model('api', 'Holiday')
        EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
        holiday_queryset = Holiday.objects.filter(user=user, company_id=company_id)
        print(f'From Date: {from_date} To Date: {to_date}')
        weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(user=user, company_id=company_id)
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date, to_date, company_id=company_id, user=user)

        #Leaves
        present_leave = LeaveGrade.objects.get(company_id=company_id, user=user, name='P')
        weekly_off = LeaveGrade.objects.get(company_id=company_id, user=user, name='WO')
        weekly_off_skip = LeaveGrade.objects.get(company_id=company_id, user=user, name='WO*')
        holiday_off = LeaveGrade.objects.get(company_id=company_id, user=user, name='HD')
        holiday_off_skip = LeaveGrade.objects.get(company_id=company_id, user=user, name='HD*')


        # Calculate the range of dates
        if active_employees.exists():
            for current_employee in active_employees:
                employee_salary_detail = EmployeeSalaryDetail.objects.filter(company_id=company_id, employee=current_employee.employee)
                if not employee_salary_detail.exists():
                    continue
                # print(self.paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=from_date, employee=current_employee.employee))
                # start_time_before_while = time.time()

                montly_attendance_record_to_delete = EmployeeMonthlyAttendanceDetails.objects.filter(
                        employee=current_employee.employee,
                        date=from_date.replace(day=1),
                        company_id=company_id,
                    )
                if montly_attendance_record_to_delete.exists():
                        # print(f"Deleting attendance for {current_employee.employee}'s on {current_date}")
                        montly_attendance_record_to_delete.delete()
                generative_leave_record_to_delete = EmployeeGenerativeLeaveRecord.objects.filter(
                        employee=current_employee.employee,
                        date=from_date.replace(day=1),
                        company_id=company_id,
                    )
                if generative_leave_record_to_delete.exists():
                        # print(f"Deleting attendance for {current_employee.employee}'s on {current_date}")
                        generative_leave_record_to_delete.delete()
                current_date = from_date
                # end_time_before_while = time.time()

                # start_time_while = time.time()

                #Deleting the existing attendances between the from_date and to_date inclusive
                attendance_to_delete = self.filter(
                    Q(employee=current_employee.employee) &
                    Q(date__range=(from_date, to_date)) &
                    Q(company_id=company_id)
                )
                attendance_to_delete.delete()

                #Optimizing shifts retrieval
                shift_found = False
                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=from_date, to_date__gte=from_date)
                if employee_shift_on_particular_date_queryset.exists():
                    employee_shift_on_particular_date = employee_shift_on_particular_date_queryset.first()
                    shift_from_date = employee_shift_on_particular_date.from_date
                    shift_to_date = employee_shift_on_particular_date.to_date
                    found_shift_beginning_time = employee_shift_on_particular_date.shift.beginning_time
                    found_shift_end_time = employee_shift_on_particular_date.shift.end_time
                    found_shift_late_grace = employee_shift_on_particular_date.shift.late_grace
                    shift_found = True

                attendance_records = []
                total_expected_instances = 0
                while current_date <= to_date:
                    
                    if current_date >= current_employee.date_of_joining and (current_employee.resigned == False or current_date<=current_employee.resignation_date):
                        if current_date.strftime('%a').lower() == current_employee.weekly_off or (self.weekday_occurrence_in_month(date=current_date) == current_employee.extra_off):
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            weekly_off_to_give = weekly_off_skip
                            if self.paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                weekly_off_to_give = weekly_off
                            attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, employee=current_employee.employee, first_half=weekly_off_to_give, second_half=weekly_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0))
                            total_expected_instances +=1

                        #If Current date is a holdiday
                        elif holiday_queryset.filter(date=current_date).exists():
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            holiday_off_to_give = holiday_off_skip
                            if self.paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                holiday_off_to_give = holiday_off
                            attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, employee=current_employee.employee, first_half=holiday_off_to_give, second_half=holiday_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0))
                            total_expected_instances +=1

                        #It's not weekly off nor holiday off
                        else:
                            if not shift_found or (current_date < shift_from_date and current_date > shift_to_date):
                                print('Yes Refetching')
                                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date)
                                if employee_shift_on_particular_date_queryset.exists():
                                    employee_shift_on_particular_date = employee_shift_on_particular_date_queryset.first()
                                    shift_from_date = employee_shift_on_particular_date.from_date
                                    shift_to_date = employee_shift_on_particular_date.to_date
                                    found_shift_beginning_time = employee_shift_on_particular_date.shift.beginning_time
                                    found_shift_end_time = employee_shift_on_particular_date.shift.end_time
                                    found_shift_late_grace = employee_shift_on_particular_date.shift.late_grace
                                    shift_found = True

                            # employee_shift_on_particular_date = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date).first()
                            attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, employee=current_employee.employee, first_half=present_leave, second_half=present_leave, manual_in=self.generate_random_time(reference_time=found_shift_beginning_time, start_buffer=AUTO_SHIFT_BEGINNING_BUFFER_BEFORE, end_buffer=found_shift_late_grace), manual_out=self.generate_random_time(reference_time=found_shift_end_time, start_buffer=AUTO_SHIFT_ENDING_BUFFER_BEFORE, end_buffer=AUTO_SHIFT_ENDING_BUFFER_AFTER), machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0))
                            total_expected_instances +=1
                    current_date += relativedelta(days=1)
                
                EmployeeAttendance.objects.bulk_create(attendance_records)
                # end_time_while = time.time()
                # print(f"Time taken by the while loop: {end_time_while - start_time_while} seconds")
                # print(f"Time taken before while loop: {end_time_before_while - start_time_before_while} seconds")


                # start_time = time.time()
                EmployeeGenerativeLeaveRecord.objects.generate_monthly_record(total_expected_instances=total_expected_instances, user=user, year=from_date.year, month=from_date.month, employee=current_employee.employee, company=current_employee.company)
                # end_time = time.time()
                # print(f"Time taken for generate_monthly_record: {end_time - start_time} seconds")


class EmployeeSalaryPreparedManager(models.Manager):

    def bulk_prepare_salaries(self, month, year, company_id, user):
        #Importing Models
        EmployeeMonthlyAttendanceDetails = apps.get_model('api', 'EmployeeMonthlyAttendanceDetails')
        EmployeeAdvancePayment = apps.get_model('api', 'EmployeeAdvancePayment')
        EmployeeAdvanceEmiRepayment = apps.get_model('api', 'EmployeeAdvanceEmiRepayment')
        EmployeeSalaryPrepared = apps.get_model('api', 'EmployeeSalaryPrepared')
        EmployeeSalaryEarning = apps.get_model('api', 'EmployeeSalaryEarning')
        EmployeeSalaryDetail = apps.get_model('api', 'EmployeeSalaryDetail')
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        Calculations = apps.get_model('api', 'Calculations')
        PfEsiSetup = apps.get_model('api', 'PfEsiSetup')
        EarnedAmount = apps.get_model('api', 'EarnedAmount')
        EmployeePfEsiDetail = apps.get_model('api', 'EmployeePfEsiDetail')
        EarningsHead = apps.get_model('api', 'EarningsHead')

        #Querysets
        from_date=date(year, month, 1)
        to_date = from_date + relativedelta(months=1) - relativedelta(days=1)
        company_pf_esi_setup = PfEsiSetup.objects.get(user=user, company_id=company_id)
        basic_earning_head_id = EarningsHead.objects.get(user=user, company_id=company_id, name='Basic').id
        company_calculations = Calculations.objects.get(user=user, company_id=company_id)
        active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date=from_date, to_date=to_date, company_id=company_id, user=user)

        if active_employees.exists():
            for current_employee in active_employees:
                employee_pf_esi_detail = EmployeePfEsiDetail.objects.filter(company_id=company_id, employee=current_employee.employee)
                employee_salary_detail = EmployeeSalaryDetail.objects.filter(company_id=company_id, employee=current_employee.employee)
                employee_monthly_attendance_detail = EmployeeMonthlyAttendanceDetails.objects.filter(company_id=company_id, employee=current_employee.employee, date=from_date)
                employee_salary_earnings_for_each_head = EmployeeSalaryEarning.objects.filter(company_id=company_id, from_date__lte=from_date, to_date__gte=from_date, employee=current_employee.employee
                )

                if not employee_pf_esi_detail.exists() or not employee_salary_detail.exists() or not employee_monthly_attendance_detail.exists() or not employee_salary_earnings_for_each_head.exists():
                    continue
                # print(employee_monthly_attendance_detail, employee_pf_esi_detail, employee_salary_detail)
                days_in_month = calendar.monthrange(year, month)[1]
                total_salary_rate = 0
                total_earned_amount = 0
                earned_amount_dict = {}
                for salary_earning in employee_salary_earnings_for_each_head:
                    current_earning_earned_amount = (Decimal(salary_earning.value)*(Decimal(employee_monthly_attendance_detail.first().paid_days_count)/Decimal(2)))//Decimal(days_in_month)
                    # rounded_earning = math.ceil(current_earning_earned_amount) if current_earning_earned_amount >= 0.5 else math.floor(current_earning_earned_amount)
                    rounded_earning = current_earning_earned_amount.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                    total_earned_amount += rounded_earning
                    total_salary_rate += salary_earning.value
                    if current_employee.employee.attendance_card_no ==1:
                        print(f'{salary_earning.earnings_head.name}: {rounded_earning}, actual: {current_earning_earned_amount}')
                    earned_amount_dict[salary_earning.earnings_head.id] = {
                        'rate' : salary_earning.value,
                        'earned_amount' : rounded_earning,
                        'arear_amount': 0,
                    }
                print(earned_amount_dict)

                #Pf Deductions
                pf_deducted = 0
                if employee_pf_esi_detail.first().pf_allow == True:
                    if employee_pf_esi_detail.first().pf_limit_ignore_employee == False:
                        pfable_amount = min(company_pf_esi_setup.ac_1_epf_employee_limit, earned_amount_dict[basic_earning_head_id]['earned_amount'])
                        pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                        # Round the result
                        pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                    elif employee_pf_esi_detail.first().pf_limit_ignore_employee == True:
                        pfable_amount = earned_amount_dict[basic_earning_head_id]['earned_amount']
                        if employee_pf_esi_detail.first().pf_limit_ignore_employee_value != None:
                            pfable_amount = min(employee_pf_esi_detail.first().pf_limit_ignore_employee_value, earned_amount_dict[basic_earning_head_id]['earned_amount'])
                        pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                        # Round the result
                        pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                print(pf_deducted)

                #OT earned
                net_ot_minutes_monthly = 0
                net_ot_amount_monthly = 0
                if employee_salary_detail.first().overtime_type != 'no_overtime':
                    net_ot_minutes_monthly = employee_monthly_attendance_detail.first().net_ot_minutes_monthly
                    net_ot_hrs = Decimal(net_ot_minutes_monthly) / Decimal(60)
                    overtime_rate_multiplier = 2 if employee_salary_detail.first().overtime_rate == 'D' else 1
                    overtime_divisor = Decimal(26)
                    if company_calculations.ot_calculation == 'month_days':
                        overtime_divisor = Decimal(days_in_month)
                    else:
                        overtime_divisor = Decimal(company_calculations.ot_calculation)
                    net_ot_amount_monthly = Decimal(total_salary_rate) / overtime_divisor / Decimal(8) * net_ot_hrs * Decimal(overtime_rate_multiplier)
                    net_ot_amount_monthly = net_ot_amount_monthly.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)


                #ESI Deducted
                esi_deducted = 0
                if employee_pf_esi_detail.first().esi_allow == True:
                    total_earned_for_esi_deduction = total_earned_amount
                    if employee_pf_esi_detail.first().esi_on_ot == True:
                        total_earned_for_esi_deduction +=net_ot_amount_monthly
                    esiable_amount = min(company_pf_esi_setup.esi_employee_limit, total_earned_for_esi_deduction)
                    esi_deducted = Decimal(esiable_amount) * Decimal(company_pf_esi_setup.esi_employee_percentage) / Decimal(100)
                    esi_deducted = esi_deducted.quantize(Decimal('1.'), rounding=ROUND_CEILING)

                #VPF Deducted
                vpf_deducted = employee_pf_esi_detail.first().vpf_amount

                #TDS Deducted
                tds_deducted = employee_pf_esi_detail.first().tds_amount

                payment_mode = employee_salary_detail.first().payment_mode

                #Labour Wellfare Fund
                labour_welfare_fund_deducted = 0
                if company_pf_esi_setup.enable_labour_welfare_fund == True and employee_salary_detail.first().labour_wellfare_fund == True:
                    max_lwf_deduction_allowed = company_pf_esi_setup.labour_welfare_fund_limit
                    labour_welfare_fund_deducted = min(Decimal(max_lwf_deduction_allowed), Decimal(company_pf_esi_setup.labour_welfare_fund_percentage) / Decimal(100) * Decimal(total_earned_amount))
                    labour_welfare_fund_deducted = labour_welfare_fund_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

                #Deleting Advances associated with the salary prepared
                old_prepared_salary = EmployeeSalaryPrepared.objects.filter(user=user, employee=current_employee.employee, date=from_date)
                if old_prepared_salary.exists():
                    EmployeeAdvanceEmiRepayment.objects.filter(salary_prepared=old_prepared_salary.first().id).delete()

                #Calculating Advance to be deducted
                monthly_advance_repayment = 0
                employee_advances = EmployeeAdvancePayment.objects.filter(user=user, employee=current_employee.employee, company_id=company_id, date__lt=(from_date + relativedelta(months=1))).order_by('date')
                if employee_advances.exists():
                    monthly_advance_repayment = 0
                    max_advance_repayment_left = 0
                    for advance in employee_advances:
                        max_advance_repayment_left += advance.principal-advance.repaid_amount
                        if advance.emi <= (advance.principal-advance.repaid_amount):
                            monthly_advance_repayment += advance.emi
                        elif (advance.principal-advance.repaid_amount) > 0:
                            monthly_advance_repayment += (advance.principal-advance.repaid_amount)
                    print(f"Advance to be paid: {monthly_advance_repayment}")

                defaults = {
                    "user": user,
                    "employee": current_employee.employee,
                    "company_id": company_id,  # Assuming employee_instance has a related Company instance
                    "date": from_date,
                    "incentive_amount": 0,
                    "pf_deducted": pf_deducted,
                    "esi_deducted": esi_deducted,
                    "vpf_deducted": vpf_deducted,
                    "advance_deducted": monthly_advance_repayment,
                    "tds_deducted": tds_deducted,
                    "labour_welfare_fund_deducted": labour_welfare_fund_deducted,
                    "others_deducted": 0,
                    "net_ot_minutes_monthly": net_ot_minutes_monthly,
                    "net_ot_amount_monthly": net_ot_amount_monthly,
                    "payment_mode": payment_mode,
                }

                salary_prepared_obj, created = EmployeeSalaryPrepared.objects.update_or_create(
                    user=user,
                    employee=current_employee.employee,
                    date=from_date,
                    defaults=defaults,
                )
                print(f"Created: {created} Object: {salary_prepared_obj.id}")

                for earnings_head_id, earned_dict in earned_amount_dict.items():
                    defaults = {
                        "user": user,
                        "earnings_head_id": earnings_head_id,
                        "salary_prepared_id": salary_prepared_obj.id,
                        "rate": earned_dict['rate'],
                        "earned_amount": earned_dict['earned_amount'],
                        "arear_amount": 0,
                        }
                    earned_amount_obj, created = EarnedAmount.objects.update_or_create(
                        user=user,
                        salary_prepared_id=salary_prepared_obj.id,
                        earnings_head_id=earnings_head_id,
                        defaults=defaults
                    )
                
                advance_deducted_left = salary_prepared_obj.advance_deducted
                for advance in employee_advances:
                    add_to_repaid = min(advance.principal-advance.repaid_amount, advance.emi)
                    EmployeeAdvanceEmiRepayment.objects.create(user=user, amount=min(add_to_repaid, advance_deducted_left), employee_advance_payment_id=advance.id, salary_prepared_id=salary_prepared_obj.id)
                    advance_deducted_left -= min(add_to_repaid, advance_deducted_left)

                
                print(f'ESI Deducted: {esi_deducted} Employee Name: {current_employee.employee.name}')


        print(month, year)
        return True, "Operation successful"