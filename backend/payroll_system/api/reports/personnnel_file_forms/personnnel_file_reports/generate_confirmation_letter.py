import os
from dateutil.relativedelta import relativedelta

def generate_confirmation_letter(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "intro_headers": 25,
        # "placeholder": 75,
        "signature": 80
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
    report.set_font('noto-sans-devanagari', size=14, style="B")

    #Printing Heading
    report.cell(w=0, h=default_cell_height_for_heading, text='स्थायी नियुक्त्ति पत्र ', align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Top paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Company Name and address
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{employee.company.name}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    compnay_address = ''
    try: compnay_address = employee.company.company_details.address
    except: pass
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{compnay_address}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")

    #Main Body
    #Name
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*2) #blank line
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"कर्मचारी का नाम:", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Father Husband Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पिता पति का नाम:", align="L", new_x="RIGHT", new_y='TOP', border=0)
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

    #Main text
    employee_doj = ''
    employee_confirmation_date = ''
    next_day_after_confirmation_date = ''
    try: 
        employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
        employee_confirmation_date_obj = employee.employee_professional_detail.date_of_confirm
        employee_confirmation_date = employee_confirmation_date_obj.strftime('%d-%b-%Y')
        next_day_after_confirmation_date = (employee_confirmation_date_obj + relativedelta(days=1)).strftime('%d-%b-%Y')
    except: pass
    report.set_xy(x=report.get_x()+width_of_columns["paraindent"], y=report.get_y()+default_cell_height) #blank line
    report.cell(w=0, h=default_cell_height, text=f"आपको सूचित किया जाता है कि प्रबंधन ने आपको कम्पनी की सेवाओं में दिनांक    {employee_doj}    से दिनांक    {employee_confirmation_date}    तक परिवीक्षाकल पर रखा था |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपका कार्य एवं आचरण संतोष जनक रहा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x()+width_of_columns["paraindent"], y=report.get_y()+default_cell_height) #blank line
    report.cell(w=0, h=default_cell_height, text=f"अतः आपको कम्पनी में आज दिनांक    {next_day_after_confirmation_date}    से आपको स्थाई रूप से नियुक्त्त किया जाता है | आपको कम्पनी द्वारा दी गयी सुविधाओं को लेने का पूर्ण", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अधिकार होगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Signature and footers
    #A4: 210 x 297
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height))
    report.cell(w=None, h=footer_cell_height, text="कर्मचारी के हस्ताक्षर", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Bottom Right
    report.set_xy(x=210-width_of_columns['signature']-right_margin-left_margin, y=297-10-(footer_cell_height*3))
    report.cell(w=width_of_columns['signature'], h=footer_cell_height, text=f"For {employee.company.name}", align="R", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+footer_cell_height)
    report.cell(w=width_of_columns['signature'], h=footer_cell_height, text=f"अधिकृत हस्ताक्षरकर्ता", align="R", new_x="LEFT", new_y='NEXT', border=0)
