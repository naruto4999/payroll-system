from django.db import models
# from api.models import EmployeePersonalDetail, EmployeeProfessionalDetail
from django.db.models import Q
from django.apps import apps
from datetime import datetime, timedelta, date



class ActiveEmployeeManager(models.Manager):
    def active_employees_between_dates(self, from_date, to_date, company_id, user):
        return self.filter(
            Q(resigned=False) | Q(resignation_date__gte=from_date),
            date_of_joining__lte=to_date,
            company_id=company_id,
            user=user
        )

class EmployeeAttendanceManager(models.Manager):
    def bulk_autofill(self, from_date, to_date, company_id, user):
        print(f'From Date: {from_date} To Date: {to_date}')
        EmployeeProfessionalDetail = apps.get_model('api', 'EmployeeProfessionalDetail')
        active_employees = EmployeeProfessionalDetail.objects.active_employees_between_dates(from_date, to_date, company_id=company_id, user=user)
        print(active_employees)

        # Calculate the range of dates
        if active_employees.exists():
            for current_employee in active_employees:
                 # Get the start date for the 6 days prior to from_date
                start_date = from_date - timedelta(days=6)

                # Filter existing EmployeeAttendance records for the date range
                EmployeeAttendance = apps.get_model('api', 'EmployeeAttendance')
                attendance_records = EmployeeAttendance.objects.filter(
                    # Q(first_half__name='P') | Q(second_half__name='P'),
                    Q(first_half__name__in=['P', 'OD']) | Q(second_half__name__in=['P', 'OD']),
                    employee=current_employee.employee,
                    date__range=[start_date, from_date - timedelta(days=1)],
                    company_id=company_id
                )
                #Counting number of present/on duty
                present_count = 0
                if attendance_records.exists():
                    for attendance in attendance_records:
                        present_count += 1 if attendance.first_half.name == "P" or attendance.first_half.name == "OD" else 0
                        present_count += 1 if attendance.second_half.name == "P" or attendance.second_half.name == "OD" else 0
                print(present_count)
                current_date = from_date
                while current_date <= to_date:
                    # print(f'Processing date: {current_date}')
                    current_date += timedelta(days=1)
