from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

#A4 size 210 x 297 mm
width_of_columns = {
        "serial_number": 8,
        "paycode": 21,
        "acn": 21,
        "employee_name": 50,
        "father_name": 50,
        "designation": 35,
        "status": 12
    }

def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix

class FPDF(FPDF):
    def __init__(self, my_date, company_name, company_address, *args, **kwargs):
        self.my_date = my_date
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
        day_suffix = get_day_suffix(self.my_date.day)
        self.cell(w=None, h=6, text=self.my_date.strftime(f"Absent Report for the day of %e{day_suffix} %B, %Y  |  %A"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        #Printing the column headers
        self.set_font('Helvetica', 'B', 8)
        self.set_line_width(0.5)
        self.cell(w=width_of_columns['serial_number'], h=5, text='S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['paycode'], h=5, text='Paycode', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['acn'], h=5, text='ACN', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['employee_name'], h=5, text='Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['father_name'], h=5, text="Father's Name", align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['designation'], h=5, text='Designation', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['status'], h=5, text='Status', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        self.set_line_width(0.2)

def generate_absent_report(request_data, absent_employees_attendance):
    default_cell_height = 5
    default_cell_height_large = 7
    default_row_number_of_cells = 1
    left_margin = 6
    right_margin = 7
    bottom_margin = 8

    company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    absent_report = FPDF(my_date=date(request_data['year'], request_data['month'], request_data['filters']['date']),company_name=absent_employees_attendance[0].company.name,company_address=company_details[0].address if (company_details.exists() and company_details[0].address != None) else '    ', orientation="P", unit="mm", format="A4")

    #Page settings
    absent_report.set_margins(left=left_margin, top=6, right=right_margin)
    absent_report.add_page()
    absent_report.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": absent_report.get_x(), "y": absent_report.get_y()}
    absent_report.set_font("Helvetica", size=8)

    for employee_index, attendance in enumerate(absent_employees_attendance):
        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = attendance.employee.employee_professional_detail.department
                previous_employee_department = absent_employees_attendance[employee_index-1].employee.employee_professional_detail.department if employee_index!=0 else None
                if employee_index == 0 or current_employee_department != previous_employee_department:
                    absent_report.set_font("Helvetica", size=10, style="B")
                    absent_report.cell(w=0, h=default_cell_height_large, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
            except:
                pass
        absent_report.set_font("Helvetica", size=8, style="")
        #Serial Number
        absent_report.cell(w=width_of_columns['serial_number'], h=default_cell_height*default_row_number_of_cells, text=f'{employee_index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Paycode
        absent_report.cell(w=width_of_columns['paycode'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.paycode}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #ACN
        absent_report.cell(w=width_of_columns['acn'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.attendance_card_no}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Employee Name
        absent_report.multi_cell(w=width_of_columns['employee_name'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.name}', align="L", new_x="RIGHT", new_y='TOP', border=1)
        
        #Father's Name
        absent_report.multi_cell(w=width_of_columns['father_name'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.father_or_husband_name or ""}', align="L", new_x="RIGHT", new_y='TOP', border=1)
        
        #Designation
        employee_designation = None
        try:
            employee_designation = attendance.employee.employee_professional_detail.designation
        except: pass
        absent_report.multi_cell(w=width_of_columns['designation'], h=default_cell_height*default_row_number_of_cells, text=f'{employee_designation.name if employee_designation!=None else ""}', align="L", new_x="RIGHT", new_y='TOP', border=1)

       #Status
        absent_report.multi_cell(w=width_of_columns['status'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.first_half.name}-{attendance.second_half.name}', align="C", new_x="LMARGIN", new_y='NEXT', border=1)



    # Save the pdf with name .pdf
    buffer = bytes(absent_report.output())
    yield buffer
