import os
# from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


def generate_employee_orientation(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "serial": 5,
        "paraindent": 8,
        # "placeholder": 75,
        "authorized_signature": 80
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
    report.cell(w=0, h=default_cell_height_for_heading, text='Employee Orientation', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    # report.cell(w=0, h=default_cell_height_for_heading, text='आवेदन पत्र', align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"Employee Paycode: {employee.paycode}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"Employee Name: {employee.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    #Main text
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कर्मचारी जब कम्पनी में काम करने के लिए आता है तो उसे निम्न बातों का ध्यान रखना अनिवार्य है :-", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #1
    first_shift = None
    try: first_shift = employee.shifts.order_by('to_date').first()
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='1.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"के आने का समय सुबह    {first_shift.shift.beginning_time.strftime('%H:%M') if first_shift else ''}    बजे से है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #2
    lunch_beginning_time = None
    lunch_end_time = None
    try: 
        first_shift = employee.shifts.order_by('to_date').first()
        lunch_beginning_time = first_shift.shift.lunch_beginning_time
        lunch_end_time = (datetime.combine(datetime.now().date(), lunch_beginning_time) + relativedelta(minutes=first_shift.shift.lunch_duration)).time()
    except:
        pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='2.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"दोपहर के भोजन का समय    {lunch_beginning_time.strftime('%H:%M') if lunch_beginning_time else ''}    से    {lunch_end_time.strftime('%H:%M') if lunch_end_time else ''}    तक है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #3
    first_shift = None
    try: first_shift = employee.shifts.order_by('to_date').first()
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='3.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"शाम को जाने का समय    {first_shift.shift.end_time.strftime('%H:%M') if first_shift else ''}    है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #4
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='4.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"अतिरिक्त्त घंटे काम करना अनिवार्य नहीं है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #5
    employee_weekly_off = None
    try: employee_weekly_off = employee.employee_professional_detail.get_weekly_off_display()
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='5.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"साप्ताहिक छुट्टी    {employee_weekly_off if employee_weekly_off else ''}    को होगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #6
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='6.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"राष्ट्रीय और धार्मिक त्योहार की कुल 8 छुट्टी 1 जनवरी से 31 दिसंबर, जो एक कैलेंडर वर्ष में होती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #7
    limit = ''
    try: limit = employee.company.leave_grades.get(name="CL").limit
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='7.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कैलेंडर वर्ष में {limit} आकस्मिक छुट्टी ले सकते हैं |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #8
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='8.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"अर्जित छुट्टी ( वार्षिक छुट्टी ) या इसका पैसा ले सकते हैं | इसकी  गणना आपकी वर्ष भर की उपस्थिति के आधार पर होती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #9
    pf_percentage = None
    try: pf_percentage = employee.company.pf_esi_setup_details.ac_1_epf_employee_percentage
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='9.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कर्मचारी के वेतन से    {pf_percentage if pf_percentage else ''}    प्रतिशत भविष्य निधि ( पी.एफ ) के रूप में काटा जाता है | इतना ही हिस्सा कम्पनी भी आपके पी.एफ खाते में जमा करती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #10
    employee_esi_percentage = None
    esi_employer_percentage = None
    try: 
        employee_esi_percentage = employee.company.pf_esi_setup_details.esi_employee_percentage
        esi_employer_percentage = employee.company.pf_esi_setup_details.esi_employer_percentage
    except: pass
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='10.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कर्मचारी के वेतन से    {employee_esi_percentage if employee_esi_percentage else ''}    प्रतिशत ई.इस.आई के रूप में काटा जाता है |    {esi_employer_percentage if esi_employer_percentage else ''}    प्रतिशत कम्पनी अपने हिस्से से जमा करती है | जिसके बाद ई.इस.आई", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपको विभिन्न प्रकार की चिकित्सा सुविधाएं प्रदान करती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #11
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='11.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कर्मचारी लगातार 5 साल काम करने के बाद ग्रच्युटी के लिए अधिकारी हो जाता है सेवा छोड़ने के बाद 15 दिन प्रति वर्ष दर से जो 26 द्वारा वर्त्तमान मूल वेतन के", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"विभाजन के बाद देय है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #12
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='12.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रत्येक कर्मचारी को कार्मिक विभाग से नियुक्त्ति पत्र अवश्य ले |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #13
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='13.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"महिला कर्मचरियों को प्रसव अवकाश मिलेगा जो सरकारी नियमानुसार होगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #14
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='14.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"वेतन प्रत्येक माह की 1 से 7 तरीख तक मिलता है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #15
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='15.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"कमपनी प्रबंधन द्वारा प्रत्येक तीन माह में एक बार आग बुझाने का अभ्यास, स्वास्थ एवं सुरक्षा, स्वयम की रक्षा हेतु उपयोग में लाए जाने वाले उपकरणों, व रसायनिक पदार्थों", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"के बारे में प्रशिक्षण दिया जाता है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #16
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='16.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=0, h=default_cell_height, text=f"कमपनी प्रबंधन द्वारा प्रत्येक तीन माह में एक बार कामगार सीमिति, शिकायत निवारण सीमिति, महिला उत्पीड़न सीमिति का आयोजन किया जायेगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Signature and footers
    #A4: 210 x 297
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height))
    report.cell(w=None, h=footer_cell_height, text="कर्मचारी के हस्ताक्षर", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Bottom Right
    report.set_xy(x=210-width_of_columns['authorized_signature']-left_margin-right_margin, y=297-10-(footer_cell_height*3))
    report.cell(w=width_of_columns["authorized_signature"], h=footer_cell_height, text=f"For {employee.company.name}", align="R", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+footer_cell_height)
    report.cell(w=width_of_columns["authorized_signature"], h=footer_cell_height, text=f"अधिकृत हस्ताक्षरकर्ता", align="R", new_x="LEFT", new_y='NEXT', border=0)
