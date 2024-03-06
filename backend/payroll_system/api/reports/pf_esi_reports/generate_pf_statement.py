import pandas as pd
from django.http import HttpResponse
import io
from ...models import EarningsHead, EmployeeSalaryEarning, EarnedAmount
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar

def calculate_age(date_of_birth, reference_date):
    # Calculate age based on the provided date_of_birth and reference_date
    age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (date_of_birth.month, date_of_birth.day))
    return age


def generate_pf_statement(user, request_data, employees):
    # Create a DataFrame from the employees data
    serial = []
    paycode = []
    uan_numbers = []
    employee_names = []
    gross_wages = []
    epf_wages = []
    eps_wages = []
    edli_wages=  []
    epf_employee = []
    epf_employer = []
    edli_employer = []
    ncp_days = []
    ref_adv = []

    grand_total = {
        "gross_wages": 0,
        "epf_wages": 0,
        "eps_wages": 0,
        "edli_wages": 0,
        "epf_employee": 0,
        "epf_employer": 0,
        "edli_employer": 0,
        "ncp_days": 0,
    }
    for employee_index, employee in enumerate(employees):
        serial.append(employee_index+1)
        paycode.append(employee.paycode)

        #UAN
        uan_number = ''
        try: uan_number = employee.employee_pf_esi_detail.uan_number
        except: pass
        uan_numbers.append(uan_number)

        #Name
        employee_names.append(employee.name)

        #Wages
        total_earned = 0
        salary_prepared = employee.salaries_prepared.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
        earned_amounts = EarnedAmount.objects.filter(user=user, salary_prepared = salary_prepared.id)
        if earned_amounts.exists():
            for index, earned_amount in enumerate(earned_amounts):
                total_earned += earned_amount.earned_amount
        gross_wages.append(total_earned)
        grand_total['gross_wages']+=total_earned

        company_pf_esi_setup = employee.company.pf_esi_setup_details
        
        #EPF Wages
        # salary_prepared = None
        earned_basic_amount = None
        try: 
            pf_deducted = 0
            earned_basic_amount = earned_amounts.filter(earnings_head__name='Basic').first()
            if employee.employee_pf_esi_detail.pf_limit_ignore_employee == False:
                pfable_amount = min(company_pf_esi_setup.ac_1_epf_employee_limit, earned_basic_amount.earned_amount)
                epf_wages.append(pfable_amount)
                grand_total['epf_wages']+= pfable_amount
                pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                # Round the result
                pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                epf_employee.append(int(pf_deducted))
                grand_total['epf_employee']+=int(pf_deducted)
            elif employee.employee_pf_esi_detail.pf_limit_ignore_employee == True:
                pfable_amount = earned_basic_amount
                if employee.employee_pf_esi_detail.pf_limit_ignore_employee_value != None:
                    pfable_amount = min(employee.employee_pf_esi_detail.pf_limit_ignore_employee_value, earned_basic_amount.earned_amount)
                epf_wages.append(pfable_amount)
                grand_total['epf_wages']+=int(pfable_amount)
                pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                # Round the result
                pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                epf_employee.append(int(pf_deducted))
                grand_total['epf_employee']+=int(pf_deducted)
        except:
            epf_wages.append(0)
            epf_employee.append(0)

        #EPS Wages
        # if employee.dob:
        #     # print(f"Comparision Date: {date(request_data['year'], request_data['month'], 1)-relativedelta(days=1)}")
        #     print(f"Age : {calculate_age(employee.dob, date(request_data['year'], request_data['month'], 1)-relativedelta(months=1))} Name: {employee.name}")
        eps_deducted = 0
        epsable_amount = 0
        print(f"Salary Prepared: {salary_prepared} Earned Basic Amt: {earned_basic_amount}, Employee DOB: {employee.dob} age: {calculate_age(employee.dob, date(request_data['year'], request_data['month'], 1)) if employee.dob else ''}")
        if salary_prepared and earned_basic_amount and (employee.dob==None or calculate_age(employee.dob, date(request_data['year'], request_data['month'], 1)-relativedelta(days=1))<60):
            print('Yes Give EPS')
            if employee.employee_pf_esi_detail.pf_limit_ignore_employer == False:
                epsable_amount = min(company_pf_esi_setup.ac_10_eps_employer_limit, earned_basic_amount.earned_amount)
                eps_deducted += (Decimal(company_pf_esi_setup.ac_10_eps_employer_percentage)/Decimal(100)) * Decimal(epsable_amount)
                # Round the result
                eps_deducted = eps_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                grand_total['epf_employer']+=int(eps_deducted)
            elif employee.employee_pf_esi_detail.pf_limit_ignore_employer == True:
                epsable_amount = earned_basic_amount
                if employee.employee_pf_esi_detail.pf_limit_ignore_employer_value != None:
                    epsable_amount = min(employee.employee_pf_esi_detail.pf_limit_ignore_employer_value, earned_basic_amount)
                eps_deducted += (Decimal(company_pf_esi_setup.ac_10_eps_employer_percentage)/Decimal(100)) * Decimal(epsable_amount)
                # Round the result
                eps_deducted = eps_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        # else:
        #     eps_wages.append(0)
        #     epf_employer.append(0)
        eps_wages.append(epsable_amount)
        grand_total['eps_wages']+=epsable_amount
        epf_employer.append(int(eps_deducted))

        #EDLI Wages
        if salary_prepared and earned_basic_amount:
            edliable_amount = min(company_pf_esi_setup.ac_1_epf_employer_limit, earned_basic_amount.earned_amount)
            edli_wages.append(edliable_amount)
            grand_total['edli_wages']+=edliable_amount
            edli_employer.append(int(pf_deducted-eps_deducted))
            grand_total['edli_employer']+=int(pf_deducted-eps_deducted)
        else:
            edli_wages.append(0)
            edli_employer.append(0)

        #NCP Days
        non_paid_days = None
        try:
            monthly_details = employee.monthly_attendance_details.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
            paid_days = monthly_details.paid_days_count
            num_days_in_month = calendar.monthrange(request_data['year'], request_data['month'])[1]
            non_paid_days = num_days_in_month - (paid_days/2)
            ncp_days.append(non_paid_days)
            grand_total['ncp_days']+=non_paid_days
        except: 
            ncp_days.append(0)        

        #REF ADV
        ref_adv.append(0)

    serial.append('')
    paycode.append('')
    uan_numbers.append('')
    employee_names.append('')
    gross_wages.append(grand_total['gross_wages'])
    epf_wages.append(grand_total['epf_wages'])
    eps_wages.append(grand_total['eps_wages'])
    edli_wages.append(grand_total['edli_wages'])
    epf_employee.append(grand_total['epf_employee'])
    epf_employer.append(grand_total['epf_employer'])
    edli_employer.append(grand_total['edli_employer'])
    ncp_days.append(grand_total['ncp_days'])
    ref_adv.append('')

        


        
    # Create a DataFrame from the names
    df = pd.DataFrame({'SN': serial, 'Paycode': paycode, 'UAN': uan_numbers, 'Employee Name': employee_names, 'Gross Wages': gross_wages, "EPF Wages": epf_wages, "EPS Wages": eps_wages, "EDLI Wages": edli_wages, "EPF Employee": epf_employee, "EPF Employer": epf_employer, "DIFF EPF-EPS": edli_employer, "NCP Days": ncp_days, "REF ADV": ref_adv})
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
