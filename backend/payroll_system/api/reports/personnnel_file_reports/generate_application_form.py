import os

def generate_application_form(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "placeholder": 75,
        "signature": 80
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
    report.cell(w=0, h=default_cell_height_for_heading, text='Application Form', align="C", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_for_heading, text='आवेदन पत्र', align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)


    #Printing Photo if it exists
    #A4 size in millimeters: 210 x 297 mm.
    report.rect(x=210-right_margin-32, y=report.get_y(), w=32, h=35)
    if employee.photo != '':
        report.image(employee.photo, x=210-right_margin-32, y=report.get_y(), w=32, h=35)

    #Salutation and address
    report.multi_cell(w=0, h=default_cell_height, text=f"दिनांक:\nसेवा में,", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y())

    #Address
    for i in range(3):
        report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height*(i+1)), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height*(i+1)))
    address = ''
    try: address = employee.company.company_details.address
    except: pass
    report.multi_cell(w=0, h=default_cell_height, text=f"The Manager,\n{employee.company.name},\n{address}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Subject
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.cell(w=None, h=default_cell_height, text=f"विषय: ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    #Drawing line
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    
    designation = ''
    try: designation = employee.employee_professional_detail.designation.name
    except: pass
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{designation}", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f"हेतु आवेदन पत्र", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.cell(w=0, h=default_cell_height, text=f"महोदय,", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main Body
    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y())
    report.cell(w=None, h=default_cell_height, text='मुझे पता चला है कि आपकी कम्पनी में ', align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Drawing line and putting the designation
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{designation}", align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.cell(w=None, h=default_cell_height, text='की जगह खाली है | मुझे ', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Drawing line and putting the designation
    report.line(x1=report.get_x(), y1=report.get_y()+(default_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(default_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=default_cell_height, text=f"{designation}", align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.cell(w=None, h=default_cell_height, text='का काम करने का अच्छा अनुभव है | यदि आप मुझे एक बार सेवा का अवसर प्रदान करें तो मै अपना काम', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=None, h=default_cell_height, text='बड़ी मेहनत और ईमानदारी से करूँगा / करुँगी तथा किसी भी अवैध कार्य, राजनितिक या असामाजिक गतिविधियों में भाग नहीं लूंगा / लुंगी |', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # coordinates_after_main_body = {"x": report.get_x(), "y": report.get_y()}
    #Signature and footers
    #A4: 210 x 297
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height*2))
    report.cell(w=None, h=footer_cell_height, text='स्थान: ', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(footer_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(footer_cell_height))
    report.cell(w=width_of_columns['placeholder'], h=footer_cell_height, text='', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=None, h=footer_cell_height, text='दिनांक: ', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+(footer_cell_height), x2=report.get_x()+width_of_columns['placeholder'], y2=report.get_y()+(footer_cell_height))

    #Bottom Right
    report.set_xy(x=210-width_of_columns['signature'], y=297-10-(footer_cell_height*2))
    report.cell(w=None, h=footer_cell_height, text='(हस्ताक्षर)', align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=None, h=footer_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    # report.write(h=default_cell_height, text='का काम करने का अच्छा अनुभव है | यदि आप मुझे एक बार सेवा का अवसर प्रदान करें तो मै अपना काम बड़ी मेहनत और ईमानदारी से करूँगा / करुँगी तथा किसी भी अवैध कार्य, राजनितिक या असामाजिक गतिविधियों में भाग नहीं लूंगा / लुंगी | ', wrapmode= "WORD")