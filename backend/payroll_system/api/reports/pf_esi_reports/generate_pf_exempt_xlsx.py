
import pandas as pd
from django.http import HttpResponse
import io
from ...models import EarningsHead, EmployeeSalaryEarning, EarnedAmount, EmployeeSalaryPrepared
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar
from openpyxl.styles import Font, PatternFill

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
    rates = []
    basic_rates = []
    total_earned= []
    #esi_employer = []

    grand_total = {
        "rate": 0,
        "basic_rate": 0,
        "total_earned": 0
    }
    for employee_index, employee in enumerate(employees):
        serial.append(employee_index+1)
        paycode.append(employee.paycode)

        #Name
        employee_names.append(employee.name)
        
        #Father Husband Name
        employee_father_husband_names.append(employee.father_or_husband_name or '')

        #Employee Rate
        basic_earning_rate = None
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee, from_date__lte=date(request_data['year'], request_data['month'], 1), to_date__gte=date(request_data['year'], request_data['month'], 1))
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                print(head.name)
                if salary_for_particular_earning_head.exists():
                    if head.name=='Basic':
                        basic_earning_rate = salary_for_particular_earning_head.first().value
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass
        rates.append(total_earnings_rate if total_earnings_rate!= None else '') 
        basic_rates.append(basic_earning_rate if basic_earning_rate!=None else '')
        grand_total['rate'] += total_earnings_rate if total_earnings_rate!= None else 0
        grand_total['basic_rate'] += basic_earning_rate if basic_earning_rate!=None else 0

        #Total Earned
        total_earnings_amount = None
        try:
            prepared_salary = EmployeeSalaryPrepared.objects.filter(user=user, employee=employee, date=date(request_data['year'], request_data['month'], 1))
            if prepared_salary.exists():
                prepared_salary = prepared_salary.first()
                earned_amounts = prepared_salary.current_salary_earned_amounts.all()
                #Total Earned
                if earned_amounts and earned_amounts.exists():
                    total_earnings_amount = 0
                    for earned in earned_amounts:
                        total_earnings_amount += (earned.earned_amount)
                total_earnings_amount += prepared_salary.incentive_amount
                total_earnings_amount += prepared_salary.net_ot_amount_monthly
                # current_employee_dict['Earned Salary'] = total_earnings_amount
                # total_row['Earned Salary'] += total_earnings_amount
                # dept_total_dict['earned_salary'] += total_earnings_amount
        except:
            pass
        total_earned.append(total_earnings_amount if total_earnings_amount!=None else '')
        grand_total['total_earned'] += total_earnings_amount if total_earnings_amount!=None else 0




        company_pf_esi_setup = employee.company.pf_esi_setup_details

    serial.append('')
    paycode.append('')
    employee_names.append('')
    employee_father_husband_names.append('')
    rates.append(grand_total['rate'])
    basic_rates.append(grand_total['basic_rate'])
    total_earned.append(grand_total['total_earned'])
    #all_employee_paid_days.append(grand_total['all_employee_paid_days'])

    # Create a DataFrame from the names
    df = pd.DataFrame({' SN ': serial, 'Paycode': paycode, "Employee Name": employee_names, "Father's/Husband's Name": employee_father_husband_names, "Total Rate": rates, " Basic ": basic_rates, "Total Earned": total_earned})
    # Create an Excel file in memory
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # # Access the workbook and sheet
        # workbook = writer.book
        # worksheet = writer.sheets['Sheet1']
        #
        # # Adjust the width of all columns
        # for column in worksheet.columns:
        #     max_length = max(len(str(cell.value)) for cell in column) + 2  # Adding a little extra padding
        #     worksheet.column_dimensions[column[0].column_letter].width = max_length
        # Access the workbook and sheet
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
