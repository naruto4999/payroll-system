import os
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from ...models import EmployeeSalaryEarning

def generate_employee_personal_details(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "intro": 80,
        "increment_cell": (210-left_margin-right_margin)/7,
        "signature": 80
    }

    # Get the current script's directory
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    # Specify the relative path to the font file
    noto_sans_dev_regular = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Regular.ttf')
    noto_sans_dev_bold = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Bold.ttf')

    #Adding Hindi Font
    report.add_font("noto-sans-devanagari",fname=noto_sans_dev_regular)
    report.add_font("noto-sans-devanagari", fname=noto_sans_dev_bold, style="B")
    report.set_text_shaping(True)
    report.add_page()
    report.set_font('noto-sans-devanagari', size=14, style="B")

    #Printing Heading
    report.cell(w=0, h=default_cell_height_for_heading, text='Employee Personal Details', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="")
    # report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    # report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)


    #Printing Photo if it exists
    #A4 size in millimeters: 210 x 297 mm.
    report.rect(x=210-right_margin-32, y=report.get_y(), w=32, h=35)
    if employee.photo != '':
        report.image(employee.photo, x=210-right_margin-32, y=report.get_y(), w=32, h=35)

    #Paycode
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Paycode: {employee.paycode}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #DOJ
    date_of_joining = None
    try: date_of_joining = employee.employee_professional_detail.date_of_joining
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"DOJ: {date_of_joining.strftime('%d-%b-%Y') if date_of_joining else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Name
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Name: {employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #DOB
    date_of_birth = None
    try: date_of_birth = employee.dob
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"DOB: {date_of_birth.strftime('%d-%b-%Y') if date_of_birth else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Father or husband name
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"F/H Name: {employee.father_or_husband_name if employee.father_or_husband_name else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Designation
    designation = None
    try: designation = employee.employee_professional_detail.designation
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Designation: {designation.name if designation else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)


    #Total Rate or Wages
    total_earnings_rate = None
    try:
        today = datetime.now() #Replace with date coming from backend later
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(from_date__lte=date(today.year, today.month, 1), to_date__gte=date(today.year, today.month, 1), employee=employee).order_by('earnings_head__id')
        total_earnings_rate = 0
        for index, salary_rate in enumerate(employee_salary_rates):
            total_earnings_rate += salary_rate.value
    except: 
        pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Wages: {total_earnings_rate if total_earnings_rate else ''} / month or day", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Department
    department = None
    try: department = employee.employee_professional_detail.department
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Department: {department.name if department else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Qualification
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"Qualification: {employee.get_education_qualification_display() or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Local Address
    text=''
    if employee.local_address:
        text += employee.local_address
    if employee.local_district:
        if len(text) !=0:
            text += ', '
        text += employee.local_district
    if employee.local_state_or_union_territory:
        if len(text) !=0:
            text += ', '
        text += employee.local_state_or_union_territory
    if employee.local_pincode:
        if len(text) !=0:
            text += ', '
        text += employee.local_pincode
    report.cell(w=0, h=default_cell_height, text=f"Local Address: {text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Permanent Address
    text=''
    if employee.permanent_address:
        text += employee.permanent_address
    if employee.permanent_district:
        if len(text) !=0:
            text += ', '
        text += employee.permanent_district
    if employee.permanent_state_or_union_territory:
        if len(text) !=0:
            text += ', '
        text += employee.permanent_state_or_union_territory
    if employee.permanent_pincode:
        if len(text) !=0:
            text += ', '
        text += employee.permanent_pincode
    report.cell(w=0, h=default_cell_height, text=f"Permanent Address: {text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)

    report.set_font('noto-sans-devanagari', size=14, style="B")

    #Promotion Heading
    report.cell(w=0, h=default_cell_height_for_heading, text='Increment and Promotion Details', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Headers
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=width_of_columns['increment_cell'], h=default_cell_height*2, text='With Effect From', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.multi_cell(w=width_of_columns['increment_cell'], h=default_cell_height, text=f'Annual\nIncrement', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['increment_cell'], h=default_cell_height*2, text='DA', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.multi_cell(w=width_of_columns['increment_cell'], h=default_cell_height, text=f'Revised\nWages', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.multi_cell(w=width_of_columns['increment_cell'], h=default_cell_height, text=f'Promotion\n(If Any)', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['increment_cell'], h=default_cell_height*2, text='Approved By', align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['increment_cell'], h=default_cell_height*2, text='Remarks', align="C", new_x="LMARGIN", new_y='NEXT', border=1)

    initial_coordinates_before_table = {"x": report.get_x(), "y": report.get_y()}
    for row in range(14):
        for column in range(7):
            report.rect(x=initial_coordinates_before_table['x']+(column*width_of_columns['increment_cell']), y=initial_coordinates_before_table['y']+(row*(default_cell_height*2)), w=width_of_columns['increment_cell'], h=default_cell_height*2)