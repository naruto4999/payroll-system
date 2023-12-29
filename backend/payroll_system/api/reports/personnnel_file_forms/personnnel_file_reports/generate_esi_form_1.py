import os
# from datetime import datetime, date, time
# from dateutil.relativedelta import relativedelta
from ....models import EmployeeFamilyNomineeDetial


def generate_esi_form_1(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    default_intro_cell_height = 5
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        "intro_headers": 35,
        "registration_details_headers": 36.5,
        "registration_details_values": ((210-right_margin-left_margin)-(36.5*2))/2,
        # "placeholder": 100,
        "signature": 70,
        "family_photo": 124,
        #Table 1
        # "family_details_serial": 7,
        "family_details_name": 60,
        "family_details_relation": 30,
        "family_details_dob": 18,
        "residing": 15,
        "family_details_address": 210-left_margin-right_margin-60-30-18-15,
        #Table 2
        "nominees_name": 60,
        "nominees_relation": 30,
        "percentage": 18,
        "nominee_address": 210-left_margin-right_margin-60-30-18,
        "phone_number": 25

    }

    # Get the current script's directory
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    
    # Specify the relative path to the font file
    noto_sans_dev_regular = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Regular.ttf')
    noto_sans_dev_bold = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Bold.ttf')

    #Adding Hindi Font
    report.add_font("noto-sans-devanagari",fname=noto_sans_dev_regular)
    report.add_font("noto-sans-devanagari", fname=noto_sans_dev_bold, style="B")
    report.set_text_shaping(True)
    report.add_page()
    report.set_font('noto-sans-devanagari', size=12, style="B")

    #Printing Logo of ESI
    #A4 size in millimeters: 210 x 297 mm.
    parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
    logo_path = os.path.join(parent_directory, 'logo', 'esic_logo.png')
    # report.rect(x=report.get_x(), y=report.get_y(), w=30, h=30)
    if logo_path:
        report.image(logo_path, x=report.get_x(), y=report.get_y(), w=22, h=22)

    #Printing Heading
    report.cell(w=0, h=default_cell_height_for_heading, text="EMPLOYEES' STATE INSURANCE CORPORATION", align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text='TEMPORARY IDENTITY CERTIFICATE', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    ##Employee intro
    #Name
    # report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text='Insured Person:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    # report.set_font('noto-sans-devanagari', size=9, style="")
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text=f"{employee.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_intro_cell_height, text=f"Insured Person: {employee.name}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #ESI Number of the employee
    employee_esi_number = ''
    try: employee_esi_number = employee.employee_pf_esi_detail.esi_number
    except: pass
    # report.set_font('noto-sans-devanagari', size=9, style="B")
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text='Insurance No.:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    # report.set_font('noto-sans-devanagari', size=9, style="")
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text=f"{employee_esi_number if employee_esi_number else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_intro_cell_height, text=f"Insurance No.: {employee_esi_number if employee_esi_number else '                               '}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Date of Joining
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    # report.set_font('noto-sans-devanagari', size=9, style="B")
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text='Date of Registration:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    # report.set_font('noto-sans-devanagari', size=9, style="")
    # report.cell(w=width_of_columns['intro_headers'], h=default_intro_cell_height, text=f"{employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_intro_cell_height, text=f"Date of Registration: {employee_doj}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Your Registration Details
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_intro_cell_height, text=f"YOUR REGISTRATION DETAILS", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Name and Disability
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Employee Name :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Disability :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{'Yes' if employee.handicapped else 'No'}", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Father Husband Name and DOB
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Name of Father/Husband :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.father_or_husband_name if employee.father_or_husband_name else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Date of Birth :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.dob.strftime('%d-%b-%Y') if employee.dob else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Marital Status and Gender
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Marital Status :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.get_marital_status_display() or ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Gender :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.get_gender_display() or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    coordinates_before_address = {"x": report.get_x(), "y": report.get_y()}
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Local and Permanent Address 
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height*2, text=f"Present Address :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['registration_details_values'], h=default_cell_height*2)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
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
    report.multi_cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=text, align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height*2, text=f"Permanent Address :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
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
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['registration_details_values'], h=default_cell_height*2)
    report.multi_cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=text, align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=coordinates_before_address['x'], y=coordinates_before_address['y']+default_cell_height*2)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Dispensary
    employee_esi_dispensary = ''
    try: employee_esi_dispensary = employee.employee_pf_esi_detail.esi_dispensary
    except: pass
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Dispensary/IMP :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=0, h=default_cell_height, text=f"{employee_esi_dispensary if employee_esi_dispensary else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    #Current and Previous Employer Headers
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers']+width_of_columns['registration_details_values'], h=default_cell_height, text=f"Current Employer Details", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['registration_details_headers']+width_of_columns['registration_details_values'], h=default_cell_height, text=f"Previous Employer Details", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

    #Employer Code
    current_employer_code_no = ''
    try: current_employer_code_no = employee.company.pf_esi_setup_details.employer_esi_code
    except: pass
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Employer's Code No. :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{current_employer_code_no if current_employer_code_no else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Employer's Code No. :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text="", align="L", new_x="LMARGIN", new_y='NEXT', border=1)
    
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Sub Units Code
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Sub Units Code No. :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Sub Units Code No. :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text="", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #DOJ and Previous Insurance No.
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Date of Appointment :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee_doj}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Previous Insurance No. :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text="", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Company Name
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Name of Employer :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{employee.company.name}", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height, text=f"Name of Employer :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text="", align="L", new_x="LMARGIN", new_y='NEXT', border=1)

    coordinates_before_address = {"x": report.get_x(), "y": report.get_y()}
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    #Company Address
    compnay_address = ''
    try: compnay_address = employee.company.company_details.address
    except: pass
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height*2, text=f"Address of Employer :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['registration_details_values'], h=default_cell_height*2)
    report.multi_cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text=f"{compnay_address}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['registration_details_headers'], h=default_cell_height*2, text=f"Address of Employer :", align="L", new_x="RIGHT", new_y='TOP', border=1)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['registration_details_values'], h=default_cell_height*2)
    report.multi_cell(w=width_of_columns['registration_details_values'], h=default_cell_height, text="", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=coordinates_before_address['x'], y=coordinates_before_address['y']+default_cell_height*2)

    ##Family Details
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=0, h=default_cell_height, text=f"Family Details :", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    initial_coordinates_before_family_table_header = {"x": report.get_x(), "y": report.get_y()}
    ##Printing Family Details headers
    report.cell(w=width_of_columns['family_details_name'], h=default_cell_height_smaller*2, text=f"Name", align='C', new_x="RIGHT", new_y="TOP", border=1)
    
    report.cell(w=width_of_columns['family_details_relation'], h=default_cell_height_smaller, text=f"Relation with", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_relation'], h=default_cell_height_smaller, text=f"IP", align='C', new_x="RIGHT", new_y="TOP", border='BLR')

    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])
    report.cell(w=width_of_columns['family_details_dob'], h=default_cell_height_smaller, text=f"Date of", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_dob'], h=default_cell_height_smaller, text=f"Birth", align='C', new_x="RIGHT", new_y="TOP", border='BLR')

    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])
    report.cell(w=width_of_columns['residing'], h=default_cell_height_smaller, text=f"Is Residing", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['residing'], h=default_cell_height_smaller, text=f"With IP", align='C', new_x="RIGHT", new_y="TOP", border='BLR')

    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])
    report.cell(w=width_of_columns['family_details_address'], h=default_cell_height_smaller*2, text=f"Address", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

    ##Printing Family Details values
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    family_details = EmployeeFamilyNomineeDetial.objects.filter(employee=employee)
    print(f'Family Details: {family_details}')
    for index in range(6):
        family_member = None
        try: family_member = family_details[index]
        except: pass
        border = 1
        # if index==5:
        #     border='BLR'
        report.cell(w=width_of_columns['family_details_name'], h=default_cell_height_smaller, text=f"{family_member.name if family_member and family_member.name else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_relation'], h=default_cell_height_smaller, text=f"{family_member.relation if family_member and family_member.relation else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_dob'], h=default_cell_height_smaller, text=f"{family_member.dob.strftime('%d-%b-%Y') if family_member and family_member.dob else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['residing'], h=default_cell_height_smaller, text=f"{'Yes' if family_member and family_member.residing else 'No' if family_member else ''}", align='C', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_address'], h=default_cell_height_smaller, text=f"{family_member.address if family_member and family_member.address else ''}", align='L', new_x="LMARGIN", new_y="NEXT", border=border)

    ##Nominee Details
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=0, h=default_cell_height, text=f"Nominee Details :", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    ##Nominee Details headers
    initial_coordinates_before_nominee_table_header = {"x": report.get_x(), "y": report.get_y()}
    report.cell(w=width_of_columns['nominees_name'], h=default_cell_height_smaller*2, text=f"Name", align='C', new_x="RIGHT", new_y="TOP", border=1)
    
    report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller, text=f"Relation with", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller, text=f"IP", align='C', new_x="RIGHT", new_y="TOP", border='BLR')

    report.set_xy(x=report.get_x(), y=initial_coordinates_before_nominee_table_header['y'])
    report.cell(w=width_of_columns['percentage'], h=default_cell_height_smaller*2, text=f"Percentage", align='C', new_x="RIGHT", new_y="TOP", border=1)

    report.cell(w=width_of_columns['nominee_address'], h=default_cell_height_smaller*2, text=f"Address", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

    ##Nominee Details Values
    nominees = employee.employee_family_nominee_detail.filter(is_esi_nominee=True).order_by('id')
    for index in range(4):
        nominee = None
        try: nominee = nominees[index]
        except: pass
        nominee_name = nominee.name if nominee != None else ''
        nominee_address = nominee.address if nominee != None else ''
        nominee_relation = nominee.get_relation_display() if nominee else ''
        nominee_percentage = nominee.esi_nominee_share if nominee else ''
        report.cell(w=width_of_columns['nominees_name'], h=default_cell_height_smaller, text=f"{nominee_name}", align='L', new_x="RIGHT", new_y="TOP", border=1)
        report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller, text=f"{nominee_relation}", align='L', new_x="RIGHT", new_y="TOP", border=1)
        report.cell(w=width_of_columns['percentage'], h=default_cell_height_smaller, text=f"{nominee_percentage if nominee_percentage else ''}{' %' if nominee_percentage else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        report.cell(w=width_of_columns['nominee_address'], h=default_cell_height_smaller, text=f"{nominee_address}", align='L', new_x="LMARGIN", new_y="NEXT", border=1)



    ##Ending
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=0, h=default_cell_height_smaller, text=f"Documents Uploaded :", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"Please verify the above particulars.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"Please notify your employer or in the branch office address below incase of any information found incorrect", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.multi_cell(w=0, h=default_cell_height_smaller, text=f"To get permenent ID card, employee is requested to visit the following branch office to get biometric & photo captured by this date {employee_doj} in this branch office:  {employee_esi_dispensary if employee_esi_dispensary else '                                '}  , or any nearest ESIC Bio-metric camp locations", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.rect(x=report.get_x(), y=report.get_y()+default_cell_height_smaller, w=width_of_columns['signature'], h=default_cell_height_smaller*6)
    report.cell(w=width_of_columns['signature'], h=default_cell_height_smaller, text=f"Signature/LTI of Registered Employee/IP", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Family Photo box
    report.set_xy(x=210-right_margin-width_of_columns['family_photo'], y=report.get_y())
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['family_photo'], h=default_cell_height_smaller*7)
    report.set_font('noto-sans-devanagari', size=6, style="")
    report.cell(w=width_of_columns['family_photo'], h=default_cell_height_smaller, text=f"Affix your family photograph here (attested and stamped by Employer/ESIC Official)", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Employee Phone
    employee_phone_number = ''
    try: employee_phone_number = employee.phone_number
    except: pass
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller*6)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=width_of_columns['phone_number'], h=default_cell_height_smaller, text=f"Mobile Number :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=7.5, style="")
    report.cell(w=0, h=default_cell_height_smaller, text=f"{employee_phone_number if employee_phone_number else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Note
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=0, h=default_cell_height_smaller, text=f"Note:", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=6, style="")
    report.cell(w=0, h=default_cell_height_smaller, text=f"1. Please Keep this Printout for Future Reference and bring this along with you Photo ID Card for all your claim benefits and medical benefits.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"2. This copy should be retained with you until the biometric card is dispatched.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"3. Employer to please affix employee and his family photo here and attest with official stamp across.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=297-10-default_cell_height_smaller)
    report.set_font('noto-sans-devanagari', size=7.5, style="B")
    report.cell(w=0, h=default_cell_height_smaller, text=f"Signature/Stamp of ESIC Officer/Employer", align="R", new_x="LMARGIN", new_y='NEXT', border=0)
