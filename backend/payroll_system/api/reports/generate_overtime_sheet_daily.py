from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount, EarningsHead
from datetime import date, time
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
import calendar

#A4 size 210 x 297 mm
width_of_columns = {
        "serial_number": 8,
        "paycode": 20,
        "acn": 20, 
        "employee_name": 66,
        "designation": 50,
        "shift": 20,
        "in_time": 14,
        "out_time": 14,
        "ot_hrs": 14,
        "late_hrs": 14,
        "status": 12,
        "rate": 16,
        "ot_amount":16
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
        self.cell(w=None, h=6, text=self.my_date.strftime(f"Overtime Report for the day of %e{day_suffix} %B, %Y  |  %A"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        #Printing the column headers
        self.set_font('Helvetica', 'B', 8)
        self.set_line_width(0.5)
        self.cell(w=width_of_columns['serial_number'], h=5, text='S/N', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['paycode'], h=5, text='Paycode', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['acn'], h=5, text='ACN', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['employee_name'], h=5, text='Employee Name', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['designation'], h=5, text='Designation', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['shift'], h=5, text='Shift', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['in_time'], h=5, text='In Time', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['out_time'], h=5, text='Out Time', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['ot_hrs'], h=5, text='O.T Hrs', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['late_hrs'], h=5, text='Ded. Hrs', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['status'], h=5, text='Status', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['rate'], h=5, text='Rate', align="C", new_x="RIGHT", new_y='TOP', border=1)
        self.cell(w=width_of_columns['ot_amount'], h=5, text='Amount', align="C", new_x="LMARGIN", new_y='NEXT', border=1)
        self.set_line_width(0.2)

def generate_overtime_sheet_daily(request_data, employees_attendances_with_ot):
    default_cell_height = 5
    default_cell_height_large = 7
    default_row_number_of_cells = 1
    left_margin = 6
    right_margin = 7
    bottom_margin = 8

    company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    overtime_sheet_daily = FPDF(my_date=date(request_data['year'], request_data['month'], request_data['filters']['date']),company_name=employees_attendances_with_ot[0].company.name,company_address=company_details[0].address if company_details.exists() else '', orientation="L", unit="mm", format="A4")

    #Page settings
    overtime_sheet_daily.set_margins(left=left_margin, top=6, right=right_margin)
    overtime_sheet_daily.add_page()
    overtime_sheet_daily.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": overtime_sheet_daily.get_x(), "y": overtime_sheet_daily.get_y()}
    overtime_sheet_daily.set_font("Helvetica", size=8)

    for employee_index, attendance in enumerate(employees_attendances_with_ot):
        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = attendance.employee.employee_professional_detail.department
                previous_employee_department = employees_attendances_with_ot[employee_index-1].employee.employee_professional_detail.department if employee_index!=0 else None
                if employee_index == 0 or current_employee_department != previous_employee_department:
                    overtime_sheet_daily.set_font("Helvetica", size=10, style="B")
                    overtime_sheet_daily.cell(w=0, h=default_cell_height_large, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
            except:
                pass
        overtime_sheet_daily.set_font("Helvetica", size=8, style="")
        #Serial Number
        overtime_sheet_daily.cell(w=width_of_columns['serial_number'], h=default_cell_height*default_row_number_of_cells, text=f'{employee_index+1}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Paycode
        overtime_sheet_daily.cell(w=width_of_columns['paycode'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.paycode}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #ACN
        overtime_sheet_daily.cell(w=width_of_columns['acn'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.attendance_card_no}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Employee Name
        overtime_sheet_daily.multi_cell(w=width_of_columns['employee_name'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.employee.name}', align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Designation
        designation = None
        try: designation = attendance.employee.employee_professional_detail.designation
        except: pass
        overtime_sheet_daily.multi_cell(w=width_of_columns['designation'], h=default_cell_height*default_row_number_of_cells, text=f"{designation.name if designation else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)

        #Shift
        ot_sheet_date = date(request_data['year'], request_data['month'], request_data['filters']['date'])
        shift = None
        try: shift = attendance.employee.shifts.filter(from_date__lte=ot_sheet_date, to_date__gte=ot_sheet_date).first()
        except: pass
        overtime_sheet_daily.cell(w=width_of_columns['shift'], h=default_cell_height*default_row_number_of_cells, text=f"{shift.shift.name if shift else ''}", align="C", new_x="RIGHT", new_y='TOP', border=1)

        #In time
        in_time = attendance.machine_in.strftime('%H:%M') if attendance.machine_in else ''
        if attendance.manual_in:
            in_time = attendance.manual_in.strftime('%H:%M')
        overtime_sheet_daily.cell(w=width_of_columns['in_time'], h=default_cell_height*default_row_number_of_cells, text=f'{in_time}', align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #Out time
        out_time = attendance.machine_out.strftime('%H:%M') if attendance.machine_out else ''
        if attendance.manual_out:
            out_time = attendance.manual_out.strftime('%H:%M')
        overtime_sheet_daily.cell(w=width_of_columns['out_time'], h=default_cell_height*default_row_number_of_cells, text=f'{out_time}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #OT Hrs
        overtime_hrs = attendance.ot_min
        overtime_formatted = ''
        if overtime_hrs:
            hours, minutes = divmod(overtime_hrs, 60)
            overtime_formatted = f"{hours:02d}:{minutes:02d}"
        overtime_sheet_daily.cell(w=width_of_columns['ot_hrs'], h=default_cell_height*default_row_number_of_cells, text=f'{overtime_formatted}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Late Hrs
        late_hrs = attendance.late_min
        late_hrs_str = ''
        if late_hrs and attendance.employee.employee_salary_detail.late_deduction:
            hours, minutes = divmod(late_hrs, 60)
            late_hrs_str = f"{hours:02d}:{minutes:02d}"
        overtime_sheet_daily.cell(w=width_of_columns['late_hrs'], h=default_cell_height*default_row_number_of_cells, text=f'{late_hrs_str}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Status
        overtime_sheet_daily.cell(w=width_of_columns['status'], h=default_cell_height*default_row_number_of_cells, text=f'{attendance.first_half.name}-{attendance.second_half.name}', align="C", new_x="RIGHT", new_y='TOP', border=1)

        #Salary Rate
        total_earnings_rate = None
        try:
            total_earnings_rate = 0
            earnings_heads = EarningsHead.objects.filter(company=attendance.company, user=attendance.user)
            employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=attendance.employee, from_date__lte=attendance.date, to_date__gte=attendance.date)
            for head in earnings_heads:
                salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                if salary_for_particular_earning_head.exists():
                    total_earnings_rate += salary_for_particular_earning_head.first().value
        except: 
            pass
        overtime_sheet_daily.cell(w=width_of_columns['rate'], h=default_cell_height*default_row_number_of_cells, text=f'{total_earnings_rate}', align="R", new_x="RIGHT", new_y='TOP', border=1)

        #OT Amount
        late_hrs = late_hrs if late_hrs !=None else 0
        overtime_hrs_after_late_deduction = overtime_hrs
        overtime_amount = 0
        overtime_rate_multiplier = 2 if attendance.employee.employee_salary_detail.overtime_rate == 'D' else 1
        if attendance.employee.employee_salary_detail.late_deduction:
            overtime_hrs_after_late_deduction -= ((late_hrs//30)*30 )+ (30 if late_hrs%30 >= 20 else 0)
        company_calculations = attendance.employee.company.calculations
        days_in_month = calendar.monthrange(request_data['year'], request_data['month'])[1]
        if company_calculations.ot_calculation == 'month_days':
            overtime_divisor = Decimal(days_in_month)
        else:
            overtime_divisor = Decimal(company_calculations.ot_calculation)
        rate = Decimal(total_earnings_rate)
        overtime_amount += (rate/overtime_divisor/Decimal(8) * Decimal(overtime_rate_multiplier)) * Decimal(overtime_hrs_after_late_deduction)/Decimal(60)
        overtime_amount = overtime_amount.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        overtime_sheet_daily.cell(w=width_of_columns['ot_amount'], h=default_cell_height*default_row_number_of_cells, text=f'{overtime_amount}', align="R", new_x="LMARGIN", new_y='NEXT', border=1)



    # Save the pdf with name .pdf
    buffer = bytes(overtime_sheet_daily.output())
    yield buffer