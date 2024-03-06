from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING


width_of_columns = {
        "serial_number": 8,
        "paycode": 18,
        "employee_name": 40,
        "designation": 30,
        "total_rate": 15,
        "ot_hrs": 10,
        "ot_amount": 15,
        "esi_on_ot": 10,
        "net_amount": 15,
        "signature": 35,
    }

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
        self.cell(w=None, h=6, text=self.my_date.strftime("OT Sheet for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        #Printing the column headers
        self.set_font('Helvetica', 'B', 8)
        self.set_line_width(0.5)
        self.cell(w=width_of_columns['serial_number'], h=5, text='S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['paycode'], h=5, text='Paycode', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['employee_name'], h=5, text='Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['designation'], h=5, text='Designation', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['total_rate'], h=5, text='Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['ot_hrs'], h=5, text='OT Hrs', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['ot_amount'], h=5, text='OT Amt.', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['esi_on_ot'], h=5, text='ESI', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['net_amount'], h=5, text='Net Amt.', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['signature'], h=5, text='Signature', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        self.set_line_width(0.2)


def generate_overtime_sheet(user, request_data, employee_salaries):
    
    default_cell_height = 5
    default_row_number_of_cells = 3
    left_margin = 6
    right_margin = 7
    bottom_margin = 8
    

    company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    overtime_sheet = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=employee_salaries[0].company.name,company_address=company_details[0].address if company_details.exists() else '', orientation="P", unit="mm", format="A4")

    #Page settings
    overtime_sheet.set_margins(left=left_margin, top=6, right=right_margin)
    overtime_sheet.add_page()
    overtime_sheet.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": overtime_sheet.get_x(), "y": overtime_sheet.get_y()}
    overtime_sheet.set_font("Helvetica", size=8)

    grand_total_dict = {
        'ot_amount': 0,
        'esi_on_ot': 0,
        'net_ot_amount': 0
    }

    for employee_index, salary in enumerate(employee_salaries):
        #Serial Number
        overtime_sheet.cell(w=width_of_columns['serial_number'], h=default_cell_height*default_row_number_of_cells, text=f'{employee_index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Paycode
        overtime_sheet.cell(w=width_of_columns['paycode'], h=default_cell_height*default_row_number_of_cells, text=f'{salary.employee.paycode}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Employee Name
        employee_name_width = overtime_sheet.get_string_width(salary.employee.name)
        employee_name_cell_height = default_cell_height*default_row_number_of_cells
        if employee_name_width > width_of_columns['employee_name']:
            employee_name_cell_height = default_cell_height*default_row_number_of_cells/2
        overtime_sheet.multi_cell(w=width_of_columns['employee_name'], h=employee_name_cell_height, text=f'{salary.employee.name}', align="L", new_x="RIGHT", new_y='TOP', border=1)
        
        #Designation
        employee_designation_name = salary.employee.employee_professional_detail.designation.name if salary.employee.employee_professional_detail.designation else ''
        designation_width = overtime_sheet.get_string_width(employee_designation_name)
        designation_cell_height = default_cell_height*default_row_number_of_cells
        if designation_width > width_of_columns['designation']:
            designation_cell_height = default_cell_height*default_row_number_of_cells/2
        overtime_sheet.multi_cell(w=width_of_columns['designation'], h=designation_cell_height, text=f'{employee_designation_name}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Rate
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(from_date__lte=salary.date, to_date__gte=salary.date, employee=salary.employee.id).order_by('earnings_head__id')
        total_earnings_rate = 0
        for salary_rate in employee_salary_rates:
            total_earnings_rate += salary_rate.value
        overtime_sheet.cell(w=width_of_columns['total_rate'], h=default_cell_height*default_row_number_of_cells, text=f'{total_earnings_rate}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Hrs
        overtime_sheet.cell(w=width_of_columns['ot_hrs'], h=default_cell_height*default_row_number_of_cells, text=f'{salary.net_ot_minutes_monthly/60}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Amount
        ot_amount = salary.net_ot_amount_monthly
        grand_total_dict["ot_amount"] += ot_amount
        overtime_sheet.cell(w=width_of_columns['ot_amount'], h=default_cell_height*default_row_number_of_cells, text=f'{ot_amount}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #ESI on OT
        company_pf_esi_details = salary.company.pf_esi_setup_details
        esiable_amount = 0
        if salary.employee.employee_pf_esi_detail.esi_on_ot or user.role=='REGULAR':
            esiable_amount = min(company_pf_esi_details.esi_employee_limit, salary.net_ot_amount_monthly)
        esi_deducted = Decimal(esiable_amount) * Decimal(company_pf_esi_details.esi_employee_percentage) / Decimal(100)
        esi_deducted = esi_deducted.quantize(Decimal('1.'), rounding=ROUND_CEILING)
        grand_total_dict['esi_on_ot'] += esi_deducted
        overtime_sheet.cell(w=width_of_columns['esi_on_ot'], h=default_cell_height*default_row_number_of_cells, text=f'{esi_deducted}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Net Amount
        employee_net_ot_amount = salary.net_ot_amount_monthly-esi_deducted
        grand_total_dict['net_ot_amount'] += employee_net_ot_amount
        overtime_sheet.cell(w=width_of_columns['net_amount'], h=default_cell_height*default_row_number_of_cells, text=f'{employee_net_ot_amount}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #Signature
        overtime_sheet.cell(w=width_of_columns['signature'], h=default_cell_height*default_row_number_of_cells, text=f'', align="R", new_x="LMARGIN", new_y='NEXT', border=1)

        if employee_index == len(employee_salaries)-1:
            #A4 size 210 x 297 mm
            if 297-overtime_sheet.get_y()-bottom_margin>=default_cell_height:
                overtime_sheet.set_font("Helvetica",style='B', size=8)
                overtime_sheet.rect(x=overtime_sheet.get_x(), y=overtime_sheet.get_y(), w=width_of_columns['serial_number']+width_of_columns['paycode']+width_of_columns['employee_name']+width_of_columns['designation']+width_of_columns['total_rate']+width_of_columns['ot_hrs']+width_of_columns['ot_amount']+width_of_columns['esi_on_ot']+width_of_columns['net_amount'], h=default_cell_height)
                overtime_sheet.cell(w=None, h=default_cell_height, text=f'Grand Total', align="L", new_x="LEFT", new_y='TOP', border=0)
                overtime_sheet.set_xy(x=overtime_sheet.get_x()+width_of_columns['serial_number']+width_of_columns['paycode']+width_of_columns['employee_name']+width_of_columns['designation']+width_of_columns['total_rate']+width_of_columns['ot_hrs'], y=overtime_sheet.get_y())
                overtime_sheet.cell(w=width_of_columns['ot_amount'], h=default_cell_height, text=f'{grand_total_dict["ot_amount"]}', align="R", new_x="RIGHT", new_y='TOP', border=1)
                overtime_sheet.cell(w=width_of_columns['esi_on_ot'], h=default_cell_height, text=f'{grand_total_dict["esi_on_ot"]}', align="R", new_x="RIGHT", new_y='TOP', border=1)
                overtime_sheet.cell(w=width_of_columns['net_amount'], h=default_cell_height, text=f'{grand_total_dict["net_ot_amount"]}', align="R", new_x="RIGHT", new_y='TOP', border=1)


    # Save the pdf with name .pdf
    buffer = bytes(overtime_sheet.output())
    yield buffer