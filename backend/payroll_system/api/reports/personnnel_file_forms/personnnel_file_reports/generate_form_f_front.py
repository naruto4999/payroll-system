import os
# from datetime import datetime, date, time
# from dateutil.relativedelta import relativedelta


def generate_form_f_front(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    default_cell_height_smaller = 4
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        "placeholder": 100,
        "signature": 60,
        #Table
        "nominees_serial": 7,
        "nominees_name_address": 130,
        "nominees_relation": 30,
        "nominees_age": 14,
        "proportion": 16
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
    report.cell(w=0, h=default_cell_height_for_heading, text="Form 'F'", align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=12, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text='Payment of Gratuity', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7, style="B")
    report.cell(w=0, h=default_cell_height, text='(See sub-rule (1) of Rule 5)', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height, text='Nomination', align="C", new_x="LMARGIN", new_y='NEXT', border=0)


    report.set_font('noto-sans-devanagari', size=9, style="")

    #Before Table
    report.cell(w=0, h=default_cell_height, text='To', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y())
    #Drawing line
    report.set_dash_pattern(dash=1, gap=1)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    #Printing Company Name and address
    report.cell(w=0, h=default_cell_height, text=f"{employee.company.name}", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    address = ''
    try: address = employee.company.company_details.address
    except: pass
    report.cell(w=0, h=default_cell_height, text=f"{address}", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"(Give here name of establishment with full address)", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #1
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='1.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"{employee.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x()+width_of_columns['serial'], y=report.get_y())
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"(Name in full here)", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.multi_cell(w=0, h=default_cell_height_smaller, text=f"Whose particulars are given in the statement below hereby nominate the person's mentioned below to receive the gratuity payable after my death as also the gratuity standing to my credit in the event of my death beofre the month has become has month's", align="J", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #2
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.cell(w=width_of_columns['serial'], h=default_cell_height_smaller, text='2.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.multi_cell(w=0, h=default_cell_height_smaller, text=f"I hereby certify the persons mentioned is/are a member's of my family within the meaning of clause that (h) if section 2 of the payment Act. 1972", align="J", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #3
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.cell(w=width_of_columns['serial'], h=default_cell_height_smaller, text='3.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"I hereby declare that I have no family within meaning of clause (h) of section (2) of paid Act.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #4
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.cell(w=width_of_columns['serial'], h=default_cell_height_smaller, text='4.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"(a) My father/mother/parents is/are not dependent on me", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"(b) My husband's father/mother/parents is/are not dependent on my husband", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #5
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.cell(w=width_of_columns['serial'], h=default_cell_height_smaller, text='5.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.multi_cell(w=0, h=default_cell_height_smaller, text=f"I have excluded from my family be a notice date ..................................... to the controlling authority in terms of the provision to clause (h) of section 2 of the paid Act.", align="J", new_x="LMARGIN", new_y='NEXT', border=0)

    #6
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.cell(w=width_of_columns['serial'], h=default_cell_height_smaller, text='6.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height_smaller, text=f"Nomination made herein invalidates my previous nomination", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Nominees Table headers
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height_smaller)
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text='Nominees', align="C", new_x="LMARGIN", new_y="NEXT", border=0)
    report.set_font('noto-sans-devanagari', size=7, style="B")
    report.set_dash_pattern(dash=0, gap=0)
    report.cell(w=width_of_columns['nominees_serial'], h=default_cell_height_smaller*3, text=f"S/N", align='C', new_x="RIGHT", new_y="TOP", border=1)
    report.multi_cell(w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller*3, text=f"Full Name with full address of nominee", align='C', new_x="RIGHT", new_y="TOP", border=1)
    report.multi_cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*3/2, text=f"Relationship with the employee", align='C', new_x="RIGHT", new_y="TOP", border=1)
    report.multi_cell(w=width_of_columns['nominees_age'], h=default_cell_height_smaller*3/2, text=f"Age of nominee", align='C', new_x="RIGHT", new_y="TOP", border=1)
    report.multi_cell(w=width_of_columns['proportion'], h=default_cell_height_smaller*3/2, text=f"Gratuity Proportion", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

    report.set_font('noto-sans-devanagari', size=7, style="")
    #Nominee Table values
    nominees = employee.employee_family_nominee_detail.filter(is_gratuity_nominee=True).order_by('id')
    for index in range(4):
        nominee = None
        try: nominee = nominees[index]
        except: pass
        report.cell(w=width_of_columns['nominees_serial'], h=default_cell_height_smaller*4, text=f"{index+1}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        nominee_name = nominee.name if nominee != None else ''
        nominee_address = nominee.address if nominee != None else ''
        nominee_relation = nominee.get_relation_display() if nominee else ''
        nominee_age = nominee.calculate_age() if nominee else ''
        nominee_proportion = nominee.gratuity_nominee_share if nominee else ''
        report.rect(x=report.get_x(), y=report.get_y(), w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller*4)
        report.multi_cell(w=width_of_columns['nominees_name_address'], h=default_cell_height_smaller, text=f"{nominee_name}\n{nominee_address}", align='L', new_x="RIGHT", new_y="TOP", border=0)
        report.cell(w=width_of_columns['nominees_relation'], h=default_cell_height_smaller*4, text=f"{nominee_relation}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        report.cell(w=width_of_columns['nominees_age'], h=default_cell_height_smaller*4, text=f"{nominee_age if nominee_age else ''}", align='C', new_x="RIGHT", new_y="TOP", border=1)
        report.cell(w=width_of_columns['proportion'], h=default_cell_height_smaller*4, text=f"{nominee_proportion if nominee_proportion else ''}{' %' if nominee_proportion else ''}", align='C', new_x="LMARGIN", new_y="NEXT", border=1)

