import os
# from dateutil.relativedelta import relativedelta
# from datetime import datetime, date, time
from ....models import EmployeeSalaryEarning, EarningsHead

def generate_appointment_letter_front_english(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 4
    default_cell_height_large = 7
    footer_cell_height = 12

    width_of_columns = {
        "paycode": 40,
        "paraindent": 8,
        "serial": 5,
        "intro_headers": 25,
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
    report.set_font('noto-sans-devanagari', size=8, style="")

    # #Top paycode
    # report.set_font('noto-sans-devanagari', size=8, style="")
    # report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    # report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Salutations
    report.set_xy(x=report.get_x(), y=report.get_y()+default_cell_height*4) #Blank Line for letter head
    report.cell(w=0, h=default_cell_height, text=f"To", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=None, h=default_cell_height, text=f"Mr./Mrs. ", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.cell(w=0, h=default_cell_height, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=8, style="")

    #Dated
    report.set_xy(x=report.get_x()-width_of_columns['date'], y=report.get_y())
    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    report.cell(w=0, h=default_cell_height, text=f"Dated: {employee_doj}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    #Employee Local Address
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
    report.multi_cell(w=width_of_columns['employee_address'], h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Subject
    report.set_font('noto-sans-devanagari', size=11, style="B")
    report.cell(w=0, h=default_cell_height_large, text=f"Subject : Letter For Appointment", align="C", new_x="LMARGIN", new_y='NEXT', border=0)

    #Main Body
    employee_designation = ''
    try: employee_designation = employee.employee_professional_detail.designation.name
    except: pass
    employee_department = ''
    try: employee_department = employee.employee_professional_detail.department.name
    except: pass
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.set_xy(x=report.get_x()+width_of_columns['paraindent'], y=report.get_y())
    report.write(h=default_cell_height, text=f"With reference to your application dated {employee_doj} for the post of ")
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.write(h=default_cell_height, text=f"{employee_designation}")
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.write(h=default_cell_height, text=f" for ")
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.write(h=default_cell_height, text=f"{employee_department} ")
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.write(h=default_cell_height, text=f"department and interview with undersigned on dated: {employee_doj}. Management is pleased to appoint you on trail basis for the above mentioned post in our organization on the following terms & conditions if acceptable to you.")
    # report.cell(w=None, h=default_cell_height, text=f"With reference to your application dated {employee_doj} for the post of", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #1.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"1.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You are being appointed based on the information provided in your application, which constitutes a part of your contract. In the event of any omissions, exaggerations, concealment, or misrepresentations in the application, your service may be terminated without any reference to you. In such a case, you shall have no claims against the management of any kind whatsoever. The management reserves the right to file a criminal complaint against you for the concealment of facts.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #2.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"2.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"The aforementioned post offered to you is to be filled on a probationary basis for a period of six months following a one-month trial period from your date of joining (i.e., {employee_doj}). The management reserves the right to either extend your probation for another six months or confirm your service as a permanent employee after the completion of your seven months of satisfactory service, by providing written confirmation.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #3.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"3.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will not have any lien on the post to which you are being appointed, nor will you have any claim to be appointed against a permanent or regular vacancy that occurs at any time for any other post.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #4.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"4.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"We are in a business where designs, customer information, and input from customers are of a confidential nature. Additionally, all developments and productions are time-bound. If your conduct and work are deemed unsatisfactory, your service may be terminated before the mentioned period without the need for assigning a reason. In the event of termination, you shall receive only your earned wages, and you shall not have any claim against us, except for the earned wages.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #5.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"5.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"Your Probationary appointment shall be valid from your date of joining.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #6.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"6.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You shall be monthly-rated employee and shall be paid :-", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    total_earnings_rate = 0
    earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
    employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee).order_by('from_date', 'earnings_head__id')
    report.set_font('noto-sans-devanagari', size=8, style="B")
    for head in earnings_heads:
        salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head).order_by('from_date')
        if salary_for_particular_earning_head.exists():
            current_head_value = salary_for_particular_earning_head.first().value
            total_earnings_rate += current_head_value
            report.set_xy(x=(210-left_margin-right_margin-width_of_columns['salary_headers']-width_of_columns['salary_values'])/2+left_margin, y=report.get_y())
            report.cell(w=width_of_columns['salary_headers'], h=default_cell_height, text=f"{head.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
            report.cell(w=width_of_columns['salary_values'], h=default_cell_height, text=f"{current_head_value}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_xy(x=(210-left_margin-right_margin-width_of_columns['salary_headers']-width_of_columns['salary_values'])/2+left_margin, y=report.get_y())
    report.line(x1=report.get_x(), y1=report.get_y(), x2=report.get_x()+width_of_columns['salary_headers']+width_of_columns['salary_values'], y2=report.get_y())
    report.cell(w=width_of_columns['salary_headers'], h=default_cell_height, text=f"Total", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=width_of_columns['salary_values'], h=default_cell_height, text=f"{total_earnings_rate}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.set_xy(x=left_margin+width_of_columns['serial'], y=report.get_y())
    report.multi_cell(w=0, h=default_cell_height, text=f"You will be eligible for other benefits as per the Company’s Rules & Regulations decided by the company.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #7.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"7.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will be expected to serve the company anywhere in India. You will be liable to be transferred to any department, office, or industrial establishment forming a part of our organization, whether existing currently or established/acquired at a future date. You will be required to abide by the working hours of the respective department, office, or industrial establishment without receiving any extra remuneration.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #8.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"8.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"Your appointment and/or confirmation shall be subject to your being declared physically fit. If deemed necessary, you may be required to undergo periodic medical examinations.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #9.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"9.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will work under the supervision of officers designated by the Company from time to time. You shall diligently and faithfully carry out instructions given to you by your superiors in connection with the assigned work.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #10.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"10.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"The company will expect you to work with high standards, initiative, efficiency, and economy, considering the business and financial interests of the company.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #11.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"11.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will be expected to dedicate your full time and attention to the company's business. During your employment term, you are prohibited from engaging in business with any other person, firm, or company.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #12.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"12.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will be governed by our staff rules and regulations that are applicable. You are prohibited from disclosing, by any means including verbally or otherwise, any particulars or details regarding the company's business or that of its buyers/clients. This includes but is not limited to samples, designs, marketing information, technical, administrative, and organizational matters related to the company and its buyers/clients that you might be privy to due to your employment. Violation of these terms will be considered misconduct and may result in liability for damages, claims, and termination of your job.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #13.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"13.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You will initially undergo a one-month trial followed by a probationary period of six months. Your status will continue until specifically advised in writing of your confirmation. During the trial/probation period, either party can terminate your employment without notice. After confirmation, termination of your employment will require one month's notice or one month's salary in lieu thereof, from either side.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #14.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"14.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"The company's retirement age is fifty-eight. Any extension beyond the age of fifty-eight is at the sole discretion of management.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Page
    report.set_xy(x=210-width_of_columns['signature']-right_margin, y=297-8-default_cell_height)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"Page 1 of 2", align="R", new_x="RIGHT", new_y='TOP', border=0)


    # #12.
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    # report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"12.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    # report.multi_cell(w=0, h=default_cell_height, text=f"", align="L", new_x="LMARGIN", new_y='NEXT', border=0)