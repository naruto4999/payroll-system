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
import pandas_access as mdb
from io import BytesIO
import tempfile
import os
import pandas as pd




def weekday_occurrence_in_month(date):
        weekday = date.strftime('%a').lower()
        ordinal_number = (date.day - 1) // 7 + 1
        return f"{weekday}{ordinal_number}"

def paid_days_count_for_past_six_days(attendance_date, company_id, user, employee):
    EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
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
                        if current_date.strftime('%a').lower() == current_employee.weekly_off or (weekday_occurrence_in_month(date=current_date) == current_employee.extra_off):
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            weekly_off_to_give = weekly_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                weekly_off_to_give = weekly_off
                            attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, employee=current_employee.employee, first_half=weekly_off_to_give, second_half=weekly_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0))
                            total_expected_instances +=1

                        #If Current date is a holdiday
                        elif holiday_queryset.filter(date=current_date).exists():
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            holiday_off_to_give = holiday_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                holiday_off_to_give = holiday_off
                            attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, employee=current_employee.employee, first_half=holiday_off_to_give, second_half=holiday_off_to_give, manual_in=None, manual_out=None, machine_in=None, machine_out=None, date=current_date, ot_min=None, late_min=None, pay_multiplier=1.0))
                            total_expected_instances +=1

                        #It's not weekly off nor holiday off
                        else:
                            if not shift_found or (current_date < shift_from_date or current_date > shift_to_date):
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
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)
                # end_time = time.time()
                # print(f"Time taken for generate_update_monthly_record: {end_time - start_time} seconds")

    def machine_attendance(self, from_date, to_date, company_id, user, all_employees_machine_attendance, mdb_database, employee):
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        WeeklyOffHolidayOff = apps.get_model('api', 'WeeklyOffHolidayOff')
        EmployeeGenerativeLeaveRecord = apps.get_model('api', 'EmployeeGenerativeLeaveRecord')
        EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
        # Read the content of the TemporaryUploadedFile
        mdb_content = mdb_database.read()
        print(f'From Date: {from_date} End Date: {to_date}')
        Holiday = apps.get_model('api', 'Holiday')
        LeaveGrade = apps.get_model('api', 'LeaveGrade')


        # Create a temporary file and write the content to it
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(mdb_content)

        try:
            # Now you can use the temporary file path with mdb.read_table
            df = mdb.read_table(temp_file.name, 'CHECKINOUT')
            # print(df.tail(40).sort_values(by='USERID'))
            df['CHECKTIME'] = pd.to_datetime(df['CHECKTIME'], format='%m/%d/%y %H:%M:%S', errors='coerce')
            filtered_rows = df[(df['CHECKTIME'] >= (from_date - relativedelta(days=1))) & (df['CHECKTIME'] <= (to_date + relativedelta(days=1)))]

            #Leaves
            present_leave = LeaveGrade.objects.get(company_id=company_id, user=user, name='P')
            print(present_leave)
            miss_punch = LeaveGrade.objects.get(company_id=company_id, user=user, name='MS')
            absent_leave = LeaveGrade.objects.get(company_id=company_id, user=user, name='A')
            weekly_off = LeaveGrade.objects.get(company_id=company_id, user=user, name='WO')
            weekly_off_skip = LeaveGrade.objects.get(company_id=company_id, user=user, name='WO*')
            holiday_off = LeaveGrade.objects.get(company_id=company_id, user=user, name='HD')
            holiday_off_skip = LeaveGrade.objects.get(company_id=company_id, user=user, name='HD*')

            #WeeklyOffHolidayOff
            weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(user=user, company_id=company_id)

            #Holiday Queryset
            holiday_queryset = Holiday.objects.filter(user=user, company_id=company_id)

            #Getting Active Employees between dates
            if all_employees_machine_attendance == True:
                active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date=from_date, to_date=to_date, company_id=company_id, user=user)
            else:
                active_employees = EmployeeProfessionalDetail.objects.filter(user=user, company_id=company_id, employee_id=employee)
            
            start_time_before_while = time.time()
            for current_employee in active_employees:
                #Current Employee Salary Detail
                current_employee_salary_detail = None
                try:
                    current_employee_salary_detail = current_employee.employee.employee_salary_detail
                except:
                    continue

                #current_employee user_id in machine db
                user_info_df = mdb.read_table(temp_file.name, 'USERINFO')
                # print(user_info_df.tail(50))
                print(type(user_info_df['Badgenumber'].iloc[0]))
                print(f'Current Employee ACN: {current_employee.employee.attendance_card_no}')
                filtered_user_info = user_info_df[user_info_df['Badgenumber'] == str(current_employee.employee.attendance_card_no)]
                user_id = None
                if not filtered_user_info.empty:
                    user_id = filtered_user_info['USERID'].iloc[0]
                    print(f"The USERID for Badgenumber is: {user_id}")
                else:
                    print(f"No USERID found for Badgenumber/ACN {current_employee.employee.attendance_card_no}")
                    continue
                #Filter the Dataframe rows corresponding to the current employee
                employee_rows = filtered_rows[filtered_rows['USERID'] == user_id]
                employee_rows_asc_time = employee_rows.sort_values(by='CHECKTIME', ascending=True)
                employee_rows_desc_time = employee_rows.sort_values(by='CHECKTIME', ascending=False)
                print(employee_rows_desc_time)
                print(employee_rows_desc_time)
                #Getting Shift Before the start of the loop
                employee_shift_on_particular_date=None
                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=from_date, to_date__gte=from_date)
                if employee_shift_on_particular_date_queryset.exists():
                    employee_shift_on_particular_date = employee_shift_on_particular_date_queryset.first()
                    shift_from_date = employee_shift_on_particular_date.from_date
                    shift_to_date = employee_shift_on_particular_date.to_date
                
                attendance_records = []
                update_attendance_records = []
                current_date = from_date

                # Fetch all existing attendance records within the date range for current employee
                date_range = [from_date + timedelta(days=i) for i in range((to_date - from_date).days + 1)]
                attendance_by_date = self.filter(user=user, company_id=company_id, employee=current_employee.employee, date__in=date_range).distinct("date").in_bulk(field_name='date')
                # print(attendance_by_date)

                while current_date <= to_date:
                    #Get current attendance if any
                    skip_calculating_attendances = False
                    # existing_attendance = self.filter(user=user, company_id=company_id, date=current_date, employee=current_employee.employee)
                    existing_attendance = attendance_by_date.get(current_date.date(), None)
                    if existing_attendance != None:
                        if existing_attendance.manual_in != None and existing_attendance.manual_out != None:
                            skip_calculating_attendances = True
                    # print(current_date.strftime("%Y-%m-%d"))  # or do something with the date
                    #Get the shift of the current employee
                    if employee_shift_on_particular_date==None or (current_date.date() < shift_from_date or current_date.date() > shift_to_date):
                                print('Yes Refetching')
                                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date)
                                if employee_shift_on_particular_date_queryset.exists():
                                    employee_shift_on_particular_date = employee_shift_on_particular_date_queryset.first()
                                    shift_from_date = employee_shift_on_particular_date.from_date
                                    shift_to_date = employee_shift_on_particular_date.to_date

                    # employee_shift_on_particular_date = EmployeeShifts.objects.get(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date)
                    
                    #Shift Beginnning time and End Time with current date
                    shift_beginning_time = datetime.combine(current_date.date(), employee_shift_on_particular_date.shift.beginning_time)
                    shift_end_time = datetime.combine(current_date.date() if employee_shift_on_particular_date.shift.end_time > employee_shift_on_particular_date.shift.beginning_time else current_date.date()+relativedelta(days=1), employee_shift_on_particular_date.shift.end_time)

                    #Minimum in and Maximum Out times, also change the 3 hrs used here later on by some settings so that the user can modify this option
                    minimum_in_time = shift_beginning_time - relativedelta(hours=3) #inclusive meaning the intime can in equal to this
                    maximum_out_time = minimum_in_time + relativedelta(days=1) #Exclusive meaning the outtime should be less than this
                    possible_punch_in_times = employee_rows_asc_time[(employee_rows_asc_time['CHECKTIME'] >= minimum_in_time) & (employee_rows_asc_time['CHECKTIME'] < maximum_out_time)]
                    possible_punch_out_times = employee_rows_desc_time[(employee_rows_desc_time['CHECKTIME'] < maximum_out_time) & (employee_rows_desc_time['CHECKTIME'] > minimum_in_time)]
                    
                    punch_in_row = pd.DataFrame(columns=possible_punch_in_times.columns)
                    punch_out_row = pd.DataFrame(columns=possible_punch_in_times.columns)
                    if not possible_punch_in_times.empty:
                        punch_in_row = possible_punch_in_times.iloc[0]
                        
                    if not possible_punch_out_times.empty:
                        punch_out_row = possible_punch_out_times.iloc[0]

                    punch_in_time = None
                    punch_out_time = None
                    machine_punch_in = None
                    machine_punch_out = None
                    #Checking for punch in time
                    if existing_attendance != None and existing_attendance.manual_in is not None:
                        if employee_shift_on_particular_date.shift.beginning_time < employee_shift_on_particular_date.shift.end_time:
                            if existing_attendance.manual_in < employee_shift_on_particular_date.shift.end_time:
                                punch_in_time = datetime.combine(current_date.date(), existing_attendance.manual_in)
                            elif existing_attendance.manual_in > employee_shift_on_particular_date.shift.end_time:
                                punch_in_time = datetime.combine(current_date.date(), existing_attendance.manual_in) - relativedelta(days=1)
                        if employee_shift_on_particular_date.shift.beginning_time > employee_shift_on_particular_date.shift.end_time:
                            if existing_attendance.manual_in < employee_shift_on_particular_date.shift.end_time:
                                punch_in_time = datetime.combine(current_date.date(), existing_attendance.manual_in) + relativedelta(days=1)
                            else:
                                punch_in_time = datetime.combine(current_date.date(), existing_attendance.manual_in)
                    
                    #Punch in from machine
                    elif not punch_in_row.empty and 'CHECKTIME' in punch_in_row:
                        punch_in_time = datetime.combine(punch_in_row['CHECKTIME'].date(), punch_in_row['CHECKTIME'].time().replace(second=0))
                        if punch_in_time > shift_end_time-relativedelta(minutes=employee_shift_on_particular_date.shift.half_day_minimum_minutes):
                            punch_in_time=None
                    
                    if not punch_in_row.empty and 'CHECKTIME' in punch_in_row:
                        machine_punch_in = datetime.combine(punch_in_row['CHECKTIME'].date(), punch_in_row['CHECKTIME'].time().replace(second=0))
                        if machine_punch_in > shift_end_time-relativedelta(minutes=employee_shift_on_particular_date.shift.half_day_minimum_minutes):
                            machine_punch_in=None
                        

                    #Checking for punch out time
                    if existing_attendance != None and existing_attendance.manual_out is not None:
                        if employee_shift_on_particular_date.shift.beginning_time < employee_shift_on_particular_date.shift.end_time:
                            if existing_attendance.manual_out > employee_shift_on_particular_date.shift.beginning_time:
                                punch_out_time = datetime.combine(current_date.date(), existing_attendance.manual_out)
                            elif existing_attendance.manual_out < employee_shift_on_particular_date.shift.beginning_time:
                                punch_out_time = datetime.combine(current_date.date(), existing_attendance.manual_out) + relativedelta(days=1)
                        else:
                            if existing_attendance.manual_out < employee_shift_on_particular_date.shift.beginning_time:
                                punch_out_time = datetime.combine(current_date.date(), existing_attendance.manual_out) + relativedelta(days=1)
                            else:
                                punch_out_time = datetime.combine(current_date.date(), existing_attendance.manual_out)
                    
                    #Punch out from machine
                    elif not punch_out_row.empty and 'CHECKTIME' in punch_out_row:
                        if not punch_out_row.empty and not punch_in_row.empty:
                            punch_out_time = datetime.combine(punch_out_row['CHECKTIME'].date() ,punch_out_row['CHECKTIME'].time().replace(second=0))
                            if punch_out_time == punch_in_time:
                                punch_out_time = None
                    
                    if not punch_out_row.empty and 'CHECKTIME' in punch_out_row:
                        if not punch_out_row.empty and not punch_in_row.empty:
                            machine_punch_out = datetime.combine(punch_out_row['CHECKTIME'].date() ,punch_out_row['CHECKTIME'].time().replace(second=0))
                            if machine_punch_out == machine_punch_in:
                                machine_punch_out = None

                    #Calculating OT
                    # print(f'Punch in time : {punch_in_time} Punch out time : {punch_out_time}')
                    overtime_minutes = timedelta(minutes=0)
                    if current_employee_salary_detail.overtime_type != 'no_overtime':
                        if not skip_calculating_attendances and (punch_in_time is not None and punch_out_time is not None):
                            if current_date.strftime('%a').lower() == current_employee.weekly_off or (weekday_occurrence_in_month(date=current_date) == current_employee.extra_off) or holiday_queryset.filter(date=current_date).exists():
                                print('Chhutti')
                                minutes_worked = (punch_out_time - punch_in_time)
                                # print(minutes_worked)
                                if minutes_worked > timedelta(minutes=employee_shift_on_particular_date.shift.ot_begin_after):
                                    overtime_minutes += minutes_worked
                            elif current_employee_salary_detail.overtime_type == 'all_days':
                                arrived_early_minutes = shift_beginning_time - punch_in_time
                                if arrived_early_minutes > timedelta(minutes=employee_shift_on_particular_date.shift.ot_begin_after):
                                    overtime_minutes += arrived_early_minutes
                                over_stayed_minutes = punch_out_time - datetime.combine(current_date.date(), employee_shift_on_particular_date.shift.end_time)
                                if over_stayed_minutes > timedelta(minutes=employee_shift_on_particular_date.shift.ot_begin_after):
                                    overtime_minutes += over_stayed_minutes
                    overtime_minutes_integer = int(overtime_minutes.total_seconds() / 60)
                    if overtime_minutes_integer > 0:
                        overtime_minutes_integer = (overtime_minutes_integer//30) * 30 + (30 if overtime_minutes_integer%30>15 else 0)
                    else:
                        overtime_minutes_integer = None

                    #Calculating Late
                    late_minutes = timedelta(minutes=0)
                    # print(f"skip attendance?: {skip_calculating_attendances}")
                    if current_date.strftime('%a').lower() != current_employee.weekly_off and (weekday_occurrence_in_month(date=current_date) != current_employee.extra_off) and (not holiday_queryset.filter(date=current_date).exists()) and not skip_calculating_attendances:
                        print(f'Date: {current_date} Yes Late')
                        print(f'Punch in time: {punch_in_time}')
                        if punch_in_time != None:
                            print('Yes Not None')
                            if punch_in_time > (shift_beginning_time + relativedelta(minutes=employee_shift_on_particular_date.shift.late_grace)):
                                late_minutes += (punch_in_time - shift_beginning_time)
                                # print(f'In Time: {punch_in_row["CHECKTIME"]} Late: {late_minutes}')
                    late_minutes_integer = int(late_minutes.total_seconds() / 60) #Set to None while saving if late minutes are 0

                    # print(f'OT Integer Minutes: {overtime_minutes_integer} Late Minutes: {late_minutes_integer}')

                    #Marking Attendance
                    if not skip_calculating_attendances:
                        first_half = absent_leave
                        second_half = absent_leave
                        if current_date.strftime('%a').lower() == current_employee.weekly_off or (weekday_occurrence_in_month(date=current_date) == current_employee.extra_off):
                            if len(attendance_records) != 0:
                                self.bulk_create(attendance_records)
                                attendance_records.clear()
                            if len(update_attendance_records) !=0:
                                self.bulk_update(update_attendance_records, ["machine_in", "machine_out", "manual_in", "manual_out", "first_half", "second_half", "ot_min", "late_min", "pay_multiplier"])
                                update_attendance_records.clear()

                            first_half = weekly_off_skip
                            second_half = weekly_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                first_half = weekly_off
                                second_half = weekly_off

                        elif holiday_queryset.filter(date=current_date).exists():
                            if len(attendance_records) != 0:
                                self.bulk_create(attendance_records)
                                attendance_records.clear()
                            if len(update_attendance_records) !=0:
                                self.bulk_update(update_attendance_records, ["machine_in", "machine_out", "manual_in", "manual_out", "first_half", "second_half", "ot_min", "late_min", "pay_multiplier"])
                                update_attendance_records.clear()
                            first_half = holiday_off_skip
                            second_half = holiday_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                first_half = holiday_off
                                second_half = holiday_off
                        else:
                            if punch_in_time is not None and punch_out_time is not None:
                                total_worked_minutes = punch_out_time - punch_in_time
                                if total_worked_minutes >= timedelta(minutes=employee_shift_on_particular_date.shift.full_day_minimum_minutes):
                                    if late_minutes_integer <= employee_shift_on_particular_date.shift.max_late_allowed_min:
                                        first_half = present_leave
                                        second_half = present_leave
                                    else:
                                        first_half = absent_leave
                                        second_half = present_leave
                                elif total_worked_minutes < timedelta(minutes=employee_shift_on_particular_date.shift.full_day_minimum_minutes) and total_worked_minutes >= timedelta(minutes=employee_shift_on_particular_date.shift.half_day_minimum_minutes):
                                    if late_minutes_integer <= employee_shift_on_particular_date.shift.max_late_allowed_min:
                                        first_half = present_leave
                                        second_half = absent_leave
                                    else:
                                        first_half = absent_leave
                                        second_half = present_leave
                                else:
                                    first_half = absent_leave
                                    second_half = absent_leave
                            elif punch_in_time is not None or punch_out_time is not None:
                                first_half = miss_punch
                                second_half = miss_punch
                    print(f'date: {current_date} Late Minutes Integer: {late_minutes_integer} Late Min: {late_minutes}')
                    # print(f"Frist Half: {first_half} Second Half: {second_half}")
                    # defaults = {
                    # "machine_in": machine_punch_in,
                    # "machine_out": machine_punch_out,
                    # "manual_in": existing_attendance.manual_in if existing_attendance != None else None,
                    # "manual_out": existing_attendance.manual_out if existing_attendance != None else None,
                    # }
                    # if not skip_calculating_attendances:
                    #     defaults['first_half'] = first_half
                    #     defaults['second_half'] = second_half
                    #     defaults['ot_min'] = overtime_minutes_integer
                    #     defaults['late_min'] = late_minutes_integer if late_minutes_integer!=0 else None

                    if existing_attendance != None:
                        existing_attendance_obj = existing_attendance
                        existing_attendance_obj.machine_in = machine_punch_in
                        existing_attendance_obj.machine_out = machine_punch_out
                        existing_attendance_obj.manual_in = existing_attendance_obj.manual_in if existing_attendance != None else None
                        existing_attendance_obj.manual_out = existing_attendance_obj.manual_out if existing_attendance != None else None
                        if not skip_calculating_attendances:
                            pay_multiplier = 0
                            if first_half.paid and second_half.paid:
                                pay_multiplier = 1
                            elif first_half.paid or second_half.paid:
                                pay_multiplier = 0.5
                            existing_attendance_obj.first_half = first_half
                            existing_attendance_obj.second_half = second_half
                            existing_attendance_obj.ot_min = overtime_minutes_integer
                            existing_attendance_obj.late_min = late_minutes_integer if late_minutes_integer!=0 and late_minutes_integer<=employee_shift_on_particular_date.shift.max_late_allowed_min else None
                            existing_attendance_obj.pay_multiplier = pay_multiplier
                        update_attendance_records.append(existing_attendance_obj)


                    
                    # create_defaults_for_attendance = {
                    #     "user": user,
                    #     "company_id": company_id,
                    #     "date": current_date,
                    #     "employee": current_employee.employee,
                    #     "machine_in": machine_punch_in,
                    #     "machine_out": machine_punch_out,
                    #     "manual_in": None,
                    #     "manual_out": None,
                    #     "first_half": first_half,
                    #     "second_half": second_half,
                    #     "ot_min": overtime_minutes_integer,
                    #     "late_min": late_minutes_integer if late_minutes_integer!=0 else None,
                    # }
                    
                    # attendance_object, created = self.update_or_create(
                    #     user = user,
                    #     company_id = company_id,
                    #     date = current_date,
                    #     employee = current_employee.employee,
                    #     defaults = defaults,
                    #     create_defaults = create_defaults_for_attendance,
                    #     )
                    # print(f"Created: {created} Object: {attendance_object.id}")
                    # print(f'Update Records: {update_attendance_records}')

                    if existing_attendance == None:
                        pay_multiplier = 0
                        if first_half.paid and second_half.paid:
                            pay_multiplier = 1
                        elif first_half.paid or second_half.paid:
                            pay_multiplier = 0.5
                        attendance_records.append(EmployeeAttendance(user=user, company_id=company_id, date=current_date, employee=current_employee.employee, machine_in=machine_punch_in, machine_out=machine_punch_out, manual_in=None, manual_out=None, first_half=first_half, second_half=second_half, ot_min=overtime_minutes_integer, late_min=late_minutes_integer if late_minutes_integer!=0 and late_minutes_integer<=employee_shift_on_particular_date.shift.max_late_allowed_min else None, pay_multiplier=pay_multiplier))
                    current_date += timedelta(days=1)
                
                if len(attendance_records) != 0:
                    self.bulk_create(attendance_records)
                    attendance_records.clear()

                if len(update_attendance_records) !=0:
                    self.bulk_update(update_attendance_records, ["machine_in", "machine_out", "manual_in", "manual_out", "first_half", "second_half", "ot_min", "late_min", "pay_multiplier"])
                    update_attendance_records.clear()

                #Generating Monthly Attendace records
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=from_date.year, month=from_date.month, employee_id=current_employee.employee.id, company_id=current_employee.company.id)
            end_time_after_while = time.time()
            print(f"Time taken: {end_time_after_while - start_time_before_while} seconds")



        finally:
            # Clean up: Delete the temporary file
            temp_file.close()
            # Comment the line below if you don't want to delete the temporary file
            os.unlink(temp_file.name)

        return True, "Operation successful"


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