import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time
from ...models import EmployeeSalaryEarning, EarningsHead

def generate_appointment_letter_front_hindi(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 4
    default_cell_height_large = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "serial": 5,
        "intro_headers": 32,
        "intro_values": (210-left_margin-right_margin-(32*2))/2,
        "date": 100,
        "employee_address": 70,
        "salary_headers": 30,
        "salary_values": 35,
        # "placeholder": 75,
        "signature": 100
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
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{employee.company.name}", align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Top paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Company Name and address
    company_address = ''
    try: company_address = employee.company.company_details.address
    except: pass
    report.set_font('noto-sans-devanagari', size=10, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{company_address}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Heading
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"नियुक्त्ति पत्र", align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Main Line
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.write(h=default_cell_height, text=f"आपको नौकरी के लिए आवेदन पत्र और साक्षात्कार (इंटरव्यू ) के संदर्भ में आपकी    ")
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.write(h=default_cell_height, text=f"{employee_designation}")
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"  पद के लिए नियुक्त्ति करते हुए हमें हर्ष होता है | ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    ##Employee Details
    #Name
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Father/Husband Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"पिता / पति का नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee.father_or_husband_name if employee.father_or_husband_name != None else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Local Address
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"अस्थायी पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    
    #Permanent Address
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"स्थायी पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #DOB
    employee_dob = ''
    try: employee_dob = employee.dob.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"जन्म तिथि :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_dob}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #DOJ
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"काम शुरू करने की तारीख :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Designation and Department
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"पद :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_designation}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"विभाग :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_department}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"श्रेणी :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"(अकुशल, अर्द्धकुशल, कुशल, अतिकुशल)", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Salary Wage
    total_earnings_rate = None
    try:
        total_earnings_rate = 0
        earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee).order_by('from_date', 'earnings_head__id')
        for head in earnings_heads:
            salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head).order_by('from_date')
            if salary_for_particular_earning_head.exists():
                total_earnings_rate += salary_for_particular_earning_head.first().value
    except: 
        pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"वेतन :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{total_earnings_rate if total_earnings_rate else ''} /-    प्रति माह / रोज़ाना / पीस रेट के आधार पर", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # #Main Body
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_large, text=f"नियुक्त्ति की शर्तें", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")

    #1.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"1.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आप 6 महीने तक अस्थाई / प्रोबेशन पर नियुक्त्त रहेंगे | ज़रुरत पड़ने पर यह अवधि 6 महीने के लिए दोबारा बढ़ाई जा सकती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #2.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"2.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अस्थाई / प्रोबेशन कार्यालय या बढाई गयी अस्थाई / प्रोबेशन कार्यालय, के दौरान आपको यह अधिकार होगा कि आप बिना किसी सूचना (नोटिस) दिए नौकरी छोड़ सकते हैं |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"इस अस्थाई / प्रोबेशन के दौरान कम्पनी को भी अधिकार होगा कि वह आपको बिना किसी सूचना (नोटिस) के नौकरी छोड़ने के लिए कह सकती है |", align="L", new_x="LEFT", new_y='NEXT', border=0)

    # #2.
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    # report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"2.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    # report.cell(w=0, h=default_cell_height, text=f"", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # #Page
    # report.set_xy(x=210-width_of_columns['signature']-right_margin, y=297-8-default_cell_height)
    # report.set_font('noto-sans-devanagari', size=7, style="")
    # report.cell(w=0, h=default_cell_height, text=f"Page 1 of 2", align="R", new_x="RIGHT", new_y='TOP', border=0)
