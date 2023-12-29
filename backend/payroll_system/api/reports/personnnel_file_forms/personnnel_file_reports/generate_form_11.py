import os
# from datetime import datetime, date, time
# from dateutil.relativedelta import relativedelta


def generate_form_11(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 6
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        "placeholder_small": 70,
        # "placeholder_medium": 100,
        "signature": 70,
        "intro": 47,
        "intro_values": (210-left_margin-right_margin-(47*2))/2,
        "date": 60,
        #Table
        # "nominees_name": 40,
        # "nominees_address": 58,
        # "nominees_relation": 27,
        # "nominees_dob": 18,
        # "percentage": 24,
        # "last_column": 30,
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
    report.cell(w=0, h=default_cell_height_for_heading, text="EMPLOYEES' PROVIDENT FUND ORGANISATION", align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Form 2 Revised
    report.set_font('noto-sans-devanagari', size=10, style="B")
    form_2_heading_width = report.get_string_width("Form No. - 11") + 6 #padding
    report.set_xy(x=report.get_x()-(form_2_heading_width-3), y=report.get_y())
    report.cell(w=form_2_heading_width-3, h=default_cell_height_for_heading, text=f"Form No. - 11", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=report.get_x()-form_2_heading_width, y=report.get_y(), w=form_2_heading_width, h=default_cell_height_for_heading-0.75)
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_for_heading) #NEXT line

    #Secondary Heading
    report.cell(w=0, h=default_cell_height_for_heading, text="Employees' Provident Funds Scheme, 1952 (Paragraph 34 & 57) &", align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=10, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text="Employees' Provident Funds Scheme, 1995 (Paragraph 24)", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height_for_heading, text="(Declaration by a person taking up employment in any establishment on which EPF Scheme, 1952 and /or EPS, 1995 is applicable)", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main Body
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*2)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="1.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_small'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_small'], h=default_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f"Son/Wife/Daughter of Shri/Smt ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_small'], y2=report.get_y()+default_cell_height)

    report.set_xy(x=left_margin+width_of_columns['serial'], y=report.get_y()+default_cell_height) #NEXT line
    report.cell(w=0, h=default_cell_height, text=f"do hereby solemnly declare that: ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #*(a)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="*(a)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"I was employed in M/s  ______________________________________________________________________________________________________________________", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=7, style="B")
    report.cell(w=0, h=default_cell_height_smaller, text=f"(Name and Full Address of the Establishment)", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"and left service  _______________________________  period to that, I was employed in  _______________________________________________________", align="L", new_x="LEFT", new_y='NEXT', border=0)

    report.cell(w=0, h=default_cell_height, text=f"___________________________________________________________________________________  From  ________________________  To  ________________________", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #*(b)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="*(b)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"I was a member of  _______________________________________________________________________________________________________  Provident Fund", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"and also  ____________________________________________________  of the Pension Scheme  ________________________  To  ________________________", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"but not and my Account Number(s) was/were  _____________________________ / _____________________________ / _____________________________", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #*(c)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="*(c)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"I have/had not withdrawn the amount of my Provident Fund and Pension Fund.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #*(d)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="*(d)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"I have/had not drawn any superannuation benefits in respect of my past service from any employer.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #*(e)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text="*(e)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"I have/had never been a member of any Provident Fund and/or Pension Scheme.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*5)
    employee_doj = ''
    report.set_font('noto-sans-devanagari', size=9, style="B")
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"Signature of left/right hand thumb impression of the employee", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)

    report.set_line_width(0.4)
    report.line(x1=report.get_x(), y1=report.get_y(), x2=210-right_margin, y2=report.get_y())
    report.set_line_width(0.2)

    #After middle line
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)

    report.set_font('noto-sans-devanagari', size=9, style="")
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    # report.multi_cell(w=0, h=default_cell_height, text=f"Shri/Smt./Km.    {employee.name}    is appointed as    {employee_designation}    in M/s {employee.company.name}    with effect from    {employee_doj}    ")
    # report.multi_cell(
    #     w=0,
    #     h=default_cell_height,
    #     text=(
    #         f"Shri/Smt./Km. {employee.name} is appointed as {employee_designation} in "
    #         f"M/s <b>{employee.company.name}</b> with effect from {employee_doj}"
    #     )
    # )
    report.write(h=default_cell_height, text=f"Shri/Smt./Km. {employee.name} is appointed as {employee_designation} in ",)
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.write(h=default_cell_height, text=f"M/s {employee.company.name} ",)
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.write(h=default_cell_height, text=f"with effect from {employee_doj}",)

    #PF account number
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2)
    employee_pf_no = None
    try: employee_pf_no = employee.employee_pf_esi_detail.pf_number.upper()
    except: pass
    report.cell(w=0, h=default_cell_height, text=f"P.F A/c No. : {employee_pf_no if employee_pf_no else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*5)
    report.multi_cell(w=0, h=default_cell_height, text=f"(Left hand thumb impression on in the case of illiterate male member and right hand thumb impression in the case of illiterate female impression)", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2)
    report.set_xy(x=report.get_x(), y=297-10-default_cell_height*2)
    report.cell(w=width_of_columns['date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="RMARGIN", new_y='TOP', border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.multi_cell(w=width_of_columns['signature'], h=default_cell_height, text=f"Signature of the Employer or Manager or other authority officer of the establishment", align="L", new_x="RIGHT", new_y='TOP', border=0)
