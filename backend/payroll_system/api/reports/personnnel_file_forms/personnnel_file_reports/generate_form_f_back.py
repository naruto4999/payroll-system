import os
# from datetime import datetime, date, time
# from dateutil.relativedelta import relativedelta


def generate_form_f_back(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "headers": 60,
        "serial": 5,
        "paraindent": 10,
        "placeholder": 100,
        "place_date": 80,
        "signature": 70,
        "declaration_name": 120,
        "declaration_signature": 77,
        # #Table
        # "nominees_serial": 7,
        # "nominees_name_address": 130,
        # "nominees_relation": 30,
        # "nominees_age": 14,
        # "proportion": 16
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
    report.cell(w=0, h=default_cell_height_for_heading, text="Statement", align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.set_dash_pattern(dash=1, gap=1)
    #1 Employee Name
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='1.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Name of Employee in full:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee.name}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
   
    #2 Employee Gender
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='2.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Sex:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee.get_gender_display() if employee.gender else ''}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #3 Employee Religion
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='3.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Religion:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee.religion if employee.religion else ''}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #4 Employee Marital Status
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='4.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Marital Status:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee.get_marital_status_display() or ''}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #5 Department
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='5.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Department/Branch/Section where employed:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee_department}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #6 Designation
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='6.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Post held with Ticket No. or Serial No. if any:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee_designation}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #7 DOJ
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='7.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Date of Appointment:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{employee_doj}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)
    
    #8 Permanent Address
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
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='8.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=width_of_columns['headers'], h=default_cell_height, text='Permanent Address:', align="L", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)

    #Signature First
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*3)
    compnay_address = ''
    try: compnay_address = employee.company.company_details.address
    except: pass
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Place: {compnay_address}", align="L", new_x="LEFT", new_y="NEXT", border=0)
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="RMARGIN", new_y="TOP", border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"Signature/Thumb Impression of the employee", align="R", new_x="LMARGIN", new_y="NEXT", border=0)

    #Declaration by witness
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=11, style="B")
    report.cell(w=0, h=default_cell_height, text="Declaration by witness", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text="Nomination signed/thumb impressed before me", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=width_of_columns['declaration_name'], h=default_cell_height, text="Name in full and address", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['declaration_signature'], h=default_cell_height, text="Signature of witness", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    #1.
    report.cell(w=width_of_columns['declaration_name'], h=default_cell_height, text="1.", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['declaration_signature'], h=default_cell_height, text="1.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    #2.
    report.cell(w=width_of_columns['declaration_name'], h=default_cell_height, text="2.", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['declaration_signature'], h=default_cell_height, text="2.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #blank line
    
    #Address and Date
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Place: {compnay_address}", align="L", new_x="LEFT", new_y="NEXT", border=0)
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="LMARGIN", new_y="NEXT", border=0)


    #Certificate By the employer
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=11, style="B")
    report.cell(w=0, h=default_cell_height, text="Certificate by the employer", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text="Certificate that the particulars of the above nomination have been verified and record in this Employer's refrence number if any", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*3) #blank line
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="RMARGIN", new_y="TOP", border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"Authorized Signature", align="R", new_x="LMARGIN", new_y="NEXT", border=0)

    #Acknowlegement by the employer
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=11, style="B")
    report.cell(w=0, h=default_cell_height, text="Acknowlegement by the employer", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text="Received the duplicate of the nomination in Form 'F' filled by me and duty certified by the employer", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*3) #blank line
    report.cell(w=width_of_columns['place_date'], h=default_cell_height, text=f"Date: {employee_doj}", align="L", new_x="RMARGIN", new_y="TOP", border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"Signature/Thumb Impression of the employee", align="R", new_x="LMARGIN", new_y="NEXT", border=0)

    #Note
    #A4 210 x 297
    report.set_xy(x=report.get_x(), y=297-10-default_cell_height_smaller)
    report.cell(w=0, h=default_cell_height_smaller, text="Note: Strike out word/paragraph which are not applicable", align="L", new_x="RMARGIN", new_y='TOP', border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=default_cell_height_smaller, text="(Form 'F' Back)", align="R", new_x="RMARGIN", new_y='TOP', border=0)
