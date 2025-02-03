from ..models import EmployeeAttendance
from django.db.models import Q

def get_half_working_days_queryset(from_date, to_date, employee_id, company_id, user):
    attendance_records = EmployeeAttendance.objects.filter(
        Q(first_half__name='P') & Q(second_half__name='A'),
        Q(first_half__name='A') & Q(second_half__name='P'),
        employee_id=employee_id,
        date__gte=from_date,
        date__lte=to_date,
        company_id=company_id,
        user=user
    )
    return attendance_records

