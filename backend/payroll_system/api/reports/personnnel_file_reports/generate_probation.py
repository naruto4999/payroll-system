import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time

def generate_probation(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "intro_headers": 25,
        "date": 40,
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
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*4) #Blank Line for letter head
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{employee.company.name}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    # #Top paycode
    # report.set_font('noto-sans-devanagari', size=9, style="")
    # report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    # report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Company Name and address
    company_address = ''
    try: company_address = employee.company.company_details.address
    except: pass
    report.set_font('noto-sans-devanagari', size=10, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{company_address}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Main Body
    report.set_font('noto-sans-devanagari', size=9, style="")
    #Name
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*2) #blank line
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"नाम:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Date
    report.set_xy(x=report.get_x()-width_of_columns['date'], y=report.get_y()) #blank line
    report.cell(w=0, h=default_cell_height, text=f"दिनांक: {datetime.now().date().strftime('%d-%b-%Y')}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Father Husband Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पिता / पति का नाम:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee.father_or_husband_name or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Designation
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पद:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee_designation}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Department
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"विभाग:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee_department}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Paycode
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पे कोड न०:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee.paycode}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line 
    #Subject
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"विषय : अस्थाई नियुक्त्ति अवधि बढ़ाने के बारे में |", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line 

    #Salutations
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"महोदय / महोदया,", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main letter body 
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y()+default_cell_height) #Blank Line 
    report.cell(w=0, h=default_cell_height, text=f"आपको नियुक्त्ति पत्र दिनांक    {employee_doj}   के संदार्भ में जिसमे आपको छः माह परखकाल के समय के लिए नियुक्त्ति किया था | परखकाल के दौरान हमने आपके", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"कार्य को भली भाँति परखा और इस नतीजे पर अये कि अभी आपकी सेवायें संतोषजनक नहीं पायी गयी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y()+default_cell_height) #Blank Line 
    report.cell(w=0, h=default_cell_height, text=f"यद्यपि प्रबंधन के पास यह अधिकार है कि आपकी सेवायें परखकाल के दौरान समाप्त कर सकता है | फिर भी यह निर्णय लिया गया है कि आपका परखकाल अगले तीन", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"माह के लिए बढ़ाया जाये | आपकी सेवा व शर्ते वही रहेगी जो आपके नियुक्त्ति पत्र में है | आपको सूचित किया जाता है कि जब तक आपको लिखित में पत्र नहीं मिलता तब तक", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आप प्रोबेशन पर ही रहेंगे / रहेंगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Signature and footers
    #A4: 210 x 297
    #Employee Signature
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height*3))
    report.cell(w=0, h=footer_cell_height, text="कर्मचारी के हस्ताक्षर", align="L", new_x="RIGHT", new_y='TOP', border=0)
    #Company Name
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=footer_cell_height, text=f"कृते {employee.company.name}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Employee Name
    report.set_xy(x=report.get_x(), y=report.get_y()+footer_cell_height)
    report.cell(w=0, h=footer_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    #Authorised Signature
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=footer_cell_height, text=f"कर्मचारी व प्रशासन", align="R", new_x="LMARGIN", new_y='NEXT', border=0)
