import os
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


def generate_form_no_16(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "paraindent": 10,
        # "placeholder": 75,
        "signature": 60
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
    report.cell(w=0, h=default_cell_height_for_heading, text='Form No. 16', align="C", new_x="RIGHT", new_y='TOP', border=0)
    
    #Printing Paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=11, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text='[Rule 107 (2) of U.P Factories Act, 1948]', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="")

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #blank line
    #Main Body
    report.cell(w=0, h=default_cell_height, text='I hereby declare that in the event of death before resuming work the balance of my pay due for the period of leave with wages', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text='not availed of shall be paid to:', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #blank line
    report.cell(w=0, h=default_cell_height, text='Shri/Smt/Km    _________________________________________________________________________________________________', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text='who is my         _________________________________________________________________________________________________', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*5) #blank line
    report.set_xy(x=210-right_margin-width_of_columns['signature'], y=report.get_y())
    report.cell(w=width_of_columns['signature'], h=default_cell_height, text='Signature of Employee', align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=width_of_columns['signature'], h=default_cell_height, text=f"({employee.name})", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*5) #blank line
    report.cell(w=0, h=default_cell_height, text='Witness: ', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text='1.          _________________________________________________________________________________________________  Name', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text='2.          __________________________________________________________________________________________________  Date', align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*2) #blank line

    #Local Address
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height, text='Local Address:', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
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
        text += employee.get_local_state_or_union_territory_display()
    if employee.local_pincode:
        if len(text) !=0:
            text += ', '
        text += employee.local_pincode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=text, align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #blank line
    #Permanent Address
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.cell(w=0, h=default_cell_height, text='Permanent Address:', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
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
        text += employee.get_permanent_state_or_union_territory_display()
    if employee.permanent_pincode:
        if len(text) !=0:
            text += ', '
        text += employee.permanent_pincode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=text, align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Signature
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height))
    report.cell(w=0, h=default_cell_height, text="Employer's Stamp and Signature", align="L", new_x="LMARGIN", new_y='NEXT', border=0)