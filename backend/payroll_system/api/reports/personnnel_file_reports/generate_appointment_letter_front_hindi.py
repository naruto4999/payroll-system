import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time
from ...models import EmployeeSalaryEarning, EarningsHead

def generate_appointment_letter_front_hindi(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
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
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{employee.company.name}", align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Top paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Company Name and address
    company_address = ''
    try: company_address = employee.company.company_details.address
    except: pass
    report.set_font('noto-sans-devanagari', size=10, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"{company_address}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Heading
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_for_heading, text=f"नियुक्त्ति पत्र", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main Line
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.write(h=default_cell_height, text=f"आपको नौकरी के लिए आवेदन पत्र और साक्षात्कार (इंटरव्यू ) के संदर्भ में आपकी    ")
    report.set_font('noto-sans-devanagari', size=9, style="B")
    report.write(h=default_cell_height, text=f"{employee_designation}")
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.cell(w=0, h=default_cell_height, text=f"  पद के लिए नियुक्त्ति करते हुए हमें हर्ष होता है | ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    ##Employee Details
    #Name
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #Blank Line
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Father/Husband Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"पिता / पति का नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee.father_or_husband_name if employee.father_or_husband_name != None else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"अस्थायी पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"स्थायी पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #DOB
    employee_dob = ''
    try: employee_dob = employee.dob.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"जन्म तिथि :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_dob}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #DOJ
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"काम शुरू करने की तारीख :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Designation and Department
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"पद :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_designation}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"विभाग :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{employee_department}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"श्रेणी :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"(अकुशल, अर्द्धकुशल, कुशल, अतिकुशल)", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Salary Wage
    total_earnings_rate = None
    try:
        total_earnings_rate = 0
        earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee).order_by('from_date', 'earnings_head__id')
        for head in earnings_heads:
            salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head).order_by('from_date')
            if salary_for_particular_earning_head.exists():
                total_earnings_rate += salary_for_particular_earning_head.first().value
    except: 
        pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height_large, text=f"वेतन :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['intro_values'], h=default_cell_height_large, text=f"{total_earnings_rate if total_earnings_rate else ''} /-    प्रति माह / रोज़ाना / पीस रेट के आधार पर", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # #Main Body
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=14, style="B")
    report.cell(w=0, h=default_cell_height_large, text=f"नियुक्त्ति की शर्तें", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=9, style="")

    #1.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"1.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आप 6 महीने तक अस्थाई / प्रोबेशन पर नियुक्त्त रहेंगे | ज़रुरत पड़ने पर यह अवधि 6 महीने के लिए दोबारा बढ़ाई जा सकती है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #2.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"2.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अस्थाई / प्रोबेशन कार्यालय या बढाई गयी अस्थाई / प्रोबेशन कार्यालय, के दौरान आपको यह अधिकार होगा कि आप बिना किसी सूचना (नोटिस) दिए नौकरी छोड़ सकते हैं |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"इस अस्थाई / प्रोबेशन के दौरान कम्पनी को भी अधिकार होगा कि वह आपको बिना किसी सूचना (नोटिस) के नौकरी छोड़ने के लिए कह सकती है |", align="L", new_x="LEFT", new_y='NEXT', border=0)

    #3.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"3.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"किसी एक दिन 8 घंटा कार्य करने के उपरांत और किसी एक हफ्ते में 48 घंटे कार्य करने के बाद आप ओवर टाइम (OT) वेतन के हकदार हैं | फैक्ट्री एक्ट 1948 (धारा 59)", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"के तहत ओवर (OT) हमेशा आपकी स्वीकृति से होगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #4.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"4.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"काम की ज़रुरत के अनुसार कम्पनी आपका तबादला (ट्रांसफर) कम्पनी के किसी दूसरे विभाग या भारत में कम्पनी की किसी अन्य फैक्ट्री में कर सकता है | अगर आपका", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"तबादला एक से दूसरे राज्य में किया जाता है तो आपकी यात्रा का खर्चा कम्पनी के द्वारा दिया जाएगा |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    
    #5.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"5.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपकी आयु 58 वर्ष की होने पर आपको कम्पनी द्वारा रिटायर कर दिया जाएगा | कम्पनी द्वारा आपके उम्र के सबूत के तौर पर केवल स्कूल प्रमाणपत्र या आपके जन्म का", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रमाणपत्र ही माने जाएंगे | जन्म प्रमाणपत्र एक बार दिए जाने के बाद बदला नहीं जा सकता |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    
    #6.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"6.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अस्थाई / प्रोबेशन कार्यकाल ख़त्म होने के बाद आपकी नियुक्त्ति पक्की की जाएगी, कम्पनी द्वारा इस संदर्भ में आपको पत्र दिया जाएगा |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.cell(w=0, h=default_cell_height, text=f"(क) अगर आप मासिक वेतन पर कार्यरत है : पक्की नियुक्त्ति होने के बाद, अगर आप अपनी नौकरी छोड़ना चाहते हैं तो आपको कम्पनी को एक महीने का नोटिस देना पड़ेगा", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"और नोटिस पीरियड / समय के दौरान आपको कार्य करना पड़ेगा या फिर आपकी सालाना छुट्टी बकाया है तो आप उसकी एडजस्टमेंट करा सकते हैं | अगर आप कम्पनी के", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"पक्के कर्मचारी हैं और कम्पनी आपकी सेवाएं बर्खास्त करते है तो वह आपको एक महीने का नोटिस या फिर नोटिस ना देने के स्थान पर एक महीने का वेतन देगी |", align="L", new_x="LEFT", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height)
    report.cell(w=0, h=default_cell_height, text=f"(ख) अगर आप मासिक वेतन पर कार्यरत नहीं हैं : पक्की नियुक्त्ति होने के बाद, अगर आप अपनी नौकरी छोड़ना चाहते हैं तो आपको कम्पनी को दो हफ्तों का नोटिस देना", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"पड़ेगा या फिर अगर सालाना छुट्टी बकाया है तो आप उसकी एडजस्टमेंट करा सकते हैं | अगर आप पक्के कर्मचारी हैं और कम्पनी आपकी सेवाएं बर्खास्त करती है तो वह", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"आपको दो हफ्ते का नोटिस या नोटिस देने के स्थान पर दो साप्ताह का वेतन प्रदान करेगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    #7.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"7.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"बुरे व्यहवार की शिकायत मिलने पर आपको नौकरी से निलंबित (सस्पेंड) किया जा सकता है, जब तक कि जाँच (इन्क्वॉयरी) पूरी नहीं होगी | आपको सस्पेंशन के दौरान 50%", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"वेतन मिलेगा | यदि आपका बुरा व्यहवार साबित नहीं होता है तो कम्पनी आपको निलंबित समय का पूरा वेतन देगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #8.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"8.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"जब तक आप इस कम्पनी में काम करते हैं, आपको बिना कम्पनी की आज्ञा लिए दूसरी किसी कम्पनी में काम करने की अनुमति नहीं है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #9.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"9.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"भारतीय श्रम कानून के नियम अनुसार जैसे ही आप इस कम्पनी में 240 दिन काम कर लेते हैं तो आपको एक दिन की छुट्टी हर 20 कार्य दिनों के बाद वेतन सहित लेने का", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अधिकार होगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #10.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"10.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"वर्ष में 7 दिन का आकस्मिक अवकाश (CL) का अधिकार होगा पूरे वेतन के साथ |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #11.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"11.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"वर्ष में ESIC के नियमानुसार बीमारी के अवकाश का अधिकार होगा |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #12.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"12.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"यदि आपका मेडिकल इंश्योरेंस नहीं है और यदि आपने कम से कम 80 दिन कम्पनी में कार्य किया है तो गर्भावस्था के समय आपका पूरे वेतन के साथ बिना काम किये 26", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"हफ्ते की गर्भावस्था छुट्टियाँ मिलेंगी |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #13.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"13.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=0, h=default_cell_height, text=f"नियमानुसार आपको और आपके परिवार को मेडिकल इंश्योरेंस (ESI) की सुविधा दी जाएगी | जिसके लिए आपके कुल वेतन का 0.75 प्रतिशत हर महीने काट लिया जाएगा", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"और आपके योगदान के रूप में आपको ESI का कार्ड दिया जाएगा | इस कार्ड से आपको बीमार पड़ने पर छुट्टियों का पैसा मिलेगा और गर्भावस्था के दौरान भी पैसा मिलेगा |", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"अस्थाई या स्थाई रूप से अपंग होने पर भी पैसा मिलेगा | इसके अतिरिक्त्त उन सब चीज़ों का पैसा मिलेगा जो कि एम्प्लॉयीज़ स्टेट इंश्योरेंस एक्ट में दिए गए हैं |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    # #2.
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    # report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"2.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    # report.cell(w=0, h=default_cell_height, text=f"", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Page
    report.set_xy(x=210-width_of_columns['signature']-right_margin, y=297-8-default_cell_height)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"Page 1 of 2", align="R", new_x="RIGHT", new_y='TOP', border=0)
