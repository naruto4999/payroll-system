from fpdf import FPDF
from ..models import EarningsHead, EmployeeSalaryEarning, EarnedAmount, PfEsiSetup
from datetime import date
from django.db.models import Case, When, Value, CharField
import math
from .pdf_utils.custom_fpdf import CustomFPDF

#Note - Add LWF Column in this payment sheet as well. Render it conditionally depending upon if company pf esi setup has lwf enabled or not.
width_of_columns = {
    "serial": 7,
    "acn": 12,
    "employee_name": 33,
    "father_husband_name": 33,
    "designation": 23,
    "salary_rate": 11,
    "paid_days": 7,
    #"earned_salary": 12.5,
    "earned_salary": 11,
    "incentive": 11,
    "ot_hrs": 10,
    "ot_amount": 11,
    "total_earnings": 11,
    "advance": 11,
    "epf": 10,
    "esi": 8,
    "lwf": 7,
    "others": 10,
    "tds": 10,
    "total_deductions": 11,
    "net_payable": 12,
    "signature": 25
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
            self.set_font('Arial', 'B', 15)
            self.cell(0, 8, self.company_name, align="L", new_x="RIGHT", new_y='TOP', border=0)
            self.set_font("Helvetica", size=7, style="")
            self.cell(0, 8, 'Page %s' % self.page_no(), align="R", new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Address and add Address
            self.set_font('Arial', 'B', 9)
            self.cell(0, 4, self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Month and Year and add Month and Year
            self.cell(0, 6, self.my_date.strftime("Payment Sheet for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

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
            # self.cell(w=width_of_columns['salary_rate'], h=10, text=f'Sal. Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)
            self.multi_cell(w=width_of_columns['salary_rate'], h=10/2, text=f'Salary Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)

            
            #Paid Days
            coordinates_before_paid_days = {"x": self.get_x(), "y": self.get_y()}
            self.cell(w=width_of_columns['paid_days'], h=10/3, text=f'PD', align="C", new_x="LEFT", new_y='NEXT', border='LRT')
            self.set_font("Helvetica", size=4.5, style="I")
            self.multi_cell(w=width_of_columns['paid_days'], h=10/3, text=f'(Paid Days)', align="C", new_x="RIGHT", new_y='TOP', border='LRB')
            self.set_xy(x=self.get_x(), y=coordinates_before_paid_days['y'])
            self.set_font("Helvetica", size=7, style="B")
            
            #Earned Salary
            coordinates_before_earned_salary = {"x": self.get_x(), "y": self.get_y()}
            # self.cell(w=width_of_columns['earned_salary'], h=10, text=f'Earned S.', align="C", new_x="RIGHT", new_y='TOP', border=1)
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
            self.cell(w=width_of_columns['ot_amount'], h=10, text=f'OT Amt.', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
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
            
            #Signature
            self.cell(w=width_of_columns['signature'], h=10, text=f'Signature', align="C", new_x="LMARGIN", new_y='NEXT', border=1)

def generate_payment_sheet(user, request_data, prepared_salaries):

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
    }

    #Getting Company
    company = prepared_salaries[0].company
    company_address = ''
    try: company_address = company.company_details.address
    except: pass
    payment_sheet = CustomFPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=company.name,company_address=company_address,company_pf_esi_setup=company_pf_esi_setup, orientation="L", unit="mm", format="A4")

    #Page settings
    payment_sheet.set_margins(left=left_margin, top=top_margin, right=right_margin)
    payment_sheet.add_page()
    payment_sheet.set_auto_page_break(auto=True, margin = bottom_margin)

    payment_sheet.set_font("Helvetica", size=6.5, style="")
    for index, salary in enumerate(prepared_salaries):
        if request_data['filters']['group_by'] != 'none':
            try:
                if index == 0 or salary.employee.employee_professional_detail.department.name != prepared_salaries[index-1].employee.employee_professional_detail.department.name:
                    payment_sheet.set_font("Helvetica", size=9, style="B")
                    payment_sheet.cell(w=0, h=default_cell_height, text=f'{salary.employee.employee_professional_detail.department.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    payment_sheet.set_font("Helvetica", size=6.5, style="")
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
                    }
            except:
                pass
        #Serial
        payment_sheet.cell(w=width_of_columns['serial'], h=default_cell_height, text=f'{index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #ACN
        payment_sheet.cell(w=width_of_columns['acn'], h=default_cell_height, text=f'{salary.employee.attendance_card_no}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Employee Name
        payment_sheet.multi_cell_with_limit(w=width_of_columns['employee_name'], h=default_cell_height, text=f'{salary.employee.name}', min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #F/H Name
        payment_sheet.multi_cell_with_limit(w=width_of_columns['father_husband_name'], h=default_cell_height, text=f'{salary.employee.father_or_husband_name or ""}', min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = None
        try: designation = salary.employee.employee_professional_detail.designation.name
        except: pass
        payment_sheet.multi_cell_with_limit(w=width_of_columns['designation'], h=default_cell_height, text=f"{designation if designation else ''}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Salary Rate
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=salary.company, user=salary.user if salary.user.role == "OWNER" else salary.user.regular_to_owner.owner)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=salary.employee, from_date__lte=salary.date, to_date__gte=salary.date)
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass
        payment_sheet.cell(w=width_of_columns['salary_rate'], h=default_cell_height, text=f"{total_earnings_rate if total_earnings_rate!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Paid Days
        paid_days = 0
        paid_days_str = ''
        employee_monthly_attendance_details = None
        try: 
            employee_monthly_attendance_details = salary.employee.monthly_attendance_details.filter(date=salary.date, user=user).first()
            print(f"Paid Days: { salary.employee.monthly_attendance_details.filter(date=salary.date, user=user)}")
            paid_days += employee_monthly_attendance_details.paid_days_count
            paid_days_str =  paid_days/2
        except: 
            pass
        payment_sheet.cell(w=width_of_columns['paid_days'], h=default_cell_height, text=f'{paid_days_str}', align="L", new_x="RIGHT", new_y='TOP', border=1)

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
        payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{total_earnings_amount if total_earnings_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Incentive
        if salary.incentive_amount:
            grand_total_dict['incentive'] += salary.incentive_amount
            dept_total_dict['incentive'] +=salary.incentive_amount
        payment_sheet.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{salary.incentive_amount if salary.incentive_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT
        ot_hrs = None
        if employee_monthly_attendance_details:
            ot_hrs = salary.net_ot_minutes_monthly/60
        payment_sheet.cell(w=width_of_columns['ot_hrs'], h=default_cell_height, text=f"{ot_hrs if ot_hrs!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Amt
        ot_amt = None
        if employee_monthly_attendance_details:
            ot_amt = salary.net_ot_amount_monthly
        if ot_amt:
            grand_total_dict['ot_amt'] += ot_amt
            dept_total_dict['ot_amt'] += ot_amt
        payment_sheet.cell(w=width_of_columns['ot_amount'], h=default_cell_height, text=f"{ot_amt if ot_amt!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

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
        payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{total_earned if total_earned!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Advance
        if salary.advance_deducted:
            grand_total_dict['total_advance'] += salary.advance_deducted
            dept_total_dict['total_advance'] += salary.advance_deducted
        payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{salary.advance_deducted if salary.advance_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #EPF
        pf_and_vpf_deducted = 0
        if salary.pf_deducted:
            pf_and_vpf_deducted += salary.pf_deducted
            grand_total_dict['total_pf'] += salary.pf_deducted
            dept_total_dict['total_pf'] += salary.pf_deducted
        if salary.vpf_deducted:
            pf_and_vpf_deducted += salary.vpf_deducted
            grand_total_dict['total_pf'] += salary.vpf_deducted
            dept_total_dict['total_pf'] += salary.vpf_deducted
        payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{pf_and_vpf_deducted}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #ESI
        if salary.esi_deducted:
            grand_total_dict['total_esi'] += salary.esi_deducted
            dept_total_dict['total_esi'] += salary.esi_deducted
        payment_sheet.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{salary.esi_deducted if salary.esi_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)
        
        #LWF
        if company_pf_esi_setup.enable_labour_welfare_fund:
            if salary.labour_welfare_fund_deducted:
                grand_total_dict['total_lwf'] += salary.labour_welfare_fund_deducted
                dept_total_dict['total_lwf'] += salary.labour_welfare_fund_deducted
            payment_sheet.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{salary.labour_welfare_fund_deducted if salary.labour_welfare_fund_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Others
        if salary.others_deducted:
            grand_total_dict['total_others'] += salary.others_deducted
            dept_total_dict['total_others'] += salary.others_deducted
        payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{salary.others_deducted if salary.others_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #TDS
        if salary.tds_deducted:
            grand_total_dict['total_tds'] += salary.tds_deducted
            dept_total_dict['total_tds'] += salary.tds_deducted
        payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{salary.tds_deducted if salary.tds_deducted!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Deductions
        total_deductions = None
        try:
            #total_deductions = salary.pf_deducted+esi_deducted_based_on_overtime_filter+salary.vpf_deducted+salary.advance_deducted+salary.tds_deducted+salary.others_deducted
            total_deductions = salary.advance_deducted + salary.pf_deducted + salary.esi_deducted + salary.tds_deducted + salary.others_deducted + salary.vpf_deducted
            if company_pf_esi_setup.enable_labour_welfare_fund:
                total_deductions += salary.labour_welfare_fund_deducted
        except:
            pass
        if total_deductions:
            grand_total_dict['total_deductions'] +=  total_deductions
            dept_total_dict['total_deductions'] +=  total_deductions
        payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{total_deductions if total_deductions!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Net Payable
        net_payable = None
        try:
            net_payable = total_earned - total_deductions
        except:
            pass
        if net_payable:
            grand_total_dict['net_payable'] +=  net_payable
            dept_total_dict['net_payable'] +=  net_payable
        payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{net_payable if net_payable else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Signature
        payment_sheet.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

        #Dept Total if applicable
        if request_data['filters']['group_by'] != 'none':
            if (index != len(prepared_salaries)-1 and salary.employee.employee_professional_detail.department != prepared_salaries[index+1].employee.employee_professional_detail.department) or (index == len(prepared_salaries)-1 and salary.employee.employee_professional_detail.department):
                payment_sheet.set_font("Helvetica", size=6.5, style="B")
                payment_sheet.set_line_width(0.4)
                payment_sheet.set_font("Helvetica", size=6.5, style="B")
                payment_sheet.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Department Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{dept_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{dept_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{dept_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{dept_total_dict['incentive']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{dept_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{dept_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{dept_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                if company_pf_esi_setup.enable_labour_welfare_fund==True:
                    payment_sheet.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{dept_total_dict['total_lwf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{dept_total_dict['total_others']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{dept_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{dept_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{dept_total_dict['net_payable']}", align="R", new_x="LMARGIN", new_y='NEXT', border="TB")
                payment_sheet.set_font("Helvetica", size=6.5, style="")
                payment_sheet.set_line_width(0.2)

        

    #Grand Total
    payment_sheet.set_line_width(0.4)
    payment_sheet.set_font("Helvetica", size=6.5, style="B")
    payment_sheet.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Gross Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{grand_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{grand_total_dict['incentive']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{grand_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{grand_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{grand_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{grand_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['esi'], h=default_cell_height, text=f"{grand_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    if company_pf_esi_setup.enable_labour_welfare_fund==True:
        payment_sheet.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{grand_total_dict['total_lwf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{grand_total_dict['total_others']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{grand_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{grand_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{grand_total_dict['net_payable']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    

    # Save the pdf with name .pdf
    buffer = bytes(payment_sheet.output())
    yield buffer
