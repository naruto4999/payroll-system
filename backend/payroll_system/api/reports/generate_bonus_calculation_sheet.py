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
        "paycode": 18,
        "employee_name": 44,
        "designation": 40,
        "particulars": 16,
        "month": 10,
        "grand_total": 18,
        "remarks": 20,
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
        self.set_font('Helvetica', 'B', 16)
        self.cell(w=None, h=8, text=self.company_name, align="L", new_x="LEFT", border=0)
        self.set_font('Helvetica', size=6)
        self.cell(w=0, h=8, text='Page %s' % self.page_no(), border=0, align='R', new_x='LMARGIN', new_y="NEXT")
        self.set_font('Helvetica', 'B', 9)
        self.cell(w=None, h=4, text=self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)
        day_suffix = get_day_suffix(self.my_date.day)
        self.cell(w=None, h=6, text=self.my_date.strftime(f"Bonus Calculation Sheet for the year {self.my_date.year}-{self.my_date.year+1}"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        #Printing the column headers
        self.set_font('Helvetica', 'B', 7.5)
        self.set_line_width(0.5)
        self.cell(w=width_of_columns['serial_number'], h=10, text='S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['paycode'], h=10, text='Paycode', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['employee_name'], h=5, text=f'Employee Name\nFather/Husband Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.multi_cell(w=width_of_columns['designation'], h=5, text=f"Designation\nDepartment", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['particulars'], h=10, text='Particulars', align="C", new_x="RIGHT", new_y='TOP', border=1)
        start_month_year = None
        print(f"Bonus Start Month: {self.company_calculations.bonus_start_month}")
        if self.company_calculations:
            start_month_year = date(self.my_date.year, self.company_calculations.bonus_start_month, 1)
        for month in range(12):
            print(f"Month Printing: {start_month_year}")
            self.cell(w=width_of_columns['month'], h=10, text=f"{start_month_year.strftime('%b') if start_month_year else ''}", align="C", new_x="RIGHT", new_y='TOP', border=1)
            if start_month_year:
                start_month_year = start_month_year + relativedelta(months=1)
        self.cell(w=width_of_columns['grand_total'], h=10, text='Grand Tot.', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['remarks'], h=10, text='Remarks', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        self.set_line_width(0.2)

def generate_bonus_calculation_sheet(user, request_data, employees):
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
    bonus_calculation_sheet.set_font("Helvetica", size=6.5, style="")
    rows_per_page = (210-initial_coordinates_after_header['y']-bottom_margin)//(default_cell_height*6)
    if request_data['filters']['group_by'] != 'none':
        rows_per_page = ((210-initial_coordinates_after_header['y']-bottom_margin)-(default_cell_height*rows_per_page))//(default_cell_height*6)
        print('Group By Not None')

    print(f"Rows per page: {rows_per_page}")

    for employee_index, employee in enumerate(employees):
        bonus_calculation_sheet.set_xy(x=initial_coordinates_after_header['x'], y=bonus_calculation_sheet.get_y())

        #Department Heading
        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = employee.employee.employee_professional_detail.department
                previous_employee_department = employees[employee_index-1].employee.employee_professional_detail.department if employee_index!=0 else None
                if employee_index == 0 or current_employee_department != previous_employee_department:
                    bonus_calculation_sheet.set_font("Helvetica", size=10, style="B")
                    bonus_calculation_sheet.cell(w=0, h=default_cell_height_large, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    bonus_calculation_sheet.set_font("Helvetica", size=6.5, style="")
            except:
                pass

        grand_total_employee = {
            "paid_days": 0,
            "bonus_wages": 0,
            "bonus_amount": 0,
            "ex_gratia_wages": 0,
            "ex_gratia_amount": 0,
            "total_wages": 0,

        }
        coordinates_current_employee = {"x": bonus_calculation_sheet.get_x(), "y": bonus_calculation_sheet.get_y()}
        bonus_calculation_sheet.set_line_width(0.35)
        bonus_calculation_sheet.rect(x=bonus_calculation_sheet.get_x(), y=bonus_calculation_sheet.get_y(), w=297-left_margin-right_margin, h=default_cell_height*6)
        bonus_calculation_sheet.set_line_width(0.15)
        #Serial
        bonus_calculation_sheet.cell(w=width_of_columns['serial_number'], h=default_cell_height*6, text=f"{employee_index+1}", align="C",  new_x="RIGHT", new_y='TOP', border=1)
        
        #Paycode
        bonus_calculation_sheet.cell(w=width_of_columns['paycode'], h=default_cell_height*6, text=f"{employee.employee.paycode}", align="L",  new_x="RIGHT", new_y='TOP', border=1)

        #Name
        bonus_calculation_sheet.rect(x=bonus_calculation_sheet.get_x(), y=bonus_calculation_sheet.get_y(), w=width_of_columns['employee_name'], h=default_cell_height*6)
        bonus_calculation_sheet.cell(w=width_of_columns['employee_name'], h=default_cell_height*3, text=f"{employee.employee.name}", align="L",  new_x="LEFT", new_y='NEXT', border=0)
        bonus_calculation_sheet.cell(w=width_of_columns['employee_name'], h=default_cell_height*3, text=f"{employee.employee.father_or_husband_name or ''}", align="L",  new_x="RIGHT", new_y='TOP', border=0)

        #Designation / Department
        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
        department = ''
        designation = ''
        try: department=employee.employee.employee_professional_detail.department.name
        except: pass
        try: department=employee.employee.employee_professional_detail.designation.name
        except: pass
        bonus_calculation_sheet.rect(x=bonus_calculation_sheet.get_x(), y=bonus_calculation_sheet.get_y(), w=width_of_columns['designation'], h=default_cell_height*6)
        bonus_calculation_sheet.cell(w=width_of_columns['designation'], h=default_cell_height*3, text=f"{designation}", align="L",  new_x="LEFT", new_y='NEXT', border=0)
        bonus_calculation_sheet.cell(w=width_of_columns['designation'], h=default_cell_height*3, text=f"{department}", align="L",  new_x="RIGHT", new_y='TOP', border=0)

        #Particulars
        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Days", align="L",  new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Bonus Wages", align="L",  new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Bonus Amt.", align="L",  new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Exgr. Wages", align="L",  new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Exgr. Amt.", align="L",  new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['particulars'], h=default_cell_height, text=f"Total Wages", align="L",  new_x="RIGHT", new_y='NEXT', border=1)

        ##Main table
        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
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
            print(f"Paid Days: {paid_days}")
            print(f"Date: {start_month_year}")
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{paid_days/2 if paid_days else ''}", align="C", new_x="LEFT", new_y='NEXT', border=1)
            
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
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{bonus_wages if bonus_wages else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)
            
            #Bonus Amount
            bonus_amount = None
            try:
                bonus_percentage = employee.company.bonus_percentage.bonus_percentage
                bonus_amount = round(bonus_wages*bonus_percentage/100)
                grand_total_employee['bonus_amount'] += bonus_amount
            except:
                pass
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{bonus_amount if bonus_amount else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)

            #Exgratia Wages
            total_earnings_wages = None
            ex_gratia_wages = None
            try:
                total_earnings_rate = 0
                earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
                employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee.employee, from_date__lte=start_month_year, to_date__gte=start_month_year)
                for head in earnings_heads:
                    salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                    if salary_for_particular_earning_head.exists():
                        total_earnings_rate += salary_for_particular_earning_head.first().value
                if company_calculations.bonus_calculation_days == 'month_days':
                    divisor = calendar.monthrange(start_month_year.year, start_month_year.month)[1]
                else:
                    divisor = int(company_calculations.bonus_calculation_days)
                total_earnings_wages = round(total_earnings_rate/divisor*paid_days/2)
                if bonus_wages<total_earnings_wages and employee.bonus_exg==True:
                    ex_gratia_wages = total_earnings_wages-bonus_wages
                    grand_total_employee['ex_gratia_wages'] += ex_gratia_wages
                    
            except: 
                pass
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{ex_gratia_wages if ex_gratia_wages else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)

            #Exgratia Amount
            ex_gratia_amount = None
            try:
                bonus_percentage = employee.company.bonus_percentage.bonus_percentage
                ex_gratia_amount = round(ex_gratia_wages*bonus_percentage/100)
                grand_total_employee['ex_gratia_amount'] += ex_gratia_amount
            except:
                pass
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{ex_gratia_amount if ex_gratia_amount else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)

            #Total Wages
            total_wages = None
            try: 
                total_wages = bonus_wages + (ex_gratia_wages if ex_gratia_wages else 0)
                grand_total_employee['total_wages'] += total_wages
            except: pass
            bonus_calculation_sheet.cell(w=width_of_columns['month'], h=default_cell_height, text=f"{total_wages if total_wages else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

            if start_month_year:
                start_month_year = start_month_year + relativedelta(months=1)
            bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])

        #Grand Total
        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['paid_days']/2}", align="C", new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['bonus_wages']}", align="R", new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['bonus_amount']}", align="R", new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['ex_gratia_wages'] if employee.bonus_exg==True else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['ex_gratia_amount'] if employee.bonus_exg==True else ''}", align="R", new_x="LEFT", new_y='NEXT', border=1)
        bonus_calculation_sheet.cell(w=width_of_columns['grand_total'], h=default_cell_height, text=f"{grand_total_employee['total_wages']}", align="R", new_x="RIGHT", new_y='TOP', border=1)

        bonus_calculation_sheet.set_xy(x=bonus_calculation_sheet.get_x(), y=coordinates_current_employee['y'])
        for i in range(6):
            bonus_calculation_sheet.cell(w=width_of_columns['remarks'], h=default_cell_height, text=f'', align="C", new_x="LEFT", new_y='NEXT', border=1)

        if (employee_index+1)%rows_per_page==0 and employee_index!=0 and employee_index<(len(employees)-1):
            bonus_calculation_sheet.add_page()
            bonus_calculation_sheet.set_xy(x=initial_coordinates_after_header['x'], y=initial_coordinates_after_header['y'])

    buffer = bytes(bonus_calculation_sheet.output())
    yield buffer