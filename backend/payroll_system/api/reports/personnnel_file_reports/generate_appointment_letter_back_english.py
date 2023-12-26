import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time
from ...models import EmployeeSalaryEarning, EarningsHead

def generate_appointment_letter_back_english(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 4
    default_cell_height_large = 6
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
        "page": 20,
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
    report.set_font('noto-sans-devanagari', size=8, style="")

    #15.
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"15.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You are not permitted to take any leave that has not been sanctioned by the management or its authorized personnel under any circumstances. The approval or denial of your leave application will depend on the exigencies of company work.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #16.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"16.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You are responsible for the safekeeping and returning in good condition of all company property, including equipment, instruments, books, uniforms, etc., that may be in your personal custody, care, or charge. We reserve the right to deduct the monetary value of any such items from your dues or take appropriate action if you fail to account for this property to our satisfaction.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #17.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"17.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"In the event of continuous illness lasting six months or more, your service may be liable for termination without any further notice or relief thereof.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #18.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"18.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"In the event of your absence from duty for five or more continuous days, or being on leave with or without pay without proper authorization, it will be presumed that you have left the service of the Company without notice. In such an event, you will lose your job/service entitlement, and your accounts will be settled immediately.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #19.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"19.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"If there's a change in your residential address or any other personal particulars, you must promptly inform the management. Any communication sent to the address last provided by you will be considered as served to you. It is your responsibility to notify the management in writing about any changes in your current address or contact telephone number.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #20.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"20.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"You are expected to treat all information received or knowledge gained during your employment with the establishment as confidential. You must not disclose such information, whether directly or indirectly, during your tenure or after leaving the organization, to anyone in any manner. Any violation of this confidentiality may result in necessary legal action taken by the management.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21.
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"21.", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.multi_cell(w=0, h=default_cell_height, text=f"Terminations of Services", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21(a).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"a) Despite the clauses outlined in the letter of appointment, if you are a confirmed employee, the management reserves the right and discretion to terminate your services without providing any reason, following a notice period of one month or payment of one month's salary in lieu thereof. Correspondingly, you may resign from the service by giving one month's notice or by payment of one month's salary in lieu thereof.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21(b).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"b) Should you be found guilty of dishonesty, disobedience, disorderly behavior, indiscipline, absence from duty without permission, or any other conduct deemed detrimental to our interests, or if you violate one or more terms and conditions outlined in this letter, your services may be terminated without notice.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    #21(c).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"c) For all matters, including those not specifically mentioned or covered by this letter, you will be governed by the rules and regulations of the company.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    #21(d).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"d) The management's decision on all unresolved matters related to employment/service will be final and binding.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21(e).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"e) The management reserves the right to alter, change, modify, or repeal any terms and conditions of the appointment without providing notice or prior information.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21(f).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"f) Upon termination or leaving your employment with the establishment, you will need to undergo clearance from different departments before the full and final settlement of your account is completed.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #21(g).
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    report.multi_cell(w=0, h=default_cell_height, text=f"g) If the company terminates employment during the probation period, it will provide a 15-day notice. Similarly, if an employee wishes to leave the job, they also need to provide a 15-day notice to the company. After the confirmation period, the notice period for both the employee and the company changes to 30 days.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    #end
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.multi_cell(w=0, h=default_cell_height, text=f"As a token of your acceptance and confirmation of the terms and conditions of this appointment, please sign the duplicate copy of this letter and return it to us at your earliest convenience.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
   
    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    report.write(h=default_cell_height, text=f"We look forward to a long and rewarding association. We welcome you to the family of ")
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.write(h=default_cell_height, text=f"{employee.company.name}")

    report.set_xy(x=left_margin, y=report.get_y()+default_cell_height*2)
    report.set_font('noto-sans-devanagari', size=8, style="")
    report.cell(w=0, h=default_cell_height, text=f"I accept the employment on the aforementioned terms and conditions without any reservations.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Signature
    report.set_xy(x=report.get_x(), y=297-10-(default_cell_height_large*5))
    report.set_font('noto-sans-devanagari', size=8, style="B")
    report.cell(w=0, h=default_cell_height_large, text=f"(Signature of Candidate)", align="L", new_x="RIGHT", new_y='TOP', border=0)

    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=0, h=default_cell_height_large, text=f"For {employee.company.name}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    report.cell(w=0, h=default_cell_height_large, text=f"{employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=report.get_x()-width_of_columns['signature'], y=report.get_y())
    report.cell(w=0, h=default_cell_height_large, text=f"Authorized Signature", align="R", new_x="LMARGIN", new_y='NEXT', border=0)

    employee_doj = ''
    try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
    except: pass
    address = ''
    try: address = employee.company.company_details.address
    except: pass
    report.cell(w=0, h=default_cell_height_large, text=f"Date : {employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_large, text=f"Place : {address}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_large, text=f"Contact No.", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Page
    report.set_xy(x=210-width_of_columns['signature']-right_margin, y=297-8-default_cell_height)
    report.set_font('noto-sans-devanagari', size=7, style="")
    report.cell(w=0, h=default_cell_height, text=f"Page 2 of 2", align="R", new_x="RIGHT", new_y='TOP', border=0)


    # report.multi_cell(w=0, h=default_cell_height, text=f"We look forward to a long and rewarding association. We welcome you to the family of", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    # #21(b).
    # report.set_xy(x=left_margin, y=report.get_y()+default_cell_height)
    # report.cell(w=width_of_columns['serial'], h=default_cell_height, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=0)
    # report.multi_cell(w=0, h=default_cell_height, text=f"", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
