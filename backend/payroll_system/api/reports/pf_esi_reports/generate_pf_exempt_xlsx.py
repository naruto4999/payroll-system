
import pandas as pd
from django.http import HttpResponse
import io
from ...models import EarningsHead, EmployeeSalaryEarning, EarnedAmount
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar

# def calculate_age(date_of_birth, reference_date):
#     # Calculate age based on the provided date_of_birth and reference_date
#     age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (date_of_birth.month, date_of_birth.day))
#     return age


def generate_pf_exempt_xlsx(user, request_data, employees):
    # Create a DataFrame from the employees data
    serial = []
    paycode = []
    employee_names = []
    employee_father_husband_names = []
    all_employee_rate = []
    #esi_wages = []
    #esi_employee = []
    #esi_employer = []

    grand_total = {
        "all_employee_paid_days": 0,

    }
    for employee_index, employee in enumerate(employees):
        serial.append(employee_index+1)
        paycode.append(employee.paycode)

       #Name
        employee_names.append(employee.name)

        #Paid Days
        paid_days = 0
        try:
            monthly_details = employee.monthly_attendance_details.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
            paid_days = monthly_details.paid_days_count/2
        except: 
            pass
        
        #Employee Rate
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee, from_date__lte=date(request_data['year'], request_data['month'], 1), to_date__gte=date(request_data['year'], request_data['month'], 1))
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass



        company_pf_esi_setup = employee.company.pf_esi_setup_details

    serial.append('')
    paycode.append('')
    employee_names.append('')
    all_employee_paid_days.append(grand_total['all_employee_paid_days'])

    # Create a DataFrame from the names
    df = pd.DataFrame({'SN': serial, 'Paycode': paycode, "Employee Name": employee_names, "Paid Days": all_employee_paid_days})
    # Create an Excel file in memory
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Create a response with the Excel file content
    response = HttpResponse(content=excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pf_statement.xlsx"'

    # Close the buffer
    excel_buffer.close()

    # Return the response
    return response
