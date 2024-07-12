import pandas as pd
from django.http import HttpResponse
import io
from ...models import EarningsHead, EmployeeSalaryEarning, EarnedAmount
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar
from openpyxl.styles import Font, PatternFill

# def calculate_age(date_of_birth, reference_date):
#     # Calculate age based on the provided date_of_birth and reference_date
#     age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (date_of_birth.month, date_of_birth.day))
#     return age


def generate_esi_statement_xlsx(user, request_data, employees):
    # Create a DataFrame from the employees data
    serial = []
    paycode = []
    esi_numbers = []
    employee_names = []
    all_employee_paid_days = []
    esi_wages = []
    esi_employee = []
    esi_employer = []

    grand_total = {
        "all_employee_paid_days": 0,
        "esi_wages": 0,
        "esi_employee": 0,
        "esi_employer": 0,
    }
    for employee_index, employee in enumerate(employees):
        serial.append(employee_index+1)
        paycode.append(employee.paycode)

        #ESI Number
        esi_number = ''
        try: esi_number = employee.employee_pf_esi_detail.esi_number
        except: pass
        esi_numbers.append(esi_number)

        #Name
        employee_names.append(employee.name)

        #Paid Days
        paid_days = 0
        try:
            monthly_details = employee.monthly_attendance_details.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
            paid_days = monthly_details.paid_days_count/2
        except: 
            pass
        all_employee_paid_days.append(paid_days)  
        grand_total['all_employee_paid_days'] += paid_days


        company_pf_esi_setup = employee.company.pf_esi_setup_details
        #ESI
        salary_prepared = None
        total_earned_amount = 0
        try:
            esi_deducted = 0
            esiable_amount = 0
            salary_prepared = employee.salaries_prepared.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
            earned_amounts = EarnedAmount.objects.filter(user=user, salary_prepared = salary_prepared.id).order_by('earnings_head__id')
            for index, earned in enumerate(earned_amounts):
                total_earned_amount += earned.earned_amount
            total_earned_for_esi_deduction = total_earned_amount
            if employee.employee_pf_esi_detail.esi_on_ot:
                total_earned_for_esi_deduction += salary_prepared.net_ot_amount_monthly if salary_prepared.net_ot_amount_monthly else 0
            esiable_amount = min(company_pf_esi_setup.esi_employee_limit, total_earned_for_esi_deduction)
            esiable_amount_employer  = min(company_pf_esi_setup.esi_employer_limit, total_earned_for_esi_deduction)
            esi_deducted_employer = Decimal(esiable_amount_employer) * Decimal(company_pf_esi_setup.esi_employer_percentage) / Decimal(100)
            esi_deducted_employer =  esi_deducted_employer.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            esi_deducted = Decimal(esiable_amount) * Decimal(company_pf_esi_setup.esi_employee_percentage) / Decimal(100)
            esi_deducted = esi_deducted.quantize(Decimal('1.'), rounding=ROUND_CEILING)
        except:
            pass
        esi_wages.append(esiable_amount)
        esi_employee.append(int(esi_deducted))
        esi_employer.append(int(esi_deducted_employer))
        grand_total['esi_employee'] += int(esi_deducted)
        grand_total['esi_wages'] += esiable_amount
        grand_total['esi_employer'] += int(esi_deducted_employer)

    serial.append('')
    paycode.append('')
    esi_numbers.append('')
    employee_names.append('')
    all_employee_paid_days.append(grand_total['all_employee_paid_days'])
    esi_wages.append(grand_total['esi_wages'])
    esi_employee.append(grand_total['esi_employee'])
    esi_employer.append(grand_total['esi_employer'])    

    # Create a DataFrame from the names
    df = pd.DataFrame({'SN': serial, 'Paycode': paycode, "ESI Number": esi_numbers, "Employee Name": employee_names, "Paid Days": all_employee_paid_days, "ESI Wages": esi_wages, "ESI Employee": esi_employee, "ESI Employer": esi_employer})
    # Create an Excel file in memory
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')


        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Adjust the width of all columns
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column) + 2  # Adding a little extra padding
            worksheet.column_dimensions[column[0].column_letter].width = max_length

        # Make the last row bold and font color blue
        last_row = len(df) + 1
        font = Font(bold=True, color='0000FF')
        for cell in worksheet[last_row]:
            cell.font = font


    # Create a response with the Excel file content
    response = HttpResponse(content=excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pf_statement.xlsx"'

    # Close the buffer
    excel_buffer.close()

    # Return the response
    return response
