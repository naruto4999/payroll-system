from fpdf import FPDF
from ..models import EmployeeSalaryPrepared, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, LeaveGrade, EmployeeGenerativeLeaveRecord, EmployeeMonthlyAttendanceDetails, CompanyDetails, EarningsHead, EmployeeSalaryEarning, EarnedAmount, PfEsiSetup
from datetime import date
from django.db.models import Case, When, Value, CharField
import math
from .pdf_utils.custom_fpdf import CustomFPDF

width_of_columns = {
    "serial": 7,
    "acn": 12,
    "employee_name": 30,
    "father_husband_name": 30,
    "designation": 23,
    "salary_rate": 11,
    "paid_days": 7,
    "earned_salary": 11,
    "incentive": 11,
    "ot_hrs": 11,
    "ot_amount": 11,
    "total_earnings": 11,
    "advance": 11,
    "epf": 9,
    "esi": 7,
    "lwf": 7,
    "others": 10,
    "tds": 10,
    "total_deductions": 11,
    "net_payable": 12,
    "bank_payment": 11,
    "other_payment": 11,
    "signature": 10 
}

class CustomFPDF(CustomFPDF):
        def __init__(self, my_date, company_name, company_address, company_pf_esi_setup, *args, **kwargs):
            self.my_date = my_date
            self.company_name = company_name
            self.company_address = company_address
            self.company_pf_esi_setup = company_pf_esi_setup
            super().__init__(*args, **kwargs)

        def header(self):
            # Set Font for Company and add Company name
            self.set_font('Helvetica', 'B', 15)
            self.cell(0, 8, self.company_name, align="L", new_x="RIGHT", new_y='TOP', border=0)
            self.set_font("Helvetica", size=7, style="")
            self.cell(0, 8, 'Page %s' % self.page_no(), align="R", new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Address and add Address
            self.set_font('Arial', 'B', 8)
            self.cell(0, 4, self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Month and Year and add Month and Year
            self.cell(0, 6, self.my_date.strftime("Payment Sheet (As per Compliance) for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

            initial_coordinates = {"x": self.get_x(), "y": self.get_y()}

            self.set_font("Helvetica", size=7, style="B")
            self.set_line_width(0.4)

            #Serial
            self.cell(w=width_of_columns['serial'], h=10, text=f'S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Card No
            coordinates_before_acn = {"x": self.get_x(), "y": self.get_y()}
            self.cell(w=width_of_columns['acn'], h=10/3, text=f'ACN', align="C", new_x="LEFT", new_y='NEXT', border='LRT')
            self.set_font("Helvetica", size=4.5, style="I")
            self.multi_cell(w=width_of_columns['acn'], h=10/3, text=f'(Attendance Card No.)', align="C", new_x="RIGHT", new_y='TOP', border='LRB')
            self.set_xy(x=self.get_x(), y=coordinates_before_acn['y'])
            self.set_font("Helvetica", size=7, style="B")
            
            #Employee Name
            self.cell(w=width_of_columns['employee_name'], h=10, text=f'Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Father Husband Name
            self.cell(w=width_of_columns['father_husband_name'], h=10, text=f'F/H Name', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Designation
            self.cell(w=width_of_columns['designation'], h=10, text=f'Designation', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Salary Rate
            self.multi_cell(w=width_of_columns['salary_rate'], h=10/2, text=f'Salary Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Paid Days
            # self.cell(w=width_of_columns['paid_days'], h=10, text=f'PD', align="C", new_x="RIGHT", new_y='TOP', border=1)
            coordinates_before_paid_days = {"x": self.get_x(), "y": self.get_y()}
            self.cell(w=width_of_columns['paid_days'], h=10/3, text=f'PD', align="C", new_x="LEFT", new_y='NEXT', border='LRT')
            self.set_font("Helvetica", size=4.5, style="I")
            self.multi_cell(w=width_of_columns['paid_days'], h=10/3, text=f'(Paid Days)', align="C", new_x="RIGHT", new_y='TOP', border='LRB')
            self.set_xy(x=self.get_x(), y=coordinates_before_paid_days['y'])
            self.set_font("Helvetica", size=7, style="B")
            
            #Earned Salary
            coordinates_before_earned_salary = {"x": self.get_x(), "y": self.get_y()}
            self.multi_cell(w=width_of_columns['earned_salary'], h=10/3, text=f'Earned Salary', align="C", new_x="LEFT", new_y='NEXT', border='LRT')
            self.set_font("Helvetica", size=4.5, style="I")
            self.cell(w=width_of_columns['earned_salary'], h=10/3, text=f'*incl. of Arrear', align="C", new_x="RIGHT", new_y='TOP', border='LRB')
            self.set_xy(x=self.get_x(), y=coordinates_before_earned_salary['y'])
            self.set_font("Helvetica", size=7, style="B")

            #Incentive
            self.cell(w=width_of_columns['incentive'], h=10, text=f"Incen.", align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #OT Hrs
            self.cell(w=width_of_columns['ot_hrs'], h=10, text=f'OT Hrs', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #OT Amt
            self.cell(w=width_of_columns['ot_amount'], h=10, text=f'OT Amt', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Total Earnings
            self.multi_cell(w=width_of_columns['total_earnings'], h=10/2, text=f'Total Earned', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Advance
            self.cell(w=width_of_columns['advance'], h=10, text=f'Advance', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #EPF
            self.cell(w=width_of_columns['epf'], h=10, text=f'EPF', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #ESI
            self.cell(w=width_of_columns['esi'] if self.company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=10, text=f'ESI', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #LWF
            if self.company_pf_esi_setup.enable_labour_welfare_fund:
                self.cell(w=width_of_columns['lwf'], h=10, text=f'LWF', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Others
            self.cell(w=width_of_columns['others'], h=10, text=f'Others', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #TDS
            self.cell(w=width_of_columns['tds'], h=10, text=f'TDS', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Total Deductions
            coordinates_before_total_deductions = {"x": self.get_x(), "y": self.get_y()}
            self.cell(w=width_of_columns['total_deductions'], h=10/3, text=f'T. Ded.', align="C", new_x="LEFT", new_y='NEXT', border='LRT')
            self.set_font("Helvetica", size=4.5, style="I")
            self.multi_cell(w=width_of_columns['total_deductions'], h=10/3, text=f'(Total Deductions)', align="C", new_x="RIGHT", new_y='TOP', border='LRB')
            self.set_xy(x=self.get_x(), y=coordinates_before_total_deductions['y'])
            self.set_font("Helvetica", size=7, style="B")

            
            #Net Payable
            self.multi_cell(w=width_of_columns['net_payable'], h=10/2, text=f'Net Payable', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Bank Payment
            self.multi_cell(w=width_of_columns['bank_payment'], h=10/2, text=f'Bank Pay.', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Other Payment
            self.multi_cell(w=width_of_columns['other_payment'], h=10/2, text=f'Other Pay.', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Signature
            self.cell(w=width_of_columns['signature'], h=10, text=f'Signat.', align="C", new_x="LMARGIN", new_y='NEXT', border=1)

def generate_payment_sheet_as_per_compliance(user, request_data, employees):

    left_margin = 6
    right_margin = 7
    bottom_margin = 3
    top_margin = 6

    default_cell_height = 5
    default_heading_height = 10
    default_dept_heading_height = 8

    company_pf_esi_setup = PfEsiSetup.objects.get(company=request_data['company'])

    grand_total_dict = {
        "earned_salary" : 0,
        "incentive":0,
        "ot_amt": 0,
        "total_earnings": 0,
        "total_advance": 0,
        "total_pf": 0,
        "total_esi": 0,
        "total_lwf": 0,
        "total_others": 0,
        "total_tds": 0,
        "total_deductions": 0,
        "net_payable": 0,
        "bank_payment": 0,
        "other_payment": 0

    }

    dept_total_dict = {
        "earned_salary" : 0,
        "incentive": 0,
        "ot_amt": 0,
        "total_earnings": 0,
        "total_advance": 0,
        "total_pf": 0,
        "total_esi": 0,
        "total_lwf": 0,
        "total_others": 0,
        "total_tds": 0,
        "total_deductions": 0,
        "net_payable": 0,
        "bank_payment": 0,
        "other_payment": 0
    }

    #Getting Company
    company = employees[0].company
    company_address = ''
    try: company_address = company.company_details.address
    except: pass
    payment_sheet_as_per_compliance = CustomFPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=company.name,company_address=company_address,company_pf_esi_setup=company_pf_esi_setup, orientation="L", unit="mm", format="A4")

    #Page settings
    payment_sheet_as_per_compliance.set_margins(left=left_margin, top=top_margin, right=right_margin)
    payment_sheet_as_per_compliance.add_page()
    payment_sheet_as_per_compliance.set_auto_page_break(auto=True, margin = bottom_margin)

    payment_sheet_as_per_compliance.set_font("Helvetica", size=6.5, style="")
    for index, employee in enumerate(employees):
        salary = employee.owner_salary[0]
        regular_account_salary = employee.regular_account_salary[0] if len(employee.regular_account_salary)>0 else None
        if request_data['filters']['group_by'] != 'none':
            try:
                if index == 0 or employee.employee_professional_detail.department.name != employees[index-1].employee_professional_detail.department.name:
                    payment_sheet_as_per_compliance.set_font("Helvetica", size=9, style="B")
                    payment_sheet_as_per_compliance.cell(w=0, h=default_cell_height, text=f'{salary.employee.employee_professional_detail.department.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    payment_sheet_as_per_compliance.set_font("Helvetica", size=6.5, style="")
                    dept_total_dict = {
                    "earned_salary" : 0,
                    "incentive": 0,
                    "ot_amt": 0,
                    "total_earnings": 0,
                    "total_advance": 0,
                    "total_pf": 0,
                    "total_esi": 0,
                    "total_lwf": 0,
                    "total_others": 0,
                    "total_tds": 0,
                    "total_deductions": 0,
                    "net_payable": 0,
                    "bank_payment": 0,
                    "other_payment": 0
                }
            except:
                pass
        #Serial
        payment_sheet_as_per_compliance.cell(w=width_of_columns['serial'], h=default_cell_height, text=f'{index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #ACN
        payment_sheet_as_per_compliance.multi_cell_with_limit(w=width_of_columns['acn'], h=default_cell_height, text=f'{employee.attendance_card_no}', min_lines=1, max_lines=1, border_each_line=False, align="R", new_x="RIGHT", new_y='TOP', border=1)
        
        #Employee Name
        payment_sheet_as_per_compliance.multi_cell_with_limit(w=width_of_columns['employee_name'], h=default_cell_height, text=f'{employee.name}', min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Father Husband Name
        payment_sheet_as_per_compliance.multi_cell_with_limit(w=width_of_columns['father_husband_name'], h=default_cell_height, text=f'{employee.father_or_husband_name or ""}', min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = None
        try: designation = employee.employee_professional_detail.designation.name
        except: pass
        payment_sheet_as_per_compliance.multi_cell_with_limit(w=width_of_columns['designation'], h=default_cell_height, text=f"{designation if designation else ''}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Salary Rate
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=employee.company, user=user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee, from_date__lte=salary.date, to_date__gte=salary.date)
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass
        payment_sheet_as_per_compliance.cell(w=width_of_columns['salary_rate'], h=default_cell_height, text=f"{total_earnings_rate if total_earnings_rate!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Paid Days
        paid_days = 0
        paid_days_str = ''
        employee_monthly_attendance_details = None
        try: 
            employee_monthly_attendance_details = employee.monthly_attendance_details.filter(date=salary.date, user=user).first()
            paid_days += employee_monthly_attendance_details.paid_days_count
            paid_days_str =  paid_days/2
        except: 
            pass
        payment_sheet_as_per_compliance.cell(w=width_of_columns['paid_days'], h=default_cell_height, text=f'{paid_days_str}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Earned Salary
        total_earnings_amount = None
        try:
            earned_amounts = salary.current_salary_earned_amounts.all()

            #Total Earned
            if earned_amounts and earned_amounts.exists():
                total_earnings_amount = 0
                for earned in earned_amounts:
                    total_earnings_amount += (earned.earned_amount)
        except: 
            pass
        if total_earnings_amount:
            grand_total_dict['earned_salary'] += total_earnings_amount
            dept_total_dict['earned_salary'] += total_earnings_amount
        payment_sheet_as_per_compliance.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{total_earnings_amount if total_earnings_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Incentive
        if salary.incentive_amount:
            grand_total_dict['incentive'] += salary.incentive_amount
            dept_total_dict['incentive'] +=salary.incentive_amount
        payment_sheet_as_per_compliance.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{salary.incentive_amount if salary.incentive_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT
        ot_hrs = None
        if employee_monthly_attendance_details:
            ot_hrs = salary.net_ot_minutes_monthly/60
        payment_sheet_as_per_compliance.cell(w=width_of_columns['ot_hrs'], h=default_cell_height, text=f"{ot_hrs if ot_hrs!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)


        #OT Amt
        ot_amt = None
        if employee_monthly_attendance_details:
            ot_amt = salary.net_ot_amount_monthly
        if ot_amt:
            grand_total_dict['ot_amt'] += ot_amt
            dept_total_dict['ot_amt'] += ot_amt
        payment_sheet_as_per_compliance.cell(w=width_of_columns['ot_amount'], h=default_cell_height, text=f"{ot_amt if ot_amt!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)


        #Total Earned
        total_earned = None
        if total_earnings_amount:
            total_earned = total_earnings_amount
            if ot_amt:
                total_earned += ot_amt
            if salary.incentive_amount:
                total_earned += salary.incentive_amount
        if total_earned:
            grand_total_dict['total_earnings'] += total_earned
            dept_total_dict['total_earnings'] += total_earned
        payment_sheet_as_per_compliance.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{total_earned if total_earned!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        """
        Deductions start form Here
        """
        current_employee_total_deductions_regular_account = 0 if regular_account_salary!=None else None
        #Advance: This is to be taken from main account because employees who are on offroll their advance won't be considered since they won't be in subuser account.
        advance_deducted = None
        try:
            if salary!=None:
                advance_deducted = salary.advance_deducted
                current_employee_total_deductions_regular_account += advance_deducted
                grand_total_dict['total_advance'] +=  advance_deducted
                dept_total_dict['total_advance'] +=  advance_deducted
        except Exception as e: 
             print(f"Error occurred in generate_payment_sheet_as_per_compliance in Advance: {str(e)}")
        payment_sheet_as_per_compliance.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{advance_deducted if advance_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #EPF
        pf_and_vpf_deducted = None
        try:
            if regular_account_salary!=None:
                pf_and_vpf_deducted=0
                if regular_account_salary.pf_deducted:
                    pf_and_vpf_deducted += regular_account_salary.pf_deducted
                    grand_total_dict['total_pf'] += regular_account_salary.pf_deducted
                    dept_total_dict['total_pf'] += regular_account_salary.pf_deducted
                if regular_account_salary.vpf_deducted:
                    pf_and_vpf_deducted += regular_account_salary.vpf_deducted
                    grand_total_dict['total_pf'] += regular_account_salary.vpf_deducted
                    dept_total_dict['total_pf'] += regular_account_salary.vpf_deducted
                current_employee_total_deductions_regular_account += pf_and_vpf_deducted
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in EPF: {str(e)}")


        payment_sheet_as_per_compliance.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{pf_and_vpf_deducted if pf_and_vpf_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #ESI
        esi_deducted = None
        try:
            if regular_account_salary!= None and regular_account_salary.esi_deducted!=None:
                esi_deducted =  regular_account_salary.esi_deducted
                grand_total_dict['total_esi'] += regular_account_salary.esi_deducted
                dept_total_dict['total_esi'] += regular_account_salary.esi_deducted
                current_employee_total_deductions_regular_account += esi_deducted
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in ESI: {str(e)}")

        payment_sheet_as_per_compliance.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{esi_deducted if esi_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #LWF
        if company_pf_esi_setup.enable_labour_welfare_fund:
            lwf_deducted = None
            try:
                if regular_account_salary!=None and regular_account_salary.labour_welfare_fund_deducted!=None:
                    lwf_deducted = regular_account_salary.labour_welfare_fund_deducted
                    current_employee_total_deductions_regular_account += lwf_deducted
                    grand_total_dict['total_lwf'] += regular_account_salary.labour_welfare_fund_deducted
                    dept_total_dict['total_lwf'] += regular_account_salary.labour_welfare_fund_deducted
            except Exception as e: 
                print(f"Error occurred in generate_payment_sheet_as_per_compliance in LWF: {str(e)}")

            payment_sheet_as_per_compliance.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{lwf_deducted if lwf_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Others
        others_deducted = None
        try:
            if regular_account_salary!=None and regular_account_salary.others_deducted!=None:
                others_deducted = regular_account_salary.others_deducted
                current_employee_total_deductions_regular_account += others_deducted
                grand_total_dict['total_others'] += regular_account_salary.others_deducted
                dept_total_dict['total_others'] += regular_account_salary.others_deducted
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in Others: {str(e)}")
        payment_sheet_as_per_compliance.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{others_deducted if others_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #TDS
        tds_deducted = None
        try:
            if regular_account_salary!=None and regular_account_salary.tds_deducted!=None:
                tds_deducted = regular_account_salary.tds_deducted
                current_employee_total_deductions_regular_account += tds_deducted
                grand_total_dict['total_tds'] += regular_account_salary.tds_deducted
                dept_total_dict['total_tds'] += regular_account_salary.tds_deducteda
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in TDS: {str(e)}")

        payment_sheet_as_per_compliance.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{tds_deducted if tds_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Deductions
        # total_deductions = None
        # try:
        #     #total_deductions = salary.pf_deducted+esi_deducted_based_on_overtime_filter+salary.vpf_deducted+salary.advance_deducted+salary.tds_deducted+salary.others_deducted
        #     total_deductions = salary.advance_deducted + salary.pf_deducted + salary.esi_deducted + salary.tds_deducted + salary.others_deducted + salary.vpf_deducted
        #     if company_pf_esi_setup.enable_labour_welfare_fund:
        #         total_deductions += salary.labour_welfare_fund_deducted
        # except:
        #     pass
        if current_employee_total_deductions_regular_account!=None:
            grand_total_dict['total_deductions'] += current_employee_total_deductions_regular_account 
            dept_total_dict['total_deductions'] +=  current_employee_total_deductions_regular_account
        payment_sheet_as_per_compliance.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{current_employee_total_deductions_regular_account if current_employee_total_deductions_regular_account!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Net Payable
        net_payable = None
        try: #Total earned of main account - total deductions of 2nd account
            net_payable = total_earned - current_employee_total_deductions_regular_account 
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in Net Payable: {str(e)}")
        if net_payable:
            grand_total_dict['net_payable'] +=  net_payable
            dept_total_dict['net_payable'] +=  net_payable
        payment_sheet_as_per_compliance.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{net_payable if net_payable!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Bank Payment
        bank_payment = None
        try:
            if regular_account_salary!=None:
                current_employee_total_earned_regular_account = 0
                total_earnings_amount = None
                earned_amounts = regular_account_salary.current_salary_earned_amounts.all()
                #Total Earned
                if earned_amounts and earned_amounts.exists():
                    total_earnings_amount = 0
                    for earned in earned_amounts:
                        total_earnings_amount += (earned.earned_amount)
                if total_earnings_amount:
                    current_employee_total_earned_regular_account = total_earnings_amount
                    if regular_account_salary.net_ot_amount_monthly:
                        current_employee_total_earned_regular_account += regular_account_salary.net_ot_amount_monthly 
                    if regular_account_salary.incentive_amount:
                        current_employee_total_earned_regular_account += regular_account_salary.incentive_amount
                bank_payment = current_employee_total_earned_regular_account - current_employee_total_deductions_regular_account
                grand_total_dict['bank_payment'] += bank_payment
                dept_total_dict['bank_payment'] += bank_payment
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in bank payment: {str(e)}")
        payment_sheet_as_per_compliance.cell(w=width_of_columns['bank_payment'], h=default_cell_height, text=f"{bank_payment if bank_payment!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)


        #Other Payment
        other_payment = None
        try:
            other_payment = net_payable - bank_payment
            grand_total_dict['other_payment'] += other_payment
            dept_total_dict['other_payment'] += other_payment
        except Exception as e: 
            print(f"Error occurred in generate_payment_sheet_as_per_compliance in other_payment: {str(e)}")
        payment_sheet_as_per_compliance.cell(w=width_of_columns['bank_payment'], h=default_cell_height, text=f"{other_payment if other_payment!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Signature
        payment_sheet_as_per_compliance.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"", align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        print(f"Incentive Seq: {dept_total_dict['incentive']}")



        #Dept Total if applicable
        if request_data['filters']['group_by'] != 'none':
            if (index != len(employees)-1 and salary.employee.employee_professional_detail.department != employees[index+1].employee_professional_detail.department) or (index == len(employees)-1 and employee.employee_professional_detail.department):
                payment_sheet_as_per_compliance.set_line_width(0.4)
                payment_sheet_as_per_compliance.set_font("Helvetica", size=6.5, style="B")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Department Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{dept_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{dept_total_dict['incentive']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{dept_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{dept_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{dept_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{dept_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{dept_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                if company_pf_esi_setup.enable_labour_welfare_fund==True:
                    payment_sheet_as_per_compliance.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{dept_total_dict['total_lwf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{dept_total_dict['total_others']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{dept_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{dept_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{dept_total_dict['net_payable']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['bank_payment'], h=default_cell_height, text=f"{dept_total_dict['bank_payment']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet_as_per_compliance.cell(w=width_of_columns['other_payment'], h=default_cell_height, text=f"{dept_total_dict['other_payment']}", align="R", new_x="LMARGIN", new_y='NEXT', border="TB")
                payment_sheet_as_per_compliance.set_font("Helvetica", size=6.5, style="")
                payment_sheet_as_per_compliance.set_line_width(0.2)


    #Grand Total
    payment_sheet_as_per_compliance.set_line_width(0.4)
    payment_sheet_as_per_compliance.set_font("Helvetica", size=6.5, style="B")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Gross Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{grand_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{grand_total_dict['incentive']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{grand_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{grand_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{grand_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{grand_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{grand_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    if company_pf_esi_setup.enable_labour_welfare_fund==True:
        payment_sheet_as_per_compliance.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{grand_total_dict['total_lwf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{grand_total_dict['total_others']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{grand_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{grand_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{grand_total_dict['net_payable']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['bank_payment'], h=default_cell_height, text=f"{grand_total_dict['bank_payment']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet_as_per_compliance.cell(w=width_of_columns['other_payment'], h=default_cell_height, text=f"{grand_total_dict['other_payment']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")


    # Save the pdf with name .pdf
    buffer = bytes(payment_sheet_as_per_compliance.output())
    yield buffer
