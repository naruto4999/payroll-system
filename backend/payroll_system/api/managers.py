from django.db import models
# from api.models import EmployeePersonalDetail, EmployeeProfessionalDetail
from django.db.models import Q
from django.apps import apps
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import random
import time



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
        # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        weekday = date.strftime('%a').lower()

        # Calculate the ordinal number of the weekday in the month
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
                start_time_before_while = time.time()

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
                end_time_before_while = time.time()

                start_time_while = time.time()

                #Deleting the existing attendances between the from_date and to_date inclusive
                attendance_to_delete = self.filter(
                    employee=current_employee.employee,
                    date__range=(from_date, to_date),
                    company_id=company_id,
                )
                    
                if attendance_to_delete.exists():
                    # print(f"Deleting attendance for {current_employee.employee}'s on {current_date}")
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

                total_expected_instances = 0
                while current_date <= to_date:
                    
                    if current_date >= current_employee.date_of_joining and (current_employee.resigned == False or current_date<=current_employee.resignation_date):
                        if current_date.strftime('%a').lower() == current_employee.weekly_off or (self.weekday_occurrence_in_month(date=current_date) == current_employee.extra_off):
                            weekly_off_to_give = weekly_off_skip
                            if self.paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                weekly_off_to_give = weekly_off
                            self.create(user=user, company_id=company_id, employee=current_employee.employee, first_half=weekly_off_to_give, second_half=weekly_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0)
                            total_expected_instances +=1

                        #If Current date is a holdiday
                        elif holiday_queryset.filter(date=current_date).exists():
                            holiday_off_to_give = holiday_off_skip
                            if self.paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                holiday_off_to_give = holiday_off
                            self.create(user=user, company_id=company_id, employee=current_employee.employee, first_half=holiday_off_to_give, second_half=holiday_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0)
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
                            self.create(user=user, company_id=company_id, employee=current_employee.employee, first_half=present_leave, second_half=present_leave, manual_in=self.generate_random_time(reference_time=found_shift_beginning_time, start_buffer=AUTO_SHIFT_BEGINNING_BUFFER_BEFORE, end_buffer=found_shift_late_grace), manual_out=self.generate_random_time(reference_time=found_shift_end_time, start_buffer=AUTO_SHIFT_ENDING_BUFFER_BEFORE, end_buffer=AUTO_SHIFT_ENDING_BUFFER_AFTER), machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0)
                            total_expected_instances +=1
                    current_date += relativedelta(days=1)
                end_time_while = time.time()
                print(f"Time taken by the while loop: {end_time_while - start_time_while} seconds")
                print(f"Time taken before while loop: {end_time_before_while - start_time_before_while} seconds")


                start_time = time.time()
                EmployeeGenerativeLeaveRecord.objects.generate_monthly_record(total_expected_instances=total_expected_instances, user=user, year=from_date.year, month=from_date.month, employee=current_employee.employee, company=current_employee.company)
                end_time = time.time()
                print(f"Time taken for generate_monthly_record: {end_time - start_time} seconds")





