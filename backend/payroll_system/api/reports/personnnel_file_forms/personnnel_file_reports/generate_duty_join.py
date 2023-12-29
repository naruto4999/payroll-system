import os
# from dateutil.relativedelta import relativedelta
from ....models import EarningsHead, EmployeeSalaryEarning

def generate_duty_join(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "intro_headers": 30,
        "date": 80,
        "placeholder_small": 50,
        "placeholder_large": 140,
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
    report.cell(w=0, h=default_cell_height_for_heading, text='कार्यग्रहण सूचना', align="C", new_x="RIGHT", new_y='TOP', border=0)

    #Top paycode
    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*2) #blank line
    #Salutattions and Date
    employee_doj = ''
    try: 
        employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=0, h=default_cell_height, text=f"सेवा में", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=210-right_margin-width_of_columns['date'], y=report.get_y())
    report.cell(w=0, h=default_cell_height, text=f"दिनांक: {employee_doj}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"प्रबंधक महोदय", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height, text=f"{employee.company.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    compnay_address = ''
    try: compnay_address = employee.company.company_details.address
    except: pass
    report.cell(w=0, h=default_cell_height, text=f"{compnay_address if compnay_address else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y()) #blank line

    #Main Body
    report.cell(w=None, h=default_cell_height, text=f"आपके द्वारा दिए गए नियुक्त्ति पत्र दिनांक ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_small'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_small'], h=default_cell_height, text=f"{employee_doj}", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f" के अनुसार मैं आज दिनांक ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_small'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_small'], h=default_cell_height, text=f"{employee_doj}", align="C", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=None, h=default_cell_height, text=f"से ड्यूटी पर रिपोर्ट करता / करती  हूँ , जिसके अनिवार्य विवरण इस प्रकार है |", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height) #blank line
    ##Employee intro
    #Employee Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=f"{employee.name}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Employee Father / Husband Name
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पिता / पति का नाम :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=f"{employee.father_or_husband_name or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Designation
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"पद :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=f"{employee_designation or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Salary
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"वेतन प्रतिमाह :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=f"{total_earnings_rate or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Local Address
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"स्थानीय पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=text, align="L", new_x="LMARGIN", new_y='NEXT', border=0)
  
    #Printing Permanent Address
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
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"स्थाई पता :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=text, align="L", new_x="LMARGIN", new_y='NEXT', border=0)
  
    #DOJ
    report.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"कार्यग्रहण करने की तिथि :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.line(x1=report.get_x(), y1=report.get_y()+default_cell_height, x2=report.get_x()+width_of_columns['placeholder_large'], y2=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['placeholder_large'], h=default_cell_height, text=f"{employee_doj or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    #Signature and footers
    #A4: 210 x 297
    report.set_xy(x=report.get_x(), y=297-10-(footer_cell_height))
    report.cell(w=None, h=footer_cell_height, text="कर्मचारी के हस्ताक्षर", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Bottom Right
    report.set_xy(x=210-width_of_columns['authorized_signature']-left_margin-right_margin, y=297-10-(footer_cell_height*3))
    report.cell(w=width_of_columns["authorized_signature"], h=footer_cell_height, text=f"For {employee.company.name}", align="R", new_x="LEFT", new_y='NEXT', border=0)
    report.set_xy(x=report.get_x(), y=report.get_y()+footer_cell_height)
    report.cell(w=width_of_columns["authorized_signature"], h=footer_cell_height, text=f"अधिकृत हस्ताक्षरकर्ता", align="R", new_x="LEFT", new_y='NEXT', border=0)
