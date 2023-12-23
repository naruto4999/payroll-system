import os
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


def generate_pf_form_2_back(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 6
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        "placeholder": 100,
        "signature": 50,
        "authorised_signature": 65,
        "intro": 47,
        "intro_values": (210-left_margin-right_margin-(47*2))/2,
        #Table 1
        "family_serial": 12,
        "family_name_address": 210-left_margin-right_margin-18-30-12,
        "family_age": 18,
        "family_relation": 30,
        #Table
        "nominees_name_address": 210-left_margin-right_margin-18-30,
        "nominees_dob": 18,
        "nominees_relation": 30,
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
    primary_heading_width = report.get_string_width("PARA - B (EPS)") + 10 #padding
    print(f'String width: {primary_heading_width}')
    report.cell(w=0, h=default_cell_height_for_heading, text="PARA - B (EPS)", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=(210-primary_heading_width)/2, y=report.get_y(), w=primary_heading_width, h=default_cell_height_for_heading-0.75)

    # #Form 2 Revised
    # report.set_font('noto-sans-devanagari', size=9, style="")
    # form_2_heading_width = report.get_string_width("Form-2 (Revised)") + 6 #padding
    # report.set_xy(x=report.get_x()-(form_2_heading_width-3), y=report.get_y())
    # report.cell(w=form_2_heading_width-3, h=default_cell_height_for_heading, text=f"Form-2 (Revised)", align="L", new_x="RIGHT", new_y='TOP', border=0)
    # report.rect(x=report.get_x()-form_2_heading_width, y=report.get_y(), w=form_2_heading_width, h=default_cell_height_for_heading-0.75)
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_for_heading) #NEXT line

    #Secondary Heading
    report.set_font('noto-sans-devanagari', size=10, style="B")
    secondary_heading_width = report.get_string_width("(Para 18)") + 10 #padding
    report.cell(w=0, h=default_cell_height_for_heading, text='(Para 18)', align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=(210-secondary_heading_width)/2, y=report.get_y(), w=secondary_heading_width, h=default_cell_height_for_heading-0.75)

    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main statement
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    report.multi_cell(w=0, h=default_cell_height_smaller, text="I hereby furnish below particulars of the members of my family who would be eligible to receive Widow/Children Pension in the event of my premature death in service.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    initial_coordinates_before_table_header = {"x": report.get_x(), "y": report.get_y()}
    report.set_font('noto-sans-devanagari', size=7, style="")
    #Table Headers
    # report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['family_name_address'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['family_serial'], h=default_cell_height_smaller*2, text="Sr. No", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.multi_cell(w=width_of_columns['family_name_address'], h=default_cell_height_smaller*2, text="Name & Address of the Family Member", align="C", new_x="RIGHT", new_y='TOP', border=1)
    
    report.multi_cell(w=width_of_columns['family_age'], h=default_cell_height_smaller*2, text="Age", align="C", new_x="RIGHT", new_y='TOP', border=1)

    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['family_relation'], h=default_cell_height_smaller*2)
    report.multi_cell(w=width_of_columns['family_relation'], h=default_cell_height_smaller, text="Relationship with the member", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Table serials
    report.cell(w=width_of_columns['family_serial'], h=default_cell_height_smaller, text="(1)", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['family_name_address'], h=default_cell_height_smaller, text="(2)", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['family_age'], h=default_cell_height_smaller, text="(3)", align="C", new_x="RIGHT", new_y='TOP', border=1)
    report.cell(w=width_of_columns['family_relation'], h=default_cell_height_smaller, text="(4)", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

    #Family Table values
    family_members = employee.employee_family_nominee_detail.order_by('id')
    for index in range(6):
        member = None
        try: member = family_members[index]
        except: pass
        member_name = member.name if member != None else ''
        member_address = member.address if member != None and member.address else ''
        member_relation = member.get_relation_display() if member and  member.relation else ''
        member_age = member.calculate_age() if member and member.dob else ''
        #Serial
        report.cell(w=width_of_columns['family_serial'], h=default_cell_height_smaller*2, text=f"{index+1}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #Member Name
        report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['family_name_address'], h=default_cell_height_smaller*2)
        report.multi_cell(w=width_of_columns['family_name_address'], h=default_cell_height_smaller, text=f"{member_name}\n{member_address}", align='L', new_x="RIGHT", new_y="TOP", border=0)
        #Member Age
        report.cell(w=width_of_columns['family_age'], h=default_cell_height_smaller*2, text=f"{member_age if member_age else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #Nominee Relation
        report.cell(w=width_of_columns['family_relation'], h=default_cell_height_smaller*2, text=f"{member_relation}", align='C', new_x="LMARGIN", new_y="NEXT", border=1)
    
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    #More Content of rules
    report.multi_cell(w=0, h=default_cell_height_smaller, text="Certified that I have no family as defined in para 2 (vii) of the Employees's Family Pension Scheme 1995 and should I acquire a family hereafter I shall furnish Particulars there on in the above form.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    report.multi_cell(w=0, h=default_cell_height_smaller, text="I hereby nominate the following person for receiving the monthly widow pension (admissible under para 16 2 (a) (i) & (ii) in the event of my death without leaving any eligible family member for receiving pension.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller) #Blank Line
    
    initial_coordinates_before_table_header = {"x": report.get_x(), "y": report.get_y()}
    report.set_font('noto-sans-devanagari', size=7, style="")
    #Table Headers
    # report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['family_name_address'], h=default_cell_height_smaller*6)
    report.multi_cell(w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller*2, text="Name and Address of the nominee", align="C", new_x="RIGHT", new_y='TOP', border=1)
    
    report.multi_cell(w=width_of_columns['nominees_dob'], h=default_cell_height_smaller*2, text="Date of Birth", align="C", new_x="RIGHT", new_y='TOP', border=1)

    report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*2)
    report.multi_cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller, text="Relationship with member", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

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
        #Nominee Name and Address
        report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller*2)
        report.multi_cell(w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller, text=f"{nominee_name}\n{nominee_address}", align='L', new_x="RIGHT", new_y="TOP", border=0)
        #Nominee DOB
        report.cell(w=width_of_columns['nominees_dob'], h=default_cell_height_smaller*2, text=f"{nominee_dob if nominee_dob else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        #Nominee Relation
        report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*2, text=f"{nominee_relation}", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

    #Signature
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=210-right_margin-width_of_columns['signature'], y=report.get_y()+default_cell_height_smaller*6) #Blank Line
    report.multi_cell(w=width_of_columns['signature'], h=default_cell_height_smaller, text="Signature/or thumb impression of the subscriber", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Certificate by employer
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller*2) #Blank Line
    last_heading_width = report.get_string_width("CERTIFICATE BY EMPLOYER") + 10 #padding
    print(f'String width: {last_heading_width}')
    report.cell(w=0, h=default_cell_height_for_heading, text="CERTIFICATE BY EMPLOYER", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.rect(x=(210-last_heading_width)/2, y=report.get_y(), w=last_heading_width, h=default_cell_height_for_heading-0.75)

    #Last main body
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_smaller*3) #Blank Line
    report.multi_cell(w=0, h=default_cell_height_smaller, text="Certified that the above declaration and nomination has been signed / thumb impressed before me by Shri / Smt./ Miss _________________________________________________________________ employed in my establishment after he/she has read the entries / the entries have been read over to him/her by me and got confirmed by him/her.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller*2) #Blank Line
    #Company Address and DOJ
    address = ''
    try: address = employee.company.company_details.address
    except: pass
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=0, h=default_cell_height_for_heading, text=f"Place : {address}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_for_heading, text=f"Date :  {employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Footers
    report.set_xy(x=report.get_x(), y=297-10-default_cell_height*3)
    report.cell(w=0, h=default_cell_height, text=f"Name & address of the Factory /Establishment", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height, text=f"{employee.company.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"{address}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    report.set_xy(x=report.get_x()-width_of_columns['authorised_signature'], y=report.get_y()-default_cell_height_smaller*3) #Blank Line
    report.cell(w=None, h=default_cell_height, text=f"For ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height, text=f"{employee.company.name} ", align="L", new_x="RIGHT", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['authorised_signature'], y=report.get_y()+default_cell_height)
    report.cell(w=0, h=default_cell_height, text=f"Authorised Signature", align="L", new_x="RIGHT", new_y='TOP', border=0)

