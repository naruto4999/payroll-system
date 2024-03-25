from fpdf import FPDF
from ..models import EmployeeSalaryPrepared, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, LeaveGrade, EmployeeGenerativeLeaveRecord, EmployeeMonthlyAttendanceDetails, CompanyDetails, EarningsHead, EmployeeSalaryEarning, EarnedAmount, PfEsiSetup
from datetime import date
from django.db.models import Case, When, Value, CharField
import math

width_of_columns = {
    "serial": 12,
    "acn": 25,
    "employee_name": 47,
    "father_husband_name": 47,
    "designation": 46,
    "advance": 20,
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
            self.cell(0, 6, self.my_date.strftime("Advance Report for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

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
                        
            #Advance
            self.cell(w=width_of_columns['advance'], h=10, text=f'Advance', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
            

def generate_advance_report(user, request_data, prepared_salaries):

    left_margin = 6
    right_margin = 7
    bottom_margin = 3
    top_margin = 6

    default_cell_height = 5
    default_heading_height = 10
    default_dept_heading_height = 8

    grand_total_dict = {
        "total_advance": 0,
    }

    dept_total_dict = {
        "total_advance": 0,
    }

    #Getting Company
    company = prepared_salaries[0].company
    company_address = ''
    try: company_address = company.company_details.address
    except: pass
    advance_report = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=company.name,company_address=company_address, orientation="P", unit="mm", format="A4")

    #Page settings
    advance_report.set_margins(left=left_margin, top=top_margin, right=right_margin)
    advance_report.add_page()
    advance_report.set_auto_page_break(auto=True, margin = bottom_margin)

    advance_report.set_font("Helvetica", size=7, style="")

    for index, salary in enumerate(prepared_salaries):
        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = salary.employee.employee_professional_detail.department
                previous_employee_department = prepared_salaries[index-1].employee.employee_professional_detail.department if index!=0 else None
                if index == 0 or current_employee_department != previous_employee_department:
                    advance_report.set_font("Helvetica", size=10, style="B")
                    advance_report.cell(w=0, h=default_dept_heading_height, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    advance_report.set_font("Helvetica", size=7, style="")
                    dept_total_dict = {
                        "total_advance": 0,
                    }
            except:
                pass

        #Serial
        advance_report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f'{index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #ACN
        advance_report.cell(w=width_of_columns['acn'], h=default_cell_height, text=f'{salary.employee.attendance_card_no}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Employee Name
        advance_report.cell(w=width_of_columns['employee_name'], h=default_cell_height, text=f'{salary.employee.name}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #F/H Name
        advance_report.cell(w=width_of_columns['father_husband_name'], h=default_cell_height, text=f'{salary.employee.father_or_husband_name or ""}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = None
        try: designation = salary.employee.employee_professional_detail.designation.name
        except: pass
        advance_report.cell(w=width_of_columns['designation'], h=default_cell_height, text=f"{designation if designation else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Advance
        advance_deducted = salary.advance_deducted
        # try:
        #     advance = salary.advance_deducted
        #     if  advance > 0:
        #         advance_deducted = advance
        # except:
        #     pass
        # if advance_deducted:
        grand_total_dict['total_advance'] += advance_deducted
        dept_total_dict['total_advance'] += advance_deducted
        advance_report.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{advance_deducted if advance_deducted else ''}", align="R", new_x="LMARGIN", new_y='NEXT', border=1)

        #Dept Total if applicable
        if request_data['filters']['group_by'] != 'none':
            if (index != len(prepared_salaries)-1 and salary.employee.employee_professional_detail.department != prepared_salaries[index+1].employee.employee_professional_detail.department) or (index == len(prepared_salaries)-1 and salary.employee.employee_professional_detail.department):
                advance_report.set_font("Helvetica", size=7, style="B")
                advance_report.set_line_width(0.4)
                advance_report.set_font("Helvetica", size=7, style="B")
                advance_report.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation'], h=default_cell_height, text=f"Department Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
                advance_report.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{dept_total_dict['total_advance']}", align="R", new_x="LMARGIN", new_y='NEXT', border="TB")
                advance_report.set_font("Helvetica", size=7, style="")
                advance_report.set_line_width(0.2)

    #Grand Total
    advance_report.set_line_width(0.4)
    advance_report.set_font("Helvetica", size=7, style="B")
    advance_report.cell(w=width_of_columns['serial']+width_of_columns['acn']+width_of_columns['employee_name']+width_of_columns['father_husband_name']+width_of_columns['designation'], h=default_cell_height, text=f"Grand Total", align="L", new_x="RIGHT", new_y='TOP', border="TB")
    advance_report.cell(w=width_of_columns['advance'], h=default_cell_height, text=f"{grand_total_dict['total_advance']}", align="R", new_x="RIGHT", new_y='TOP', border="TB")

    # Save the pdf with name .pdf
    buffer = bytes(advance_report.output())
    yield buffer