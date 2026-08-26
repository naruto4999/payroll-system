from django.db import models
# from api.models import EmployeePersonalDetail, EmployeeProfessionalDetail
from django.db.models import Q
from django.apps import apps
from collections import defaultdict
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
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MACHINE_ATTENDANCE_CREATE_BATCH_SIZE = 500
MACHINE_ATTENDANCE_UPDATE_BATCH_SIZE = 100

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

    @staticmethod
    def _owner_for(user):
        if user.role == 'OWNER':
            return user
        if user.role == 'REGULAR':
            try:
                return user.regular_to_owner.owner
            except ObjectDoesNotExist as exc:
                raise ValidationError({'user': 'Regular account is not linked to an owner.'}) from exc
        raise ValidationError({'user': 'Unsupported account role.'})

    @classmethod
    def _validate_company(cls, *, user, company_id):
        Company = apps.get_model('api', 'Company')
        owner = cls._owner_for(user)
        try:
            company = Company.objects.get(pk=company_id, user=owner)
        except Company.DoesNotExist as exc:
            raise ValidationError({'company': 'Company does not belong to the authenticated account.'}) from exc
        if user.role == 'REGULAR' and not company.visible:
            raise ValidationError({'company': 'Company is not available to this account.'})
        return owner, company

    @staticmethod
    def _month_keys(from_date, to_date):
        current = from_date.replace(day=1)
        end = to_date.replace(day=1)
        months = []
        while current <= end:
            months.append((current.year, current.month))
            current += relativedelta(months=1)
        return months

    @staticmethod
    def _regenerate_months(*, user, company_id, employee_ids, months):
        EmployeeGenerativeLeaveRecord = apps.get_model('api', 'EmployeeGenerativeLeaveRecord')
        for employee_id in sorted(set(employee_ids)):
            for year, month in sorted(set(months)):
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(
                    user=user,
                    year=year,
                    month=month,
                    employee_id=employee_id,
                    company_id=company_id,
                )

    def reevaluate_first_weekly_holiday_off_after_doj(self, user, employee, date_of_joining):
        #Importing models 
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        LeaveGrade = apps.get_model('api', 'LeaveGrade')
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        WeeklyOffHolidayOff = apps.get_model('api', 'WeeklyOffHolidayOff')

        employee = EmployeeProfessionalDetail.objects.get(employee=employee)        
        weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(user=user if user.role=='OWNER' else user.regular_to_owner.owner, company_id=employee.company.id)
        weekly_off = LeaveGrade.objects.get(company_id=employee.company.id, user=user if user.role=='OWNER' else user.regular_to_owner.owner, name='WO')
        weekly_off_skip = LeaveGrade.objects.get(company_id=employee.company.id, user=user if user.role=='OWNER' else user.regular_to_owner.owner, name='WO*')
        holiday_off = LeaveGrade.objects.get(company_id=employee.company.id, user=user if user.role=='OWNER' else user.regular_to_owner.owner, name='HD')
        holiday_off_skip = LeaveGrade.objects.get(company_id=employee.company.id, user=user if user.role=='OWNER' else user.regular_to_owner.owner, name='HD*')

        one_week_later = date_of_joining + relativedelta(weeks=1)
        employee_first_weekly_off = EmployeeAttendance.objects.filter(
            Q(first_half=weekly_off) | Q(first_half=weekly_off_skip),
            Q(second_half=weekly_off) | Q(second_half=weekly_off_skip),
            user=user,  # This is user
            employee=employee.employee,
            date__gte=date_of_joining,
            date__lte=one_week_later,
        ).order_by('date')

        if employee_first_weekly_off.exists():
            employee_first_weekly_off = employee_first_weekly_off.first()
            days_to_first_weekly_off = (employee_first_weekly_off.date-date_of_joining).days
            print(f"First Weekly Off: {employee_first_weekly_off.date}")
            print(f"Days to first weekly off: {days_to_first_weekly_off} Weekly Off Min Days: {weekly_off_holiday_off.min_days_for_weekly_off}")
            #If first weekly off arrived earlier than the minimum weekly off days
            if days_to_first_weekly_off<weekly_off_holiday_off.min_days_for_weekly_off:
                attendance_between_first_weekly_off_and_doj = EmployeeAttendance.objects.filter(
                    user=user,  # This is user
                    employee=employee.employee,
                    date__gte=date_of_joining,
                    date__lt=employee_first_weekly_off.date,
                ).order_by('date')
                present_all_days_before_weekly_off = True
                for attendance in attendance_between_first_weekly_off_and_doj:
                    if attendance.first_half.paid==False or attendance.second_half.paid==False:
                        present_all_days_before_weekly_off = False
                        break
                employee_first_weekly_off.first_half=weekly_off if present_all_days_before_weekly_off else weekly_off_skip
                employee_first_weekly_off.second_half=weekly_off if present_all_days_before_weekly_off else weekly_off_skip
                employee_first_weekly_off.save()
                        
            else:
                if paid_days_count_for_past_six_days(user=user, company_id=employee.company.id, attendance_date=employee_first_weekly_off.date, employee=employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                    employee_first_weekly_off.first_half=weekly_off
                    employee_first_weekly_off.second_half=weekly_off
                    employee_first_weekly_off.save()
                else:
                    employee_first_weekly_off.first_half=weekly_off_skip
                    employee_first_weekly_off.first_half=weekly_off_skip
                    employee_first_weekly_off.save()

            
        #Just code the post save receiver now for both the users and check


                    




    



    
    def generate_random_time(self, reference_time, start_buffer, end_buffer):
        reference_datetime = datetime.combine(datetime.today(), reference_time)
        reference_datetime -= relativedelta(minutes=start_buffer)
        random_time_difference = timedelta(minutes=random.randint(0, start_buffer+end_buffer))
        random_time = (reference_datetime+random_time_difference).time()
        return random_time.replace(second=0)
    
    @transaction.atomic
    def mark_default_attendance(self, from_date, to_date, company_id, user):
        # try:
        LeaveGrade = apps.get_model('api', 'LeaveGrade')
        WeeklyOffHolidayOff = apps.get_model('api', 'WeeklyOffHolidayOff')
        EmployeeGenerativeLeaveRecord = apps.get_model('api', 'EmployeeGenerativeLeaveRecord')
        owner, company = self._validate_company(user=user, company_id=company_id)
        weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(user=owner, company=company)
        Holiday = apps.get_model('api', 'Holiday')
        holiday_queryset = Holiday.objects.filter(user=owner, company=company)

        #Leaves
        absent_leave = LeaveGrade.objects.get(company=company, user=owner, name='A')
        weekly_off = LeaveGrade.objects.get(company=company, user=owner, name='WO')
        weekly_off_skip = LeaveGrade.objects.get(company=company, user=owner, name='WO*')
        holiday_off = LeaveGrade.objects.get(company=company, user=owner, name='HD')
        holiday_off_skip = LeaveGrade.objects.get(company=company, user=owner, name='HD*')
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date=from_date, to_date=to_date, company_id=company_id, user=owner)
        print(f"Length of active employees: {len(active_employees)}")
        if active_employees.exists():
            for employee in active_employees:
                try: employee.employee.employee_salary_detail
                except: continue
                existing_attendance_dates = set(
                    EmployeeAttendance.objects.filter(
                        Q(user=user) &
                        Q(employee=employee.employee) &
                        Q(date__gte=from_date) &
                        Q(date__lte=to_date)
                    ).values_list('date', flat=True)
                )
                date_range = [from_date + timedelta(days=x) for x in range((to_date - from_date).days + 1)]
                dates_without_attendance = [date for date in date_range if date not in existing_attendance_dates]
                print(f"Dates without attendances: {dates_without_attendance}")

                # Mark attendance for dates where attendance object doesn't exist
                attendance_records = []
                total_expected_instances = 0
                for current_date in dates_without_attendance:
                    if current_date >= employee.date_of_joining and (employee.resigned == False or current_date<=employee.resignation_date):

                        if (employee.employee.employee_salary_detail.salary_mode.lower() != 'daily') and (holiday_queryset.filter(date=current_date).exists()):
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            holiday_off_to_give = holiday_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                holiday_off_to_give = holiday_off
                            pay_multiplier = 0
                            if holiday_off_to_give.paid:
                                pay_multiplier = 1.0
                            attendance_records.append(EmployeeAttendance(user=user, company=company, employee=employee.employee, first_half=holiday_off_to_give, second_half=holiday_off_to_give, date=current_date, pay_multiplier=pay_multiplier))
                            total_expected_instances +=1

                        elif (employee.employee.employee_salary_detail.salary_mode.lower() != 'daily') and (current_date.strftime('%a').lower() == employee.weekly_off or (weekday_occurrence_in_month(date=current_date) == employee.extra_off)):
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()
                            weekly_off_to_give = weekly_off_skip
                            if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                weekly_off_to_give = weekly_off
                            pay_multiplier = 0
                            if weekly_off_to_give.paid:
                                pay_multiplier = 1.0
                            attendance_records.append(EmployeeAttendance(user=user, company=company, employee=employee.employee, first_half=weekly_off_to_give, second_half=weekly_off_to_give, date=current_date, pay_multiplier=pay_multiplier))
                            total_expected_instances +=1


                        else:
                            attendance_records.append(EmployeeAttendance(user=user, company=company, employee=employee.employee, first_half=absent_leave, second_half=absent_leave, date=current_date, pay_multiplier=0))
                            total_expected_instances +=1
                    current_date += relativedelta(days=1)
                    print(attendance_records)
                
                EmployeeAttendance.objects.bulk_create(attendance_records)
                self._regenerate_months(
                    user=user,
                    company_id=company.id,
                    employee_ids=[employee.employee_id],
                    months=self._month_keys(from_date, to_date),
                )
        return True, "Operation successful"
        # except:
        #     return False, "Operation Failed"
    
    # def get_employee_shift_on_date(self, user, company_id, employee, date_to_find):
    #     EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
    #     employee_shift_on_particular_date = EmployeeShifts.objects.filter(company_id=company_id, user=user, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date).first()

    @transaction.atomic
    def bulk_autofill(self, from_date, to_date, company_id, user, employee_ids=None):
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
        employee_ids = list(employee_ids or ())
        owner, company = self._validate_company(user=user, company_id=company_id)
        holiday_queryset = Holiday.objects.filter(user=owner, company=company)
        weekly_off_holiday_off = WeeklyOffHolidayOff.objects.get(user=owner, company=company)
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        if len(employee_ids)==0:
            active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date, to_date, company_id=company_id, user=owner)
        else:
            active_employees = EmployeeProfessionalDetail.objects.filter(employee__id__in=employee_ids, company=company, user=owner)
            found_ids = set(active_employees.values_list('employee_id', flat=True))
            if found_ids != set(employee_ids):
                raise ValidationError({'employee_ids': 'Every employee must belong to the requested company.'})

        #Leaves
        present_leave = LeaveGrade.objects.get(company=company, user=owner, name='P')
        absent = LeaveGrade.objects.get(company=company, user=owner, name='A')
        weekly_off = LeaveGrade.objects.get(company=company, user=owner, name='WO')
        weekly_off_skip = LeaveGrade.objects.get(company=company, user=owner, name='WO*')
        holiday_off = LeaveGrade.objects.get(company=company, user=owner, name='HD')
        holiday_off_skip = LeaveGrade.objects.get(company=company, user=owner, name='HD*')


        # Calculate the range of dates
        if active_employees.exists():
            for current_employee in active_employees:
                employee_salary_detail = EmployeeSalaryDetail.objects.filter(company_id=company_id, employee=current_employee.employee).first()
                if not employee_salary_detail:
                    continue

                month_starts = [date(year, month, 1) for year, month in self._month_keys(from_date, to_date)]
                montly_attendance_record_to_delete = EmployeeMonthlyAttendanceDetails.objects.filter(
                        employee=current_employee.employee,
                        date__in=month_starts,
                        company=company,
                        user=user,
                    )
                if montly_attendance_record_to_delete.exists():
                        montly_attendance_record_to_delete.delete()
                generative_leave_record_to_delete = EmployeeGenerativeLeaveRecord.objects.filter(
                        employee=current_employee.employee,
                        date__in=month_starts,
                        company=company,
                        user=user,
                    )
                if generative_leave_record_to_delete.exists():
                        generative_leave_record_to_delete.delete()
                current_date = from_date

                #Deleting the existing attendances between the from_date and to_date inclusive
                attendance_to_delete = self.filter(
                    Q(employee=current_employee.employee) &
                    Q(date__range=(from_date, to_date)) &
                    Q(company_id=company_id) &
                    Q(user=user)
                )
                attendance_to_delete.delete()

                #Optimizing shifts retrieval
                shift_found = False
                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=current_employee.employee, from_date__lte=from_date, to_date__gte=from_date)
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
                        
                        #If Current date is a holdiday
                        if holiday_queryset.filter(date=current_date).exists():
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records) #Bulk create here to update the attendances before calling paid days function
                            attendance_records.clear()

                            if employee_salary_detail.salary_mode.lower() == 'daily':
                                #It's daily wage employee so mark as absent since holiday off cannot be given to daily wage employees
                                attendance_records.append(EmployeeAttendance(user=user, company=company, employee=current_employee.employee, first_half=absent, second_half=absent, date=current_date, pay_multiplier=0))
                            else:
                                holiday_off_to_give = holiday_off_skip
                                if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_holiday_off * 2):
                                    holiday_off_to_give = holiday_off
                                attendance_records.append(EmployeeAttendance(user=user, company=company, employee=current_employee.employee, first_half=holiday_off_to_give, second_half=holiday_off_to_give, date=current_date, pay_multiplier=1.0))
                            total_expected_instances +=1


                        #If Current Date is Weekly or Extra off
                        elif current_date.strftime('%a').lower() == current_employee.weekly_off or (weekday_occurrence_in_month(date=current_date) == current_employee.extra_off):
                            #If it's weekly off bulk create the employees of the list so that when "paid_days_count_for_past_six_days" called it uses the updated Attendances
                            EmployeeAttendance.objects.bulk_create(attendance_records)
                            attendance_records.clear()

                            if employee_salary_detail.salary_mode.lower() == 'daily':
                                #It's daily wage employee so mark as absent since weekly off cannot be given to daily wage employees
                                attendance_records.append(EmployeeAttendance(user=user, company=company, employee=current_employee.employee, first_half=absent, second_half=absent, date=current_date, pay_multiplier=0))
                            else:
                                weekly_off_to_give = weekly_off_skip
                                if paid_days_count_for_past_six_days(user=user, company_id=company_id, attendance_date=current_date, employee=current_employee.employee) >= (weekly_off_holiday_off.min_days_for_weekly_off * 2):
                                    weekly_off_to_give = weekly_off
                                attendance_records.append(EmployeeAttendance(user=user, company=company, employee=current_employee.employee, first_half=weekly_off_to_give, second_half=weekly_off_to_give, date=current_date, pay_multiplier=1.0))
                            total_expected_instances +=1

                        
                        #It's not weekly off nor holiday off
                        else:
                            if not shift_found or (current_date < shift_from_date or current_date > shift_to_date):
                                employee_shift_on_particular_date_queryset = EmployeeShifts.objects.filter(company_id=company_id, user=user if user.role=="OWNER" else user.regular_to_owner.owner, employee=current_employee.employee, from_date__lte=current_date, to_date__gte=current_date)
                                if employee_shift_on_particular_date_queryset.exists():
                                    employee_shift_on_particular_date = employee_shift_on_particular_date_queryset.first()
                                    shift_from_date = employee_shift_on_particular_date.from_date
                                    shift_to_date = employee_shift_on_particular_date.to_date
                                    found_shift_beginning_time = employee_shift_on_particular_date.shift.beginning_time
                                    found_shift_end_time = employee_shift_on_particular_date.shift.end_time
                                    found_shift_late_grace = employee_shift_on_particular_date.shift.late_grace
                                    shift_found = True

                            attendance_records.append(EmployeeAttendance(user=user, company=company, employee=current_employee.employee, first_half=present_leave, second_half=present_leave, manual_in=self.generate_random_time(reference_time=found_shift_beginning_time, start_buffer=AUTO_SHIFT_BEGINNING_BUFFER_BEFORE, end_buffer=found_shift_late_grace), manual_out=self.generate_random_time(reference_time=found_shift_end_time, start_buffer=AUTO_SHIFT_ENDING_BUFFER_BEFORE, end_buffer=AUTO_SHIFT_ENDING_BUFFER_AFTER), date=current_date, pay_multiplier=1.0))
                            total_expected_instances +=1
                    current_date += relativedelta(days=1)
                
                EmployeeAttendance.objects.bulk_create(attendance_records)
                self._regenerate_months(
                    user=user,
                    company_id=company.id,
                    employee_ids=[current_employee.employee_id],
                    months=self._month_keys(from_date, to_date),
                )

    @staticmethod
    def _shift_datetimes(work_date, shift, payroll_tz):
        start = datetime.combine(work_date, shift.beginning_time, tzinfo=payroll_tz)
        end_date = work_date if shift.end_time > shift.beginning_time else work_date + timedelta(days=1)
        return start, datetime.combine(end_date, shift.end_time, tzinfo=payroll_tz)

    @staticmethod
    def _punch_datetime(work_date, punch, shift_start, shift_end, *, is_out):
        if punch is None:
            return None
        candidate = datetime.combine(work_date, punch, tzinfo=shift_start.tzinfo)
        if is_out and candidate < shift_start:
            candidate += timedelta(days=1)
        elif not is_out and candidate > shift_end:
            candidate -= timedelta(days=1)
        return candidate

    @classmethod
    def _raw_overtime_intervals(
        cls, *, work_date, shift, punch_in, punch_out, full_span_off_day, payroll_tz, source=None,
    ):
        if punch_in is None or punch_out is None or punch_out <= punch_in:
            return []
        shift_start, shift_end = cls._shift_datetimes(work_date, shift, payroll_tz)
        threshold = timedelta(minutes=shift.ot_begin_after)
        if full_span_off_day:
            if punch_out - punch_in <= threshold:
                return []
            interval = {
                'start_datetime': punch_in,
                'end_datetime': punch_out,
                'source': source or 'OFF_DAY_WORK',
                '_interval_kind': 'OFF_DAY_WORK',
            }
            if shift.lunch_beginning_time and shift.lunch_duration:
                lunch_start = datetime.combine(work_date, shift.lunch_beginning_time, tzinfo=payroll_tz)
                if lunch_start < shift_start:
                    lunch_start += timedelta(days=1)
                lunch_end = lunch_start + timedelta(minutes=shift.lunch_duration)
                exclusion_start = max(punch_in, lunch_start)
                exclusion_end = min(punch_out, lunch_end)
                if exclusion_end > exclusion_start and exclusion_end - exclusion_start < punch_out - punch_in:
                    interval['exclusions'] = [{
                        'start_datetime': exclusion_start,
                        'end_datetime': exclusion_end,
                        'exclusion_reason': 'MEAL_BREAK',
                    }]
            return [interval]
        intervals = []
        if shift_start - punch_in > threshold:
            intervals.append({
                'start_datetime': punch_in,
                'end_datetime': shift_start,
                'source': source or 'EARLY_ARRIVAL',
                '_interval_kind': 'EARLY_ARRIVAL',
            })
        if punch_out - shift_end > threshold:
            intervals.append({
                'start_datetime': shift_end,
                'end_datetime': punch_out,
                'source': source or 'LATE_DEPARTURE',
                '_interval_kind': 'LATE_DEPARTURE',
            })
        return intervals

    @staticmethod
    def _normalize_machine_badge(value):
        if pd.isna(value):
            return None
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value).strip()

    @classmethod
    def _machine_punch_index(cls, *, punches, users, from_day, to_day):
        punches = punches.copy()
        punches['CHECKTIME'] = pd.to_datetime(
            punches['CHECKTIME'], format='%m/%d/%y %H:%M:%S', errors='coerce',
        )
        coarse_start = datetime.combine(from_day - timedelta(days=1), datetime.min.time())
        coarse_end = datetime.combine(to_day + timedelta(days=2), datetime.min.time())
        punches = punches[
            (punches['CHECKTIME'] >= coarse_start) & (punches['CHECKTIME'] < coarse_end)
        ]
        punches_by_user = {
            user_id: pd.DatetimeIndex(group['CHECKTIME'].sort_values())
            for user_id, group in punches.groupby('USERID', sort=False)
        }
        user_by_badge = {}
        for badge, user_id in users[['Badgenumber', 'USERID']].itertuples(index=False, name=None):
            normalized = cls._normalize_machine_badge(badge)
            if normalized is not None:
                user_by_badge.setdefault(normalized, user_id)
        return user_by_badge, punches_by_user

    @staticmethod
    def _punch_window(punches, *, window_start, window_end):
        if punches is None or punches.empty:
            return None, None
        start = window_start.replace(tzinfo=None)
        end = window_end.replace(tzinfo=None)
        start_index = punches.searchsorted(start, side='left')
        end_index = punches.searchsorted(end, side='left')
        rows = punches[start_index:end_index]
        if rows.empty:
            return None, None
        return rows[0], rows[-1] if len(rows) > 1 else None

    @staticmethod
    def _shift_on_day(assignments, work_date):
        for assignment in assignments:
            if assignment.from_date <= work_date <= assignment.to_date:
                return assignment.shift
        return None

    @classmethod
    def _evaluate_machine_day(
        cls, *, professional, attendance, current_day, shift, raw_in, raw_out,
        payroll_tz, holidays, leaves, weekly_config, paid_halves,
    ):
        shift_start, shift_end = cls._shift_datetimes(current_day, shift, payroll_tz)
        machine_in = (
            datetime.combine(raw_in.date(), raw_in.time().replace(second=0, microsecond=0), tzinfo=payroll_tz)
            if raw_in is not None else None
        )
        machine_out = (
            datetime.combine(raw_out.date(), raw_out.time().replace(second=0, microsecond=0), tzinfo=payroll_tz)
            if raw_out is not None else None
        )
        if machine_in and machine_in > shift_end - timedelta(minutes=shift.half_day_minimum_minutes):
            if machine_out is None:
                machine_out = machine_in
            machine_in = None
        punch_in = (
            cls._punch_datetime(current_day, attendance.manual_in, shift_start, shift_end, is_out=False)
            if attendance and attendance.manual_in else machine_in
        )
        punch_out = (
            cls._punch_datetime(current_day, attendance.manual_out, shift_start, shift_end, is_out=True)
            if attendance and attendance.manual_out else machine_out
        )

        calendar_off_day = (
            current_day in holidays
            or current_day.strftime('%a').lower() == professional.weekly_off
            or weekday_occurrence_in_month(current_day) == professional.extra_off
        )
        salary_mode = professional.employee.employee_salary_detail.salary_mode.lower()
        late_minutes = 0
        if punch_in and (salary_mode == 'daily' or not calendar_off_day) and punch_in > shift_start + timedelta(minutes=shift.late_grace):
            late_minutes = int((punch_in - shift_start).total_seconds() // 60)

        first_half = second_half = leaves['A']
        if salary_mode != 'daily' and current_day in holidays:
            required = weekly_config.min_days_for_holiday_off * 2
            first_half = second_half = leaves['HD'] if paid_halves >= required else leaves['HD*']
        elif salary_mode != 'daily' and calendar_off_day:
            required = weekly_config.min_days_for_weekly_off * 2
            first_half = second_half = leaves['WO'] if paid_halves >= required else leaves['WO*']
        elif punch_in and punch_out:
            worked = punch_out - punch_in
            if salary_mode == 'daily' and calendar_off_day:
                worked = max(
                    min(punch_out, shift_end) - max(punch_in, shift_start),
                    timedelta(0),
                )
            if worked >= timedelta(minutes=shift.full_day_minimum_minutes):
                first_half, second_half = (
                    (leaves['P'], leaves['P'])
                    if late_minutes <= shift.max_late_allowed_min else (leaves['A'], leaves['P'])
                )
            elif worked >= timedelta(minutes=shift.half_day_minimum_minutes):
                first_half, second_half = (
                    (leaves['P'], leaves['A'])
                    if late_minutes <= shift.max_late_allowed_min else (leaves['A'], leaves['P'])
                )
        elif punch_in or punch_out:
            first_half = second_half = leaves['MS']

        return {
            'machine_in': machine_in.time() if machine_in else None,
            'machine_out': machine_out.time() if machine_out else None,
            'first_half': first_half,
            'second_half': second_half,
            'late_min': late_minutes if 0 < late_minutes <= shift.max_late_allowed_min else None,
            'pay_multiplier': 1 if first_half.paid and second_half.paid else .5 if first_half.paid or second_half.paid else 0,
            'intervals': cls._raw_overtime_intervals(
                work_date=current_day,
                shift=shift,
                punch_in=punch_in,
                punch_out=punch_out,
                full_span_off_day=calendar_off_day and salary_mode != 'daily',
                payroll_tz=payroll_tz,
            ),
        }

    @transaction.atomic
    def machine_attendance(self, from_date, to_date, company_id, user, all_employees_machine_attendance, mdb_database, employee):
        from .services.attendance_overtime import replace_many_attendance_overtime

        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
        WeeklyOffHolidayOff = apps.get_model('api', 'WeeklyOffHolidayOff')
        Holiday = apps.get_model('api', 'Holiday')
        LeaveGrade = apps.get_model('api', 'LeaveGrade')

        owner, company = self._validate_company(user=user, company_id=company_id)
        if user != owner:
            raise ValidationError({'user': 'Machine attendance may only be imported by the owner.'})
        try:
            payroll_tz = ZoneInfo(company.company_details.payroll_timezone)
        except (ObjectDoesNotExist, ZoneInfoNotFoundError, ValueError, TypeError) as exc:
            raise ValidationError({'company': 'Company requires a valid payroll timezone.'}) from exc
        from_day = from_date.date() if isinstance(from_date, datetime) else from_date
        to_day = to_date.date() if isinstance(to_date, datetime) else to_date
        if all_employees_machine_attendance:
            employee_queryset = EmployeeProfessionalDetail.objects.active_employees_between_dates(
                from_date=from_day, to_date=to_day, company_id=company.id, user=owner,
            )
        else:
            employee_queryset = EmployeeProfessionalDetail.objects.filter(
                user=owner, company=company, employee_id=employee,
            )
        employees = list(employee_queryset.select_related('employee__employee_salary_detail'))
        if not all_employees_machine_attendance and not employees:
            raise ValidationError({'employee': 'Employee must belong to the requested company.'})

        required_leave_names = {'P', 'MS', 'A', 'WO', 'WO*', 'HD', 'HD*'}
        leaves = {
            leave.name: leave
            for leave in LeaveGrade.objects.filter(
                company=company, user=owner, name__in=required_leave_names,
            )
        }
        missing_leave_names = required_leave_names - leaves.keys()
        if missing_leave_names:
            raise ValidationError({'leave_grades': f'Missing required leave grades: {", ".join(sorted(missing_leave_names))}.'})
        weekly_config = WeeklyOffHolidayOff.objects.get(user=owner, company=company)
        holidays = set(Holiday.objects.filter(user=owner, company=company, date__range=(from_day, to_day)).values_list('date', flat=True))
        employee_ids = [professional.employee_id for professional in employees]
        attendance_rows = list(
            self.filter(
                user=user,
                company=company,
                employee_id__in=employee_ids,
                date__range=(from_day - timedelta(days=6), to_day),
            ).select_related('first_half', 'second_half')
        )
        attendance_by_key = {
            (attendance.employee_id, attendance.date): attendance
            for attendance in attendance_rows
            if attendance.date >= from_day
        }
        paid_history = defaultdict(dict)
        for attendance in attendance_rows:
            paid_history[attendance.employee_id][attendance.date] = (
                int(attendance.first_half.paid) + int(attendance.second_half.paid)
            )
        shifts_by_employee = defaultdict(list)
        for assignment in EmployeeShifts.objects.filter(
            company=company,
            user=owner,
            employee_id__in=employee_ids,
            from_date__lte=to_day,
            to_date__gte=from_day,
        ).select_related('shift').order_by('employee_id', 'pk'):
            shifts_by_employee[assignment.employee_id].append(assignment)

        to_create = []
        to_update = []
        replacement_specs = []
        affected_employee_ids = set()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(mdb_database.read())
            temp_path = temp_file.name
        try:
            punches = mdb.read_table(temp_path, 'CHECKINOUT')
            users = mdb.read_table(temp_path, 'USERINFO')
            user_by_badge, punches_by_user = self._machine_punch_index(
                punches=punches, users=users, from_day=from_day, to_day=to_day,
            )

            for professional in employees:
                badge = self._normalize_machine_badge(professional.employee.attendance_card_no)
                machine_user_id = user_by_badge.get(badge)
                employee_punches = punches_by_user.get(machine_user_id) if machine_user_id is not None else None
                affected_employee_ids.add(professional.employee_id)
                current_day = from_day
                while current_day <= to_day:
                    if current_day < professional.date_of_joining or (professional.resigned and current_day > professional.resignation_date):
                        current_day += timedelta(days=1)
                        continue
                    key = (professional.employee_id, current_day)
                    attendance = attendance_by_key.get(key)
                    if attendance and (attendance.manual_mode or (attendance.manual_in is not None and attendance.manual_out is not None)):
                        current_day += timedelta(days=1)
                        continue
                    shift = self._shift_on_day(shifts_by_employee[professional.employee_id], current_day)
                    if shift is None:
                        raise ValidationError({'shift': f'No shift is configured for employee {professional.employee_id} on {current_day}.'})
                    shift_start, shift_end = self._shift_datetimes(current_day, shift, payroll_tz)
                    window_start = shift_start - timedelta(hours=3)
                    window_end = window_start + timedelta(days=1)
                    raw_in, raw_out = self._punch_window(
                        employee_punches, window_start=window_start, window_end=window_end,
                    )
                    paid_halves = sum(
                        paid_history[professional.employee_id].get(current_day - timedelta(days=days), 0)
                        for days in range(1, 7)
                    )
                    values = self._evaluate_machine_day(
                        professional=professional,
                        attendance=attendance,
                        current_day=current_day,
                        shift=shift,
                        raw_in=raw_in,
                        raw_out=raw_out,
                        payroll_tz=payroll_tz,
                        holidays=holidays,
                        leaves=leaves,
                        weekly_config=weekly_config,
                        paid_halves=paid_halves,
                    )

                    if attendance is None:
                        attendance = EmployeeAttendance(
                            user=user,
                            company=company,
                            employee=professional.employee,
                            date=current_day,
                            first_half=values['first_half'],
                            second_half=values['second_half'],
                        )
                        to_create.append(attendance)
                    else:
                        to_update.append(attendance)
                    for field in ('machine_in', 'machine_out', 'first_half', 'second_half', 'late_min', 'pay_multiplier'):
                        setattr(attendance, field, values[field])
                    attendance_by_key[key] = attendance
                    paid_history[professional.employee_id][current_day] = (
                        int(values['first_half'].paid) + int(values['second_half'].paid)
                    )
                    replacement_specs.append((key, values['intervals']))
                    current_day += timedelta(days=1)
        finally:
            os.unlink(temp_path)

        EmployeeAttendance.objects.bulk_create(
            to_create,
            batch_size=MACHINE_ATTENDANCE_CREATE_BATCH_SIZE,
        )
        EmployeeAttendance.objects.bulk_update(
            to_update,
            ['machine_in', 'machine_out', 'first_half', 'second_half', 'late_min', 'pay_multiplier'],
            batch_size=MACHINE_ATTENDANCE_UPDATE_BATCH_SIZE,
        )
        persisted_attendance = {
            (attendance.employee_id, attendance.date): attendance
            for attendance in self.filter(
                user=user,
                company=company,
                employee_id__in=affected_employee_ids,
                date__range=(from_day, to_day),
            ).select_related('employee', 'company', 'user')
        }
        replacements = [
            {
                'attendance': persisted_attendance[key],
                'intervals': intervals,
                'source': 'IMPORTED',
            }
            for key, intervals in replacement_specs
        ]
        replace_many_attendance_overtime(replacements=replacements, actor=user)
        detail_months = {
            (work_date.year, work_date.month)
            for work_date in apps.get_model('api', 'EmployeeAttendanceOvertimeDetail').objects.filter(
                attendance__in=[item['attendance'] for item in replacements]
            ).values_list('work_date', flat=True)
        }
        self._regenerate_months(
            user=user,
            company_id=company.id,
            employee_ids=affected_employee_ids,
            months=set(self._month_keys(from_day, to_day)) | detail_months,
        )
        return True, "Operation successful"
    

    @staticmethod
    def _cap_overtime_intervals(intervals, cap_minutes):
        remaining = max(0, int(cap_minutes))
        capped = []
        for interval in intervals:
            if remaining <= 0:
                break
            gross = int((interval['end_datetime'] - interval['start_datetime']).total_seconds() // 60)
            exclusion_minutes = sum(
                int((item['end_datetime'] - item['start_datetime']).total_seconds() // 60)
                for item in interval.get('exclusions', ())
            )
            eligible = gross - exclusion_minutes
            keep = min(eligible, remaining)
            item = dict(interval)
            if keep < eligible:
                if item.get('_interval_kind') == 'EARLY_ARRIVAL':
                    item['start_datetime'] = item['end_datetime'] - timedelta(minutes=keep)
                else:
                    candidate_end = item['start_datetime'] + timedelta(minutes=keep)
                    while True:
                        excluded = sum(
                            max(0, int((min(candidate_end, exclusion['end_datetime']) - max(item['start_datetime'], exclusion['start_datetime'])).total_seconds() // 60))
                            for exclusion in item.get('exclusions', ())
                        )
                        revised_end = min(
                            interval['end_datetime'],
                            item['start_datetime'] + timedelta(minutes=keep + excluded),
                        )
                        if revised_end == candidate_end:
                            break
                        candidate_end = revised_end
                    item['end_datetime'] = candidate_end
                exclusions = []
                for exclusion in item.get('exclusions', ()):
                    start = max(item['start_datetime'], exclusion['start_datetime'])
                    end = min(item['end_datetime'], exclusion['end_datetime'])
                    if end > start and end - start < item['end_datetime'] - item['start_datetime']:
                        exclusions.append({**exclusion, 'start_datetime': start, 'end_datetime': end})
                item['exclusions'] = exclusions
            capped.append(item)
            remaining -= keep
        return capped

    @transaction.atomic
    def transfer_attendance_from_owner_to_regular(self, month, year, company_id, user):
        from .services.attendance_overtime import replace_many_attendance_overtime

        EmployeeShifts = apps.get_model('api', 'EmployeeShifts')
        SubUserOvertimeSettings = apps.get_model('api', 'SubUserOvertimeSettings')
        SubUserMiscSettings = apps.get_model('api', 'SubUserMiscSettings')
        EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
        EmployeeAttendanceOvertimeDetail = apps.get_model('api', 'EmployeeAttendanceOvertimeDetail')

        owner, company = self._validate_company(user=user, company_id=company_id)
        if user != owner:
            raise ValidationError({'user': 'Attendance transfer requires the owner account.'})
        try:
            regular = owner.owner_to_regular.user
        except ObjectDoesNotExist as exc:
            raise ValidationError({'user': 'Owner is not linked to a regular attendance account.'}) from exc
        if regular.role != 'REGULAR' or regular.regular_to_owner.owner_id != owner.id:
            raise ValidationError({'user': 'Owner and regular account relationship is invalid.'})
        try:
            payroll_tz = ZoneInfo(company.company_details.payroll_timezone)
        except (ObjectDoesNotExist, ZoneInfoNotFoundError, ValueError, TypeError) as exc:
            raise ValidationError({'company': 'Company requires a valid payroll timezone.'}) from exc

        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])
        misc = SubUserMiscSettings.objects.filter(company=company, user=owner).first()
        owner_rows = self.filter(
            user=owner, company=company, date__range=(start_date, end_date), employee__visible=True,
        ).select_related(
            'employee__employee_professional_detail',
            'employee__employee_salary_detail',
        )
        existing = {
            (row.employee_id, row.date): row
            for row in self.filter(user=regular, company=company, date__range=(start_date, end_date))
        }
        replacements = []
        affected_employee_ids = set()
        for source_attendance in owner_rows:
            employee_shift = EmployeeShifts.objects.filter(
                user=owner, company=company, employee=source_attendance.employee,
                from_date__lte=source_attendance.date, to_date__gte=source_attendance.date,
            ).select_related('shift').first()
            if employee_shift is None:
                raise ValidationError({'shift': f'No shift is configured for employee {source_attendance.employee_id} on {source_attendance.date}.'})
            shift = employee_shift.shift
            shift_start, shift_end = self._shift_datetimes(source_attendance.date, shift, payroll_tz)
            punch_in = self._punch_datetime(
                source_attendance.date,
                source_attendance.manual_in or source_attendance.machine_in,
                shift_start,
                shift_end,
                is_out=False,
            )
            punch_out = self._punch_datetime(
                source_attendance.date,
                source_attendance.manual_out or source_attendance.machine_out,
                shift_start,
                shift_end,
                is_out=True,
            )
            professional = source_attendance.employee.employee_professional_detail
            calendar_off_day = (
                source_attendance.date.strftime('%a').lower() == professional.weekly_off
                or weekday_occurrence_in_month(source_attendance.date) == professional.extra_off
                or apps.get_model('api', 'Holiday').objects.filter(
                    user=owner, company=company, date=source_attendance.date,
                ).exists()
            )
            salary_mode = source_attendance.employee.employee_salary_detail.salary_mode.lower()
            full_span_off_day = calendar_off_day and salary_mode != 'daily'
            buffer_minutes = 3 if full_span_off_day else 10
            if punch_in and punch_in < shift_start - timedelta(minutes=buffer_minutes):
                punch_in = shift_start - timedelta(minutes=buffer_minutes)
            if punch_out and misc and misc.enable_female_max_punch_out and source_attendance.employee.gender == 'F':
                female_cap = datetime.combine(source_attendance.date, misc.max_female_punch_out, tzinfo=payroll_tz)
                if female_cap < shift_start:
                    female_cap += timedelta(days=1)
                punch_out = min(punch_out, female_cap)

            target = existing.get((source_attendance.employee_id, source_attendance.date))
            if target is None:
                target = EmployeeAttendance(
                    user=regular,
                    company=company,
                    employee=source_attendance.employee,
                    date=source_attendance.date,
                    first_half=source_attendance.first_half,
                    second_half=source_attendance.second_half,
                )
            target.machine_in = punch_in.time() if punch_in else None
            target.machine_out = punch_out.time() if punch_out else None
            target.manual_in = None
            target.manual_out = None
            target.first_half = source_attendance.first_half
            target.second_half = source_attendance.second_half
            target.late_min = source_attendance.late_min
            target.manual_mode = source_attendance.manual_mode
            target.pay_multiplier = source_attendance.pay_multiplier
            target.save()

            intervals = self._raw_overtime_intervals(
                work_date=source_attendance.date,
                shift=shift,
                punch_in=punch_in,
                punch_out=punch_out,
                full_span_off_day=full_span_off_day,
                payroll_tz=payroll_tz,
                source='TRANSFER',
            )
            overtime_setting = SubUserOvertimeSettings.objects.filter(
                user=owner, company=company, date=source_attendance.date,
            ).first()
            intervals = self._cap_overtime_intervals(
                intervals,
                overtime_setting.max_ot_hrs * 60 if overtime_setting else 0,
            )
            replacements.append({'attendance': target, 'intervals': intervals, 'source': 'TRANSFER'})
            affected_employee_ids.add(source_attendance.employee_id)

        replace_many_attendance_overtime(replacements=replacements, actor=regular)
        detail_months = {
            (work_date.year, work_date.month)
            for work_date in EmployeeAttendanceOvertimeDetail.objects.filter(
                attendance__in=[item['attendance'] for item in replacements]
            ).values_list('work_date', flat=True)
        }
        self._regenerate_months(
            user=regular,
            company_id=company.id,
            employee_ids=affected_employee_ids,
            months={(year, month)} | detail_months,
        )
        return True, "Operation successful"



class EmployeeSalaryPreparedManager(models.Manager):

    def bulk_prepare_salaries(self, month, year, company_id, user, employee_ids=None):
        from api.services.salary_preparation import bulk_prepare_salaries

        results = bulk_prepare_salaries(
            actor=user,
            company_id=company_id,
            year=year,
            month=month,
            employee_ids=employee_ids,
        )
        return True, f'{len(results)} salaries prepared'
