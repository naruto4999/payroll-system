from fpdf import FPDF
import os
from ...models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount, EarningsHead
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

#A4 size 210 x 297 mm

def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix

def format_text(text, max_width_mm, fpdf_instance):
    if fpdf_instance.get_string_width(text) <= max_width_mm:
        return text
    else:
        for i in range(len(text), 0, -1):
            str_width = fpdf_instance.get_string_width(text[:i])
            if str_width<=max_width_mm:
                return text[:i]


class FPDF(FPDF):
    def __init__(self, width_of_columns, from_date, to_date, company_name, company_address, *args, **kwargs):
        self.width_of_columns = width_of_columns
        self.from_date = from_date
        self.to_date = to_date
        self.company_name = company_name
        self.company_address = company_address

        super().__init__(*args, **kwargs)
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(w=None, h=8, text=self.company_name, align="L", new_x="LEFT", border=0)
        self.set_font('Helvetica', size=6)
        self.cell(w=0, h=8, text='Page %s' % self.page_no(), border=0, align='R', new_x='LMARGIN', new_y="NEXT")
        self.set_font('Helvetica', 'B', 9)
        self.cell(w=None, h=4, text=self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)
        day_suffix = get_day_suffix(self.from_date.day)
        self.cell(w=None, h=6, text=f"Strength Report for the period of {self.from_date.strftime(f'%e{day_suffix} %B, %Y')} to {self.to_date.strftime(f'%e{day_suffix} %B, %Y')}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        #Printing the column headers
        self.set_font('Helvetica', 'B', 7)
        self.set_line_width(0.5)
        self.cell(w=self.width_of_columns['serial_number'], h=5, text='S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['paycode'], h=5, text='Paycode', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['employee_name'], h=5, text='Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['father_name'], h=5, text="Father's Name", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['doj'], h=5, text="DOJ", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['resignation_date'], h=5, text="Resig. Date", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['department'], h=5, text='Department', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=self.width_of_columns['designation'], h=5, text='Designation', align="C", new_x="RIGHT" if 'rate' in self.width_of_columns else "LMARGIN", new_y='TOP' if 'rate' in self.width_of_columns else "NEXT", border=1)
        if 'rate' in self.width_of_columns:
            self.cell(w=self.width_of_columns['rate'], h=5, text='Rate', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        self.set_line_width(0.2)

    # def print_cell(self, text, width):
    #     formatted_text = format_text(text, self.width_of_columns)
    #     self.cell(w=width, h=self.default_cell_height, txt=formatted_text, align="C", border=1)

    def cell(self, w=None, h=None, text='', border=0, align="L", fill=False, link='', center=False, markdown=False, new_x='RIGHT', new_y='TOP', length_check=False):
        if text and length_check:
            max_width_mm = w
            formatted_text = format_text(text, max_width_mm, self)
            super().cell(w=w, h=h, text=formatted_text, border=border, align=align, fill=fill, link=link, center=center, markdown=markdown, new_x=new_x, new_y=new_y)
        else:
            super().cell(w=w, h=h, text=text, border=border, align=align, fill=fill, link=link, center=center, markdown=markdown, new_x=new_x, new_y=new_y)

def generate_strength_report(user, request_data, employees):
    print(request_data['filters']['salary_rate'])
    width_of_columns = {
        "serial_number": 8,
        "paycode": 14,
        "employee_name": 40,
        "father_name": 40,
        "doj": 15,
        "resignation_date": 15,
        "department": 25,
        "designation": 25,
        "rate": 15,
    }
    if request_data['filters']['salary_rate']=='without_salary_rate':
        width_of_columns.pop("rate")
        width_of_columns['paycode'] = 15
        width_of_columns['employee_name'] = 42
        width_of_columns['father_name'] = 42
        width_of_columns['department'] = 30
        width_of_columns['designation'] = 30
        
    default_cell_height = 5
    default_cell_height_large = 7
    default_row_number_of_cells = 1
    left_margin = 6
    right_margin = 7
    bottom_margin = 8

    company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    strength_report = FPDF(width_of_columns=width_of_columns, from_date=request_data['from_date'], to_date=request_data['to_date'],company_name=employees[0].company.name,company_address=company_details[0].address if company_details.exists() else '', orientation="P", unit="mm", format="A4")

    #Page settings
    strength_report.set_margins(left=left_margin, top=6, right=right_margin)
    strength_report.add_page()
    strength_report.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": strength_report.get_x(), "y": strength_report.get_y()}

    for index, employee in enumerate(employees):
        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = employee.employee_professional_detail.department
                previous_employee_department = employees[index-1].employee_professional_detail.department if index!=0 else None
                if index == 0 or current_employee_department != previous_employee_department:
                    strength_report.set_font("Helvetica", size=10, style="B")
                    strength_report.cell(w=0, h=default_cell_height_large, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
            except:
                pass

        strength_report.set_font("Helvetica", size=6)
        #Serial
        strength_report.cell(w=width_of_columns['serial_number'], h=default_cell_height, text=f'{index+1}', new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #Paycode
        strength_report.cell(w=width_of_columns['paycode'], h=default_cell_height, text=f'{employee.paycode}', new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #Employee Name
        strength_report.cell(w=width_of_columns['employee_name'], h=default_cell_height, text=f'{employee.name}', new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #Father's Name
        strength_report.cell(w=width_of_columns['father_name'], h=default_cell_height, text=f"{employee.father_or_husband_name if employee.father_or_husband_name else ''}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #DOJ
        date_of_joining = None
        try: date_of_joining = employee.employee_professional_detail.date_of_joining
        except: pass
        strength_report.cell(w=width_of_columns['doj'], h=default_cell_height, text=f"{date_of_joining.strftime('%d-%b-%Y') if date_of_joining else ''}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #Resignation Date
        resignation_date = None
        try: resignation_date = employee.employee_professional_detail.resignation_date
        except: pass
        strength_report.cell(w=width_of_columns['resignation_date'], h=default_cell_height, text=f"{resignation_date.strftime('%d-%b-%Y') if resignation_date else ''}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        #Department
        department = None
        try: department = employee.employee_professional_detail.department
        except: pass
        strength_report.cell(w=width_of_columns['department'], h=default_cell_height, text=f"{department.name if department else ''}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)

        #Designation
        designation = None
        try: designation = employee.employee_professional_detail.designation
        except: pass
        strength_report.cell(w=width_of_columns['designation'], h=default_cell_height, text=f"{designation.name if designation else ''}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)
        
        if 'rate' in width_of_columns:
            #Total Rate or Wages
            total_earnings_rate = None
            try:
                total_earnings_rate = 0
                earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
                employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee).order_by('-from_date', 'earnings_head__id')
                for head in earnings_heads:
                    salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head).order_by('-from_date')
                    if salary_for_particular_earning_head.exists():
                        total_earnings_rate += salary_for_particular_earning_head.first().value
            except: 
                pass
            strength_report.cell(w=width_of_columns['rate'], h=default_cell_height, text=f"{total_earnings_rate}", new_x="RIGHT", new_y="TOP", align='L', length_check=True, border=1)

        strength_report.set_xy(x=left_margin, y=strength_report.get_y() + default_cell_height)

    strength_report.set_font('Helvetica', 'B', 8)
    strength_report.set_line_width(0.5)
    strength_report.cell(w=0, h=default_cell_height_large, text=f"Total Employees:    {len(employees)}", new_x="RIGHT", new_y="TOP", align='L', border=1)






    # Save the pdf with name .pdf
    buffer = bytes(strength_report.output())
    yield buffer