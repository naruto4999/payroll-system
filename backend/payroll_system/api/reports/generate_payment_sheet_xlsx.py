import pandas as pd
from django.http import HttpResponse
import io
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar
from api.models import EarningsHead,EmployeeSalaryEarning
from openpyxl.styles import Font, PatternFill


# def calculate_age(date_of_birth, reference_date):
#     # Calculate age based on the provided date_of_birth and reference_date
#     age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (date_of_birth.month, date_of_birth.day))
#     return age


def generate_payment_sheet_xlsx(request_data, employee_salaries):
    employees_data = []
    total_row = {
    'S/N': '',
    'ACN': '',
    'Employee Name': '',
    'Father/Husband Name': '',
    'Designation': '',
    'Salary Rate': 0,
    'PD': 0,
    'Earned Salary': 0,
    'OT Hrs': 0,
    'OT Amount': 0,
    'Total Earned': 0,
    'Advance': 0,
    'EPF': 0,
    'ESI': 0,
    'TDS': 0,
    'Total Deduction': 0,
    'Net Payable': 0
}
    for salary_index, employee_salary in enumerate(employee_salaries):
        current_employee_dict = {
            'S/N': salary_index+1,
            'ACN': employee_salary.employee.attendance_card_no,
            'Employee Name': employee_salary.employee.name,
            'Father/Husband Name': employee_salary.employee.father_or_husband_name,
            'Designation': '',
            'Salary Rate': 0,
            'PD': 0,
            'Earned Salary': 0,
            'OT Hrs': 0,
            'OT Amount': 0,
            'Total Earned': 0,
            'Advance': 0,
            'EPF': 0,
            'ESI': 0,
            'TDS': 0,
            'Total Deduction': 0,
            'Net Payable': 0
            }
        #Designation
        try: current_employee_dict['Designation'] = employee_salary.employee.employee_professional_detail.designation.name
        except: pass

        #Salary Rate
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=employee_salary.company, user=employee_salary.user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee_salary.employee, from_date__lte=employee_salary.date, to_date__gte=employee_salary.date)
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
            current_employee_dict['Salary Rate'] = total_earnings_rate
            total_row['Salary Rate'] += total_earnings_rate
        except: 
            pass

        #Paid Days
        employee_monthly_attendance_details = None
        try: 
            employee_monthly_attendance_details = employee_salary.employee.monthly_attendance_details.filter(date=employee_salary.date).first()
            current_employee_dict['PD']= employee_monthly_attendance_details.paid_days_count/2
            total_row['PD'] += employee_monthly_attendance_details.paid_days_count/2
        except: pass        

        #Earned Salary
        try:
            earned_amounts = employee_salary.current_salary_earned_amounts.all()
            #Total Earned
            if earned_amounts and earned_amounts.exists():
                total_earnings_amount = 0
                for earned in earned_amounts:
                    total_earnings_amount += (earned.earned_amount)
            total_earnings_amount += employee_salary.incentive_amount
            current_employee_dict['Earned Salary'] = total_earnings_amount
            total_row['Earned Salary'] += total_earnings_amount
        except: pass

        #OT
        ot_hrs = employee_salary.net_ot_minutes_monthly/60
        current_employee_dict['OT Hrs'] = ot_hrs
        total_row['OT Hrs'] += ot_hrs
        
        #OT Amt
        ot_amt = employee_salary.net_ot_amount_monthly
        current_employee_dict['OT Amount'] = ot_amt
        total_row['OT Amount'] += ot_amt

        #Total Earned
        if total_earnings_amount:
            total_earned = total_earnings_amount
            if ot_amt:
                total_earned += ot_amt
            current_employee_dict['Total Earned'] = total_earned
            total_row['Total Earned'] += total_earned

        #Advance
        try:
            advance = employee_salary.advance_deducted
            current_employee_dict['Advance'] = advance
            total_row['Advance'] += advance
        except: pass

        #EPF
        try:
            pf = employee_salary.pf_deducted
            current_employee_dict['EPF'] = pf
            total_row['EPF'] += pf
        except: pass

        #ESI
        try:
            esi = employee_salary.esi_deducted
            current_employee_dict['ESI'] = esi
            total_row['ESI'] += esi
        except: pass

        #TDS
        try:
            tds = employee_salary.tds_deducted
            current_employee_dict['TDS'] = tds
            total_row['TDS'] += tds
        except: pass

        #Total Deductions
        try:
            total_deductions = advance + pf + esi + tds
            current_employee_dict['Total Deduction'] = total_deductions
            total_row['Total Deduction'] += total_deductions
        except: pass

        #Net Payable
        try:
            net_payable = total_earned - total_deductions
            current_employee_dict['Net Payable'] = net_payable
            total_row['Net Payable'] += net_payable
        except: pass

        employees_data.append(current_employee_dict)
            
    employees_data.append(total_row)

    df = pd.DataFrame(employees_data)

    # Create a BytesIO buffer
    excel_buffer = io.BytesIO()

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Get the worksheet
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Get the last row number
        last_row = len(df) + 1

        # Apply bold font and blue fill color to the last row
        for col in range(1, len(df.columns) + 1):
            cell = worksheet.cell(row=last_row, column=col)
            cell.font = Font(bold=True, color='FF0000FF')  # Set the font color to blue

    # Create a response with the Excel file content
    response = HttpResponse(content=excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pf_statement.xlsx"'

    # Close the buffer
    excel_buffer.close()

    # Return the response
    return response