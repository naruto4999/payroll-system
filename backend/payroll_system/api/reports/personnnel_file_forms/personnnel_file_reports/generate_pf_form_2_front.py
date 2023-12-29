import os
# from datetime import datetime, date, time
# from dateutil.relativedelta import relativedelta


def generate_pf_form_2_front(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 6
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        "placeholder": 100,
        "signature": 50,
        "intro": 47,
        "intro_values": (210-left_margin-right_margin-(47*2))/2,
        #Table
        "nominees_name": 40,
        "nominees_address": 58,
        "nominees_relation": 27,
        "nominees_dob": 18,
        "percentage": 24,
        "last_column": 30,
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
    primary_heading_width = report.get_string_width("NOMINATION AND DECLARATION") + 10 #padding
    print(f'String width: {primary_heading_width}')
    report.cell(w=0, h=default_cell_height_for_heading, text="NOMINATION AND DECLARATION", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=(210-primary_heading_width)/2, y=report.get_y(), w=primary_heading_width, h=default_cell_height_for_heading-0.75)

    #Form 2 Revised
    report.set_font('noto-sans-devanagari', size=9, style="")
    form_2_heading_width = report.get_string_width("Form-2 (Revised)") + 6 #padding
    report.set_xy(x=report.get_x()-(form_2_heading_width-3), y=report.get_y())
    report.cell(w=form_2_heading_width-3, h=default_cell_height_for_heading, text=f"Form-2 (Revised)", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=report.get_x()-form_2_heading_width, y=report.get_y(), w=form_2_heading_width, h=default_cell_height_for_heading-0.75)
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_for_heading) #NEXT line

    #Secondary Heading
    report.set_font('noto-sans-devanagari', size=11, style="B")
    secondary_heading_width = report.get_string_width("(FOR UNEXEMPTED/EXEMPTED ESTABLISHMENTS)") + 10 #padding
    report.cell(w=0, h=default_cell_height_for_heading, text='(FOR UNEXEMPTED/EXEMPTED ESTABLISHMENTS)', align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=(210-secondary_heading_width)/2, y=report.get_y(), w=secondary_heading_width, h=default_cell_height_for_heading-0.75)

    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main statement
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height) #Blank Line
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.multi_cell(w=0, h=default_cell_height, text="Declaration & Nomination Form under the Employee's Provident Funda and Employees Pension Schemes (Paragraph 33 & 61 (1) of Employees's Provident Fund Scheme, 1952 & Paragraph 18 of the Employee's Pension Scheme 1995) ", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height) #Blank Line
    report.set_font('noto-sans-devanagari', size=9, style="")
    ##Employee Intro
    #Name
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"1. Name (In block letters)", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.name.upper()}", align="L", new_x="RIGHT", new_y='TOP', border=0)

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
    serial_width = report.get_string_width("7. ")
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"8. Permanent Address", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x()+serial_width, y=report.get_y())
    report.multi_cell(w=width_of_columns['intro_values']+width_of_columns["intro"]-serial_width, h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y='TOP', border=0)

    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2) #Blank Line
    #Father Husband Name
    father_or_husband_name = None
    try: father_or_husband_name = employee.father_or_husband_name.upper()
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"2. Father's/Husband's Name", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{father_or_husband_name if father_or_husband_name else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #DOB
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"3. Date of Birth", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.dob.strftime('%d-%b-%Y') if employee.dob else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2) #Blank Line
    #Gender
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"4. Sex", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.get_gender_display() if employee.gender else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
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
    serial_width = report.get_string_width("7. ")
    # report.set_xy(x=report.get_x()+serial_width, y=report.get_y())
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"9. Temporary Address", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x()+serial_width, y=report.get_y())
    report.multi_cell(w=width_of_columns['intro_values']+width_of_columns["intro"]-serial_width, h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y='TOP', border=0)

    #Marital Status
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"5. Marital Status", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.get_marital_status_display() or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Account No
    employee_pf_no = None
    try: employee_pf_no = employee.employee_pf_esi_detail.pf_number.upper()
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"6. Account No.", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_pf_no if employee_pf_no else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #DOJ
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['intro'], h=default_cell_height, text=f"7. Date of Appointment", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2) #Blank Line
    #EPF Part A
    #Printing Heading
    report.set_font('noto-sans-devanagari', size=14, style="B")
    primary_heading_width = report.get_string_width("PART - A (EPF)") + 10 #padding
    print(f'String width: {primary_heading_width}')
    report.cell(w=0, h=default_cell_height_for_heading, text="PART - A (EPF)", align="C", new_x="LMARGIN", new_y='TOP', border=0)
    report.rect(x=(210-primary_heading_width)/2, y=report.get_y(), w=primary_heading_width, h=default_cell_height_for_heading-0.75)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2) #Blank Line
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.multi_cell(w=0, h=default_cell_height_smaller, text="I hereby nominate the person(s)/cancel the nomination made by me previously and nominate the person(s) mentioned below to receive the amount standing to by credit in the Employee's Provident Fund, in the event of my death.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    initial_coordinates_before_table_header = {"x": report.get_x(), "y": report.get_y()}
    report.set_font('noto-sans-devanagari', size=7, style="")
    #Table Headers
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_name'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['nominees_name'], h=default_cell_height_smaller*6/2, text="Name of the nominee / nominees", align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    report.multi_cell(w=width_of_columns['nominees_address'], h=default_cell_height_smaller*6, text="Address", align="C", new_x="RIGHT", new_y='TOP', border=1)

    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*6/3, text="Nominee's relationship with the member", align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_dob'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['nominees_dob'], h=default_cell_height_smaller*6, text="Date of Birth", align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['percentage'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['percentage'], h=default_cell_height_smaller*6/5, text="Total amt. or share of accumulations in Provident Funds paid to be paid to each nominee", align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['last_column'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['last_column'], h=default_cell_height_smaller, text="If the nominee is minor name and address of the guardian who may receive the amount during the minority of the nominee", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Table serials
    report.cell(w=width_of_columns['nominees_name'], h=default_cell_height_smaller, text="1", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['nominees_address'], h=default_cell_height_smaller, text="2", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller, text="3", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['nominees_dob'], h=default_cell_height_smaller, text="4", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['percentage'], h=default_cell_height_smaller, text="5", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['last_column'], h=default_cell_height_smaller, text="6", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

    #Nominee Table values
    nominees = employee.employee_family_nominee_detail.filter(is_pf_nominee=True).order_by('id')
    for index in range(4):
        nominee = None
        try: nominee = nominees[index]
        except: pass
        nominee_name = nominee.name if nominee != None else ''
        nominee_address = nominee.address if nominee != None and nominee.address else ''
        nominee_relation = nominee.get_relation_display() if nominee and  nominee.relation else ''
        nominee_dob = nominee.dob.strftime('%d-%b-%Y') if nominee and nominee.dob else ''
        nominee_percentage = nominee.pf_nominee_share if nominee and nominee.pf_nominee_share else ''
        #Nominee Name
        report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_name'], h=default_cell_height_smaller*3)
        report.multi_cell(w=width_of_columns['nominees_name'], h=default_cell_height_smaller, text=f"{nominee_name}", align='L', new_x="RIGHT", new_y="TOP", border=0)
        #Nominee Address
        report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_address'], h=default_cell_height_smaller*3)
        report.multi_cell(w=width_of_columns['nominees_address'], h=default_cell_height_smaller, text=f"{nominee_address}", align='L', new_x="RIGHT", new_y="TOP", border=0)
        #Nominee Relation
        report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*3, text=f"{nominee_relation}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #Nominee Age
        report.cell(w=width_of_columns['nominees_dob'], h=default_cell_height_smaller*3, text=f"{nominee_dob if nominee_dob else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #Nominee Share
        report.cell(w=width_of_columns['percentage'], h=default_cell_height_smaller*3, text=f"{nominee_percentage if nominee_percentage else ''}{' %' if nominee_percentage else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #If Nominee is a minor
        report.cell(w=width_of_columns['last_column'], h=default_cell_height_smaller*3, text=f"{''}", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

    
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    report.multi_cell(w=0, h=default_cell_height_smaller, text="1. Certified that I have no family as defined in para 2 (g) of the Employees Provident Fund Scheme 1952 and should I acquire a family hereafter the above nomination should be deemed as cancelled.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    report.multi_cell(w=0, h=default_cell_height_smaller, text="2. Certified that my father/mother is/are dependent upon me.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=297-10-default_cell_height_smaller)
    report.cell(w=0, h=default_cell_height_smaller, text="Strike out whichever is not applicable", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y()-default_cell_height_smaller)
    report.multi_cell(w=width_of_columns['signature'], h=default_cell_height_smaller, text="Signature/or thumb impression of the subscriber", align="L", new_x="RIGHT", new_y='TOP', border=0)