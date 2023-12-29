import os
# from dateutil.relativedelta import relativedelta

def generate_appointment_letter_back_hindi(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
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
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    
    # Specify the relative path to the font file
    noto_sans_dev_regular = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Regular.ttf')
    noto_sans_dev_bold = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Bold.ttf')

    #Adding Hindi Font
    report.add_font("noto-sans-devanagari",fname=noto_sans_dev_regular)
    report.add_font("noto-sans-devanagari", fname=noto_sans_dev_bold, style="B")
    report.set_text_shaping(True)
    report.add_page()
    report.set_font('noto-sans-devanagari', size=9, style="")

    #Main Body
    #14.
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"14.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपको नियमानुसार प्रोविडेंट फंड (PF) की सुविधा भी मिलेगी जिसके लिए आपके वेतन के मूल (BASIC) व महंगाई भत्ते (DA) का 12 प्रतिशत काट लिया जाएगा |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपके (PF) खाते में हर महीने जमा किया जाएगा | कम्पनी भी अपनी तरफ से 12 प्रतिशत, उतना ही पैसा आपके खाते में जमा कराएगी | ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #15.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"15.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"यदि आप कम्पनी में 30 दिन से ज़्यादा काम कर चुके हैं तो साल में कुल वेतन का कम से कम 8.33% या अधिक से अधिक 20% बोनस दिया जाएगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #16.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"16.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"यदि आपने कम्पनी में बिना नौकरी छोड़े लगातार 5 साल तक काम किया है तो कम्पनी आपको नौकरी छोड़ने पर ग्रेचुएटी की सुविधा देगी जो की ग्रेचुएटी पेमेंट एक्ट के तहत", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"होगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #17.
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"17.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"यदि आपको ऊपर दी गयीं शर्ते मंज़ूर हैं तो आप इस नियुक्त्ति पत्र पर स्वीकृत के लिए अपने हस्ताक्षर करें और दिनांक {employee_doj} से काम पर आएं |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Signature
    report.set_xy(x=report.get_x(), y=297-10-(default_cell_height_large*6))
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.cell(w=0, h=default_cell_height_large, text=f"मैंने ऊपर लिखी सभी शर्ते पढ़ और समझ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_large, text=f"ली हैं मैं उन्हें स्वीकार करता/करती हूँ |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height_large*2)
    report.cell(w=0, h=default_cell_height_large, text=f"हस्ताक्षर कर्मचारी", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Authorized Signature
    report.cell(w=0, h=default_cell_height_large, text=f"हस्ताक्षर प्रबंधक (स्टाम्प)", align="R", new_x="RIGHT", new_y='NEXT', border=0)

    #Page
    report.set_xy(x=210-width_of_columns['signature']-right_margin, y=297-8-default_cell_height)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"Page 2 of 2", align="R", new_x="RIGHT", new_y='TOP', border=0)
