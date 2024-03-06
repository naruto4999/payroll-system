from django.http import HttpResponse
import io
from ...models import EmployeeSalaryEarning, EarnedAmount
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar

def calculate_age(date_of_birth, reference_date):
    # Calculate age based on the provided date_of_birth and reference_date
    age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (date_of_birth.month, date_of_birth.day))
    return age

def generate_pf_statement_txt(user, request_data, employees):
    # Create a string to hold the text content
    txt_content = ""

    # Iterate through employees and add information to the text content
    for employee_index, employee in enumerate(employees):
        #UAN
        uan_number = ''
        try: uan_number = employee.employee_pf_esi_detail.uan_number or ''
        except: pass
        txt_content += str(uan_number)+'#~#'

        #Name
        txt_content += employee.name+'#~#'

        #Wages
        total_earned = 0
        salary_prepared = employee.salaries_prepared.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
        earned_amounts = EarnedAmount.objects.filter(user=user, salary_prepared = salary_prepared.id)
        if earned_amounts.exists():
            for index, earned_amount in enumerate(earned_amounts):
                total_earned += earned_amount.earned_amount
        txt_content += str(total_earned)+'#~#'

        company_pf_esi_setup = employee.company.pf_esi_setup_details

        #EPF Wages
        # salary_prepared = None
        earned_basic_amount = None
        try: 
            pf_deducted = 0
            earned_basic_amount = earned_amounts.filter(earnings_head__name='Basic').first()
            if employee.employee_pf_esi_detail.pf_limit_ignore_employee == False:
                pfable_amount = min(company_pf_esi_setup.ac_1_epf_employee_limit, earned_basic_amount.earned_amount)
                txt_content += str(pfable_amount)+'#~#'
                pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                # Round the result
                pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

            elif employee.employee_pf_esi_detail.pf_limit_ignore_employee == True:
                pfable_amount = earned_basic_amount
                if employee.employee_pf_esi_detail.pf_limit_ignore_employee_value != None:
                    pfable_amount = min(employee.employee_pf_esi_detail.pf_limit_ignore_employee_value, earned_basic_amount.earned_amount)
                txt_content += str(pfable_amount)+'#~#'
                pf_deducted += (Decimal(company_pf_esi_setup.ac_1_epf_employee_percentage)/Decimal(100)) * Decimal(pfable_amount)
                # Round the result
                pf_deducted = pf_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        except:
            txt_content += '0'+'#~#'

        #EPS Wages
        eps_deducted = 0
        epsable_amount = 0
        if salary_prepared and earned_basic_amount and (employee.dob==None or calculate_age(employee.dob, date(request_data['year'], request_data['month'], 1)-relativedelta(days=1))<60):
            print(f'inside if')
            if employee.employee_pf_esi_detail.pf_limit_ignore_employer == False:
                epsable_amount = min(company_pf_esi_setup.ac_10_eps_employer_limit, earned_basic_amount.earned_amount)
                
                eps_deducted += (Decimal(company_pf_esi_setup.ac_10_eps_employer_percentage)/Decimal(100)) * Decimal(epsable_amount)
                # Round the result
                eps_deducted = eps_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            elif employee.employee_pf_esi_detail.pf_limit_ignore_employer == True:
                epsable_amount = earned_basic_amount
                if employee.employee_pf_esi_detail.pf_limit_ignore_employer_value != None:
                    epsable_amount = min(employee.employee_pf_esi_detail.pf_limit_ignore_employer_value, earned_basic_amount)
                
                eps_deducted += (Decimal(company_pf_esi_setup.ac_10_eps_employer_percentage)/Decimal(100)) * Decimal(epsable_amount)
                # Round the result
                eps_deducted = eps_deducted.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        txt_content += str(epsable_amount)+'#~#'

        #EDLI Wages
        if salary_prepared and earned_basic_amount:
            edliable_amount = min(company_pf_esi_setup.ac_1_epf_employer_limit, earned_basic_amount.earned_amount)
            txt_content += str(edliable_amount)+'#~#'
            #edli_employer.append(int(pf_deducted-eps_deducted))
        else:
            txt_content += '0'+'#~#'

        if pf_deducted:
            txt_content += str(pf_deducted)+'#~#'
        else:
            txt_content += '0'+'#~#'

        if eps_deducted:
            txt_content += str(eps_deducted)+'#~#'
        else:
            txt_content += '0'+'#~#'

        #EDLI Deducted
        txt_content += str((pf_deducted or 0)-(eps_deducted or 0))+'#~#'

        #NCP Days
        non_paid_days = None
        try:
            monthly_details = employee.monthly_attendance_details.filter(user=user, date=date(request_data['year'], request_data['month'], 1)).first()
            paid_days = monthly_details.paid_days_count
            num_days_in_month = calendar.monthrange(request_data['year'], request_data['month'])[1]
            non_paid_days = int((num_days_in_month - (paid_days/2))//1)
            txt_content += str(non_paid_days)+'#~#'
        except: 
            txt_content += '0'+'#~#'
        
        #REF ADV
        txt_content += '0'


        if employee_index != len(employees)-1:
            txt_content += '\n'

    return txt_content
