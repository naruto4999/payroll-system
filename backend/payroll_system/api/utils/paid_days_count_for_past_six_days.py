from ..models import EmployeeAttendance
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q


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
