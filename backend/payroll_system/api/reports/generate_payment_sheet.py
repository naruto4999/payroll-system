from fpdf import FPDF
from ..models import EmployeeSalaryPrepared, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, LeaveGrade, EmployeeGenerativeLeaveRecord, EmployeeMonthlyAttendanceDetails, CompanyDetails, EarningsHead, EmployeeSalaryEarning, EarnedAmount, PfEsiSetup
from datetime import date
from django.db.models import Case, When, Value, CharField
import math

width_of_columns = {
    "serial": 7,
    "acn": 12,
    "employee_name": 41,
    "father_husband_name": 39,
    "designation": 25,
    "salary_rate": 12.5,
    "paid_days": 7,
    "earned_salary": 12.5,
    "ot_hrs": 10,
    "ot_amount": 12.5,
    "total_earnings": 12.5,
    "advance": 12.5,
    "epf": 10,
    "esi": 8,
    "tds": 10,
    "total_deductions": 12.5,
    "net_payable": 15,
    "signature": 25
}

class FPDF(FPDF):
        def __init__(self, my_date, company_name, company_address, *args, **kwargs):
            self.my_date = my_date
            self.company_name = company_name
            self.company_address = company_address
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
            self.cell(w=width_of_columns['acn'], h=10, text=f'ACN', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Employee Name
            self.cell(w=width_of_columns['employee_name'], h=10, text=f'Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Father Husband Name
            self.cell(w=width_of_columns['father_husband_name'], h=10, text=f'F/H Name', align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Designation
            self.cell(w=width_of_columns['designation'], h=10, text=f'Designation', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Salary Rate
            self.cell(w=width_of_columns['salary_rate'], h=10, text=f'Sal. Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Paid Days
            self.cell(w=width_of_columns['paid_days'], h=10, text=f'PD', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Earned Salary
            self.cell(w=width_of_columns['earned_salary'], h=10, text=f'Earned S.', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #OT Hrs
            self.cell(w=width_of_columns['ot_hrs'], h=10, text=f'OT Hrs', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #OT Amt
            self.cell(w=width_of_columns['ot_amount'], h=10, text=f'OT Amt.', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Total Earnings
            self.cell(w=width_of_columns['total_earnings'], h=10, text=f'T. Earned', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Advance
            self.cell(w=width_of_columns['advance'], h=10, text=f'Advance', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #EPF
            self.cell(w=width_of_columns['epf'], h=10, text=f'EPF', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #ESI
            self.cell(w=width_of_columns['esi'], h=10, text=f'ESI', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #TDS
            self.cell(w=width_of_columns['tds'], h=10, text=f'TDS', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Total Deductions
            self.cell(w=width_of_columns['total_deductions'], h=10, text=f'T. Ded.', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Net Payable
            self.cell(w=width_of_columns['net_payable'], h=10, text=f'Net Payable', align="C", new_x="RIGHT", new_y='TOP', border=1)
            
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

    grand_total_dict = {
        "earned_salary" : 0,
        "ot_amt": 0,
        "total_earnings": 0,
        "total_advance": 0,
        "total_pf": 0,
        "total_esi": 0,
        "total_tds": 0,
        "total_deductions": 0,
        "net_payable": 0,
    }

    dept_total_dict = {
        "earned_salary" : 0,
        "ot_amt": 0,
        "total_earnings": 0,
        "total_advance": 0,
        "total_pf": 0,
        "total_esi": 0,
        "total_tds": 0,
        "total_deductions": 0,
        "net_payable": 0,
    }

    #Getting Company
    company = prepared_salaries[0].company
    company_address = ''
    try: company_address = company.company_details.address
    except: pass
    payment_sheet = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=company.name,company_address=company_address, orientation="L", unit="mm", format="A4")

    #Page settings
    payment_sheet.set_margins(left=left_margin, top=top_margin, right=right_margin)
    payment_sheet.add_page()
    payment_sheet.set_auto_page_break(auto=True, margin = bottom_margin)

    payment_sheet.set_font("Helvetica", size=7, style="")
    for index, salary in enumerate(prepared_salaries):
        if request_data['filters']['group_by'] != 'none':
            try:
                if index == 0 or salary.employee.employee_professional_detail.department.name != prepared_salaries[index-1].employee.employee_professional_detail.department.name:
                    payment_sheet.set_font("Helvetica", size=9, style="B")
                    payment_sheet.cell(w=0, h=default_cell_height, text=f'{salary.employee.employee_professional_detail.department.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    payment_sheet.set_font("Helvetica", size=7, style="")
                    dept_total_dict = {
                        "earned_salary" : 0,
                        "ot_amt": 0,
                        "total_earnings": 0,
                        "total_advance": 0,
                        "total_pf": 0,
                        "total_esi": 0,
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
        payment_sheet.cell(w=width_of_columns['employee_name'], h=default_cell_height, text=f'{salary.employee.name}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #F/H Name
        payment_sheet.cell(w=width_of_columns['father_husband_name'], h=default_cell_height, text=f'{salary.employee.father_or_husband_name or ""}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = None
        try: designation = salary.employee.employee_professional_detail.designation.name
        except: pass
        payment_sheet.cell(w=width_of_columns['designation'], h=default_cell_height, text=f"{designation if designation else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Salary Rate
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=salary.company, user=salary.user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=salary.employee, from_date__lte=salary.date, to_date__gte=salary.date)
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass
        designation = None
        try: designation = salary.employee.employee_professional_detail.designation.name
        except: pass
        payment_sheet.cell(w=width_of_columns['salary_rate'], h=default_cell_height, text=f"{total_earnings_rate if total_earnings_rate else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Paid Days
        paid_days = 0
        paid_days_str = ''
        employee_monthly_attendance_details = None
        try: 
            employee_monthly_attendance_details = salary.employee.monthly_attendance_details.filter(date=salary.date).first()
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
            try: total_earnings_amount += salary.incentive_amount
            except: pass
        except: 
            pass
        if total_earnings_amount:
            grand_total_dict['earned_salary'] += total_earnings_amount
            dept_total_dict['earned_salary'] += total_earnings_amount
        payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{total_earnings_amount if total_earnings_amount else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT
        ot_hrs = None
        if employee_monthly_attendance_details:
            ot_hrs = salary.net_ot_minutes_monthly/60
        payment_sheet.cell(w=width_of_columns['ot_hrs'], h=default_cell_height, text=f"{ot_hrs if ot_hrs else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Amt
        ot_amt = None
        if employee_monthly_attendance_details:
            ot_amt = salary.net_ot_amount_monthly
        if ot_amt:
            grand_total_dict['ot_amt'] += ot_amt
            dept_total_dict['ot_amt'] += ot_amt
        payment_sheet.cell(w=width_of_columns['ot_amount'], h=default_cell_height, text=f"{ot_amt if ot_amt else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Earned
        total_earned = None
        if total_earnings_amount:
            total_earned = total_earnings_amount
            if ot_amt:
                total_earned += ot_amt
        if total_earned:
            grand_total_dict['total_earnings'] += total_earned
            dept_total_dict['total_earnings'] += total_earned
        payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{total_earned if total_earned else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Advance
        advance_deducted = None
        try:
            advance = salary.advance_deducted
            if  advance > 0:
                advance_deducted = advance
        except:
            pass
        if advance_deducted:
            grand_total_dict['total_advance'] += advance_deducted
            dept_total_dict['total_advance'] += advance_deducted
        payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{advance_deducted if advance_deducted else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #EPF
        pf_deducted = None
        try:
            pf = salary.pf_deducted
            if  pf > 0:
                pf_deducted = pf
        except:
            pass
        if pf_deducted:
            grand_total_dict['total_pf'] += pf_deducted
            dept_total_dict['total_pf'] += pf_deducted
        payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{pf_deducted if pf_deducted else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #ESI
        esi_deducted = None
        try:
            esi = salary.esi_deducted
            if  esi > 0:
                esi_deducted = esi
        except:
            pass
        if esi_deducted:
            grand_total_dict['total_esi'] += esi_deducted
            dept_total_dict['total_esi'] += esi_deducted
        payment_sheet.cell(w=width_of_columns['esi'], h=default_cell_height, text=f"{esi_deducted if esi_deducted else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #TDS
        tds_deducted = None
        try:
            tds = salary.tds_deducted
            if  tds > 0:
                tds_deducted = tds
        except:
            pass
        if tds_deducted:
            grand_total_dict['total_tds'] += tds_deducted
            dept_total_dict['total_tds'] += tds_deducted
        payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{tds_deducted if tds_deducted else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Deductions
        total_deductions = None
        try:
            total_deductions = salary.advance_deducted + salary.pf_deducted + salary.esi_deducted + salary.tds_deducted
        except:
            pass
        if total_deductions:
            grand_total_dict['total_deductions'] +=  total_deductions
            dept_total_dict['total_deductions'] +=  total_deductions
        payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{total_deductions if total_deductions else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

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
                payment_sheet.set_font("Helvetica", size=7, style="B")
                payment_sheet.set_line_width(0.4)
                payment_sheet.set_font("Helvetica", size=7, style="B")
                payment_sheet.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Department Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{dept_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{dept_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{dept_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{dept_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{dept_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['esi'], h=default_cell_height, text=f"{dept_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{dept_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{dept_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
                payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{dept_total_dict['net_payable']}", align="R", new_x="LMARGIN", new_y='NEXT', border="TB")
                payment_sheet.set_font("Helvetica", size=7, style="")
                payment_sheet.set_line_width(0.2)

        

    #Grand Total
    payment_sheet.set_line_width(0.4)
    payment_sheet.set_font("Helvetica", size=7, style="B")
    payment_sheet.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation']+width_of_columns['salary_rate']+width_of_columns['paid_days'], h=default_cell_height, text=f"Gross Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{grand_total_dict['earned_salary']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['ot_amount']+width_of_columns['ot_hrs'], h=default_cell_height, text=f"{grand_total_dict['ot_amt']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{grand_total_dict['total_earnings']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{grand_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{grand_total_dict['total_pf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['esi'], h=default_cell_height, text=f"{grand_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{grand_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{grand_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{grand_total_dict['net_payable']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    

    # Save the pdf with name .pdf
    buffer = bytes(payment_sheet.output())
    yield buffer