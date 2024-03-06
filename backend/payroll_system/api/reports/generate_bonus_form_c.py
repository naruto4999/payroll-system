from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount, EarningsHead
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar

#A4 size 210 x 297 mm
width_of_columns = {
        "serial_number": 8,
        # "paycode": 18,
        "employee_name": 32,
        "father": 32,
        "15_years_of_age": 15,
        "designation": 30,
        "paid_days": 10,
        "total_bonus_wages": 15,
        "total_bonus_amount": 18,
        "deductions_total": 12.5,
        "deductions_puja": 14.5,
        "deductions_interim": 10.5,
        "deductions_income_tax": 12.5,
        "deductions_financial_loss": 14.5,
        "net_payable": 12.5,
        "amount_actually_paid": 15,
        "date_paid": 10,
        "signature": 22
    }

def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix

class FPDF(FPDF):
    def __init__(self, my_date, company_calculations, company_name, company_address, *args, **kwargs):
        self.my_date = my_date
        self.company_name = company_name
        self.company_address = company_address
        self.company_calculations = company_calculations
        super().__init__(*args, **kwargs)
    def header(self):
        #Form Heading
        self.set_font('Helvetica', 'B', 14)
        self.cell(w=0, h=6, text='PAYMENT OF BONUS RULE 1975', align="C", new_x="LMARGIN", new_y="TOP", border=0)

        #Page No
        self.set_font('Helvetica', size=6)
        self.cell(w=0, h=6, text='Page %s' % self.page_no(), border=0, align='R', new_x='LMARGIN', new_y="NEXT")

        self.set_font('Helvetica', 'B', 10)
        self.cell(w=0, h=5, text='FORM C [RULE 4 (C)]', align="C", new_x="LMARGIN", new_y="NEXT", border=0)

        #Year
        self.set_font('Helvetica', 'B', 7)
        self.cell(w=0, h=4, text=f'Bonus Calculation Sheet for the Year {self.my_date.year}-{self.my_date.year+1}', align="C", new_x="LMARGIN", new_y="NEXT", border=0)


        self.set_font('Helvetica', 'B', 9)
        self.cell(w=None, h=5, text=self.my_date.strftime(f"{self.company_name}"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        self.cell(w=None, h=5, text=self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

        initial_coordinates = {"x": self.get_x(), "y": self.get_y()}
        # Printing the column headers
        self.set_font('Helvetica', 'B', 6)
        self.set_line_width(0.5)
        self.cell(w=width_of_columns['serial_number'], h=28, text=f'S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['employee_name'], h=28, text=f'Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['father'], h=28, text=f"Father's Name", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['15_years_of_age'], h=3.5, text=f"Whether he has completed 15 yrs of age at the beginning of the accounting", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['designation'], h=28, text=f"Designation", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['paid_days'], h=5.6, text=f"No. of Paid Days in the year", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['total_bonus_wages'], h=9.33, text=f"Total Salary or wages in the year", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['total_bonus_amount'], h=28/6, text=f"Amt. of bonus payable under section 10 or section 11 as the case may be Ex gratia", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=(width_of_columns['deductions_puja']+width_of_columns['deductions_interim']+width_of_columns['deductions_income_tax']+width_of_columns['deductions_financial_loss']+width_of_columns['deductions_total']), h=5, text=f"DEDUCTIONS", align="C", new_x="LEFT", new_y='NEXT', border=1)
        self.multi_cell(w=width_of_columns['deductions_puja'], h=23/7, text=f"Puja Bonus or other customary bonus paid during the accounting year", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['deductions_interim'], h=23/6, text=f"Interim Bonus or bonus paid in advance", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['deductions_income_tax'], h=23/4, text=f"Amount of Income Tax Deducted", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['deductions_financial_loss'], h=23/8, text=f"Deduction on account of financial loss if any caused by misconduct of the employee", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['deductions_total'], h=23/4, text=f"Total Sum Deducted (Col. 9,10 and 11)", align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Net Amount
        self.set_xy(x=self.get_x(), y=initial_coordinates['y'])
        self.multi_cell(w=width_of_columns['net_payable'], h=28/5, text=f"Net Amount Payable [Col 8 - Col 12]", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #Actually Paid
        self.multi_cell(w=width_of_columns['amount_actually_paid'], h=28/3, text=f"Amount Actually Paid", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['date_paid'], h=28/3, text=f"Date on which paid", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['signature'], h=28/3, text=f"Signature / Thumb impression of the employee", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

        #Printing Column numbers
        self.cell(w=width_of_columns['serial_number'], h=5, text=f"1", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['employee_name'], h=5, text=f"2", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['father'], h=5, text=f"3", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['15_years_of_age'], h=5, text=f"4", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['designation'], h=5, text=f"5", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['paid_days'], h=5, text=f"6", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['total_bonus_wages'], h=5, text=f"7", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['total_bonus_amount'], h=5, text=f"8", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['deductions_puja'], h=5, text=f"9", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['deductions_interim'], h=5, text=f"10", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['deductions_income_tax'], h=5, text=f"10A", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['deductions_financial_loss'], h=5, text=f"11", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['deductions_total'], h=5, text=f"12", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['net_payable'], h=5, text=f"13", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['amount_actually_paid'], h=5, text=f"14", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['date_paid'], h=5, text=f"15", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['signature'], h=5, text=f"16", align="C", new_x="LMARGIN", new_y='NEXT', border=1)


        self.set_line_width(0.2)

def generate_bonus_form_c(user, request_data, employees):
    default_cell_height = 4.5
    default_cell_height_large = 6
    # default_row_number_of_cells = 1
    left_margin = 6
    right_margin = 7
    bottom_margin = 6

    company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    company_calculations = None
    try: company_calculations = employees[0].company.calculations
    except: pass
    print(f"company Details: {company_details}")
    bonus_calculation_sheet = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_calculations =company_calculations, company_name=employees[0].company.name, company_address=company_details[0].address if company_details.exists() else '', orientation="L", unit="mm", format="A4")

    #Page settings
    bonus_calculation_sheet.set_margins(left=left_margin, top=6, right=right_margin)
    bonus_calculation_sheet.add_page()
    bonus_calculation_sheet.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": bonus_calculation_sheet.get_x(), "y": bonus_calculation_sheet.get_y()}
    bonus_calculation_sheet.set_font("Helvetica", size=5.5, style="")

    for employee_index, employee in enumerate(employees):
        grand_total_employee = {
            "paid_days": 0,
            "bonus_wages": 0,
            "bonus_amount": 0,
            "ex_gratia_wages": 0,
            "ex_gratia_amount": 0,
            "total_wages": 0,

        }
        bonus_calculation_sheet.set_xy(x=initial_coordinates_after_header['x'], y=bonus_calculation_sheet.get_y())
        coordinates_current_employee = {"x": bonus_calculation_sheet.get_x(), "y": bonus_calculation_sheet.get_y()}

        #Serial
        bonus_calculation_sheet.cell(w=width_of_columns['serial_number'], h=default_cell_height*2, text=f"{employee_index+1}", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #Employee Name and Paycode
        bonus_calculation_sheet.cell(w=width_of_columns['employee_name'], h=default_cell_height, text=f"{employee.employee.name}", align="L", new_x="LEFT", new_y='NEXT', border='LRT')
        bonus_calculation_sheet.cell(w=width_of_columns['employee_name'], h=default_cell_height, text=f"{employee.employee.paycode}", align="L", new_x="RIGHT", new_y='TOP', border='LRB')
        
        #Father Name
        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
        bonus_calculation_sheet.cell(w=width_of_columns['father'], h=default_cell_height*2, text=f"{employee.employee.father_or_husband_name or ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)
        
        #Whether 15 years
        bonus_calculation_sheet.cell(w=width_of_columns['15_years_of_age'], h=default_cell_height*2, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = ''
        try: designation=employee.employee.employee_professional_detail.designation.name
        except: pass
        bonus_calculation_sheet.cell(w=width_of_columns['designation'], h=default_cell_height*2, text=f"{designation}", align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Paid Days
        start_month_year = None
        if company_calculations:
            start_month_year = date(request_data['year'], company_calculations.bonus_start_month, 1)
        for month in range(12):
            #Paid Days
            paid_days = None
            try:
                monthly_details = employee.employee.monthly_attendance_details.filter(user=user, date=start_month_year).first()
                paid_days = monthly_details.paid_days_count
                grand_total_employee['paid_days'] += paid_days
            except: 
                pass

            #Bonus Wages
            bonus_wages = None
            try:
                bonus_rate = employee.company.bonus_calculation.filter(date=start_month_year).first().amount
                if company_calculations.bonus_calculation_days == 'month_days':
                    divisor = calendar.monthrange(start_month_year.year, start_month_year.month)[1]
                else:
                    divisor = int(company_calculations.bonus_calculation_days)
                bonus_wages = round(bonus_rate/divisor*paid_days/2)
                grand_total_employee['bonus_wages'] += bonus_wages
            except:
                pass

            #Bonus Amount
            bonus_amount = None
            try:
                bonus_percentage = employee.company.bonus_percentage.bonus_percentage
                bonus_amount = round(bonus_wages*bonus_percentage/100)
                grand_total_employee['bonus_amount'] += bonus_amount
            except:
                pass

            print(f"Month: {start_month_year}")
            #Next Month
            if start_month_year:
                start_month_year = start_month_year + relativedelta(months=1)
        
        #Paid Days
        bonus_calculation_sheet.cell(w=width_of_columns['paid_days'], h=default_cell_height*2, text=f"{grand_total_employee['paid_days']/2}", align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Total Bonus Wages
        bonus_calculation_sheet.cell(w=width_of_columns['total_bonus_wages'], h=default_cell_height*2, text=f"{grand_total_employee['bonus_wages']}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Bonus Amount
        bonus_calculation_sheet.cell(w=width_of_columns['total_bonus_amount'], h=default_cell_height*2, text=f"{grand_total_employee['bonus_amount']}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Empty Rows
        bonus_calculation_sheet.cell(w=width_of_columns['deductions_puja'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['deductions_interim'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['deductions_income_tax'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['deductions_financial_loss'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['deductions_total'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['net_payable'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Total Bonus Amount Again
        bonus_calculation_sheet.cell(w=width_of_columns['amount_actually_paid'], h=default_cell_height*2, text=f"{grand_total_employee['bonus_amount']}", align="R", new_x="RIGHT", new_y='TOP', border=1)
        
        #Date and Signature
        bonus_calculation_sheet.cell(w=width_of_columns['date_paid'], h=default_cell_height*2, text=f"", align="R", new_x="RIGHT", new_y='TOP', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['signature'], h=default_cell_height*2, text=f"", align="R", new_x="LMARGIN", new_y='NEXT', border=1)



    buffer = bytes(bonus_calculation_sheet.output())
    yield buffer