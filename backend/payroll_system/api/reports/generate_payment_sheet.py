from datetime import date
from types import SimpleNamespace

from .pdf_utils.custom_fpdf import CustomFPDF
from .payment_sheet_data import build_payment_sheet_report

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
    prepared_salaries = list(prepared_salaries)
    report = build_payment_sheet_report(user, request_data, prepared_salaries, 'pdf')

    left_margin = 6
    right_margin = 7
    bottom_margin = 3
    top_margin = 6

    default_cell_height = 5
    company_pf_esi_setup = SimpleNamespace(
        enable_labour_welfare_fund=report.show_lwf,
    )
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
    report_rows = report.rows
    for index, salary in enumerate(prepared_salaries):
        report_row = report_rows[index]
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
        total_earnings_rate = report_row.salary_rate
        payment_sheet.cell(w=width_of_columns['salary_rate'], h=default_cell_height, text=f"{total_earnings_rate if total_earnings_rate!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Paid Days
        paid_days_str = report_row.paid_days if report_row.paid_days is not None else ''
        payment_sheet.cell(w=width_of_columns['paid_days'], h=default_cell_height, text=f'{paid_days_str}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Earned Salary
        total_earnings_amount = report_row.earned_salary
        if total_earnings_amount:
            grand_total_dict['earned_salary'] += total_earnings_amount
            dept_total_dict['earned_salary'] += total_earnings_amount
        payment_sheet.cell(w=width_of_columns['earned_salary'], h=default_cell_height, text=f"{total_earnings_amount if total_earnings_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Incentive
        if report_row.incentive:
            grand_total_dict['incentive'] += report_row.incentive
            dept_total_dict['incentive'] += report_row.incentive
        payment_sheet.cell(w=width_of_columns['incentive'], h=default_cell_height, text=f"{report_row.incentive if report_row.incentive is not None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT
        ot_hrs = report_row.ot_hours
        payment_sheet.cell(w=width_of_columns['ot_hrs'], h=default_cell_height, text=f"{ot_hrs if ot_hrs!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Amt
        ot_amt = report_row.ot_amount
        if ot_amt:
            grand_total_dict['ot_amt'] += ot_amt
            dept_total_dict['ot_amt'] += ot_amt
        payment_sheet.cell(w=width_of_columns['ot_amount'], h=default_cell_height, text=f"{ot_amt if ot_amt!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Earned
        total_earned = report_row.total_earned
        if total_earned:
            grand_total_dict['total_earnings'] += total_earned
            dept_total_dict['total_earnings'] += total_earned
        payment_sheet.cell(w=width_of_columns['total_earnings'], h=default_cell_height, text=f"{total_earned if total_earned!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Advance
        if report_row.advance:
            grand_total_dict['total_advance'] += report_row.advance
            dept_total_dict['total_advance'] += report_row.advance
        payment_sheet.cell(w=width_of_columns['advance'], h=default_cell_height, text=str(report_row.advance), align="R", new_x="RIGHT", new_y='TOP', border=1)

        #EPF
        pf_and_vpf_deducted = report_row.epf
        if pf_and_vpf_deducted:
            grand_total_dict['total_pf'] += pf_and_vpf_deducted
            dept_total_dict['total_pf'] += pf_and_vpf_deducted
        payment_sheet.cell(w=width_of_columns['epf'], h=default_cell_height, text=f"{pf_and_vpf_deducted}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #ESI
        if report_row.esi:
            grand_total_dict['total_esi'] += report_row.esi
            dept_total_dict['total_esi'] += report_row.esi
        payment_sheet.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=str(report_row.esi), align="R", new_x="RIGHT", new_y='TOP', border=1)
        
        #LWF
        if company_pf_esi_setup.enable_labour_welfare_fund:
            if report_row.lwf:
                grand_total_dict['total_lwf'] += report_row.lwf
                dept_total_dict['total_lwf'] += report_row.lwf
            payment_sheet.cell(w=width_of_columns['lwf'], h=default_cell_height, text=str(report_row.lwf), align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Others
        if report_row.others:
            grand_total_dict['total_others'] += report_row.others
            dept_total_dict['total_others'] += report_row.others
        payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=str(report_row.others), align="R", new_x="RIGHT", new_y='TOP', border=1)

        #TDS
        if report_row.tds:
            grand_total_dict['total_tds'] += report_row.tds
            dept_total_dict['total_tds'] += report_row.tds
        payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=str(report_row.tds), align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Deductions
        total_deductions = report_row.total_deductions
        if total_deductions:
            grand_total_dict['total_deductions'] +=  total_deductions
            dept_total_dict['total_deductions'] +=  total_deductions
        payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{total_deductions if total_deductions!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Net Payable
        net_payable = report_row.net_payable
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
    payment_sheet.cell(w=width_of_columns['esi'] if company_pf_esi_setup.enable_labour_welfare_fund==True else width_of_columns['esi']+width_of_columns['lwf'], h=default_cell_height, text=f"{grand_total_dict['total_esi']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    if company_pf_esi_setup.enable_labour_welfare_fund==True:
        payment_sheet.cell(w=width_of_columns['lwf'], h=default_cell_height, text=f"{grand_total_dict['total_lwf']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['others'], h=default_cell_height, text=f"{grand_total_dict['total_others']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['tds'], h=default_cell_height, text=f"{grand_total_dict['total_tds']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['total_deductions'], h=default_cell_height, text=f"{grand_total_dict['total_deductions']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    payment_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height, text=f"{grand_total_dict['net_payable']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")
    

    # Save the pdf with name .pdf
    buffer = bytes(payment_sheet.output())
    yield buffer
