import os
from ....models import EmployeeFamilyNomineeDetial

def generate_biodata(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    default_cell_height = 7
    default_table_cell_height = 5
    width_of_columns = {
        "paycode": 40,
        "serial": 5,
        "biodata_headers": 70,
        "biodata_values": 210-right_margin-70-5,
        #Table 1
        "previous_experience_serial": 7,
        "previous_experience_company_name": 50,
        "previous_experience_designation": 35,
        "previous_experience_from_date": 20,
        "previous_experience_to_date": 20,
        "previous_experience_salary": 15,
        "previous_experience_reason_for_leaving": 50,
        #Table 2
        "family_details_serial": 7,
        "family_details_name": 60,
        "family_details_relation": 30,
        "family_details_age": 15,
        "family_details_address": 85,
        #Table 3
        "references_serial": 7,
        "references_name": 55,
        "references_relation": 30,
        "references_phone": 20,
        "references_address": 85,
        #Signature at the end
        'signature': 60
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
    report.cell(w=0, h=default_cell_height_for_heading, text='Biodata Form', align="C", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=0, h=default_cell_height_for_heading, text='व्यक्त्तिगत विवरण फार्म', align="C", new_x="RIGHT", new_y='TOP', border=0)

    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=report.get_x()-width_of_columns['paycode'], y=report.get_y())
    report.cell(w=width_of_columns['paycode'], h=default_cell_height_for_heading, text=f"{employee.paycode}", align="R", new_x="LMARGIN", new_y='NEXT', border=0)


    #Printing Photo if it exists
    #A4 size in millimeters: 210 x 297 mm.
    report.rect(x=210-right_margin-32, y=report.get_y(), w=32, h=35)
    if employee.photo != '':
        report.image(employee.photo, x=210-right_margin-32, y=report.get_y(), w=32, h=35)

    #Printing Designation
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='1.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f'Designation /', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'अभ्यर्थित पद:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f'{employee.employee_professional_detail.designation.name if employee.employee_professional_detail.designation != None else ""}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Department
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='2.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f'Department /', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'विभाग:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f'{employee.employee_professional_detail.department.name if employee.employee_professional_detail.department != None else ""}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Name
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='3.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f'Name /', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'नाम:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f'{employee.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing Father/Husband Name
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='4.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Father/Husband /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'पिता/पति:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f'{employee.father_or_husband_name if employee.father_or_husband_name != None else ""}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing DOB
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='5.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Date of Birth /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'जन्म तिथि:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.dob.strftime('%d-%b-%Y') if employee.dob != None else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing DOJ
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='6.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Date of Joining /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'नियुक्त्ति की तिथि:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y') if employee.employee_professional_detail.date_of_joining != None else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing PF Number
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='7.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"PF No. /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'ई.पी.एफ सं०:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    text = ''
    try: text = employee.employee_pf_esi_detail.pf_number
    except: pass
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{text or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing ESI Number
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='8.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"ESI No. /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'ई.एस.आई सं०:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    text = ''
    try: text = employee.employee_pf_esi_detail.esi_number
    except: pass
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{text or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing Nationality
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='9.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Nationality /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'राष्ट्रीयता:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.nationality}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing Religion
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='10.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Religion /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'धर्म:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.religion or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing Marital Status
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='11.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Marital Status /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'वैवाहिक स्थिति:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.get_marital_status_display() or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
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
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='12.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Local Address /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'स्थानीय पता:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
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
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='13.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Permanent Address /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'स्थाई पता:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{text}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Qualification
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='14.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Qualification /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'योग्यता:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.get_education_qualification_display() or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #Printing Technical Qualification
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='15.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Technical Qualification /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'तकनीकी योग्यता:', align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.set_xy(x=width_of_columns['serial']+width_of_columns['biodata_headers'], y=report.get_y())
    report.cell(w=width_of_columns['biodata_values'], h=default_cell_height, text=f"{employee.technical_qualification or ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Printing Previous Experience
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='16.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Previous Experience /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'पहले का अनुभव:', align="L", new_x="LMARGIN", new_y='NEXT', border=0)


    report.set_font('noto-sans-devanagari', size=7, style="")
    
    initial_coordinates_before_table_header = {"x": report.get_x(), "y": report.get_y()}
    ##Printing Previous Experince table headers
    report.cell(w=width_of_columns['previous_experience_serial'], h=default_table_cell_height, text=f"S/N", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['previous_experience_serial'], h=default_table_cell_height, text=f"क्रमांक", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_table_header['y'])

    report.cell(w=width_of_columns['previous_experience_company_name'], h=default_table_cell_height, text=f"Name of Company", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['previous_experience_company_name'], h=default_table_cell_height, text=f"संस्था का नाम", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_table_header['y'])

    report.cell(w=width_of_columns['previous_experience_designation'], h=default_table_cell_height, text=f"Designation", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['previous_experience_designation'], h=default_table_cell_height, text=f"पद", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_table_header['y'])

    report.cell(w=width_of_columns['previous_experience_from_date'], h=default_table_cell_height, text=f"From", align='C', new_x="RIGHT", new_y="TOP", border='LT')
    report.cell(w=width_of_columns['previous_experience_to_date'], h=default_table_cell_height, text=f"To", align='C', new_x="LEFT", new_y="NEXT", border='RT')
    report.set_xy(x=report.get_x()-width_of_columns['previous_experience_to_date'], y=report.get_y())
    report.cell(w=width_of_columns['previous_experience_from_date']+width_of_columns['previous_experience_to_date'], h=default_table_cell_height, text=f"अवधि", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_table_header['y'])

    report.cell(w=width_of_columns['previous_experience_salary'], h=default_table_cell_height, text=f"Salary", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['previous_experience_salary'], h=default_table_cell_height, text=f"वेतन", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_table_header['y'])

    report.cell(w=width_of_columns['previous_experience_reason_for_leaving'], h=default_table_cell_height, text=f"Reason For Leaving", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['previous_experience_reason_for_leaving'], h=default_table_cell_height, text=f"छोड़ने का कारण", align='C', new_x="RIGHT", new_y="TOP", border='BLR')

    report.set_xy(x=initial_coordinates_before_table_header['x'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    # report.rect(x=report.get_x(), y=report.get_y(), w=210-left_margin-right_margin, h=default_cell_height*3)

    ##Printing Previous Experince table values
    #Serial
    report.cell(w=width_of_columns['previous_experience_serial'], h=default_table_cell_height, text=f"1.", align='C', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_serial'], h=default_table_cell_height, text=f"2.", align='C', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_serial'], h=default_table_cell_height, text=f"3.", align='C', new_x="LEFT", new_y="NEXT", border='BLR')

    #Company Name
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_company_name'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_company_name or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_company_name'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_company_name or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_company_name'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_company_name or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')

    #Designation
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial']+width_of_columns['previous_experience_company_name'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_designation'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_designation or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_designation'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_designation or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_designation'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_designation or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')

    #From Date
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial']+width_of_columns['previous_experience_company_name']+width_of_columns['previous_experience_designation'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_from_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_from_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.first_previous_experience_from_date else ''}", align='L', new_x="LEFT", new_y="NEXT", border='L')
    report.cell(w=width_of_columns['previous_experience_from_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_from_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.second_previous_experience_from_date else ''}", align='L', new_x="LEFT", new_y="NEXT", border='L')
    report.cell(w=width_of_columns['previous_experience_from_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_from_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.third_previous_experience_from_date else ''}", align='L', new_x="LEFT", new_y="NEXT", border='LB')

    #To Date
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial']+width_of_columns['previous_experience_company_name']+width_of_columns['previous_experience_designation']+width_of_columns['previous_experience_from_date'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_to_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_to_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.first_previous_experience_to_date else ''}", align='R', new_x="LEFT", new_y="NEXT", border='R')
    report.cell(w=width_of_columns['previous_experience_to_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_to_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.second_previous_experience_to_date else ''}", align='R', new_x="LEFT", new_y="NEXT", border='R')
    report.cell(w=width_of_columns['previous_experience_to_date'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_to_date.strftime('%d-%b-%Y') if employee.employee_professional_detail.third_previous_experience_to_date else ''}", align='R', new_x="LEFT", new_y="NEXT", border='RB')

    #Salary
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial']+width_of_columns['previous_experience_company_name']+width_of_columns['previous_experience_designation']+width_of_columns['previous_experience_from_date']+width_of_columns['previous_experience_to_date'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_salary'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_salary or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_salary'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_salary or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_salary'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_salary or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')

    #Reason For Leaving
    report.set_xy(x=initial_coordinates_before_table_header['x']+width_of_columns['previous_experience_serial']+width_of_columns['previous_experience_company_name']+width_of_columns['previous_experience_designation']+width_of_columns['previous_experience_from_date']+width_of_columns['previous_experience_to_date']+width_of_columns['previous_experience_salary'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['previous_experience_reason_for_leaving'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_previous_experience_reason_for_leaving or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_reason_for_leaving'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_previous_experience_reason_for_leaving or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['previous_experience_reason_for_leaving'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.third_previous_experience_reason_for_leaving or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')

    report.set_font('noto-sans-devanagari', size=9, style="")
    #Printing Family Details
    report.set_xy(x=initial_coordinates_before_table_header['x'], y=initial_coordinates_before_table_header['y']+default_table_cell_height*5)
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='17.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=None, h=default_cell_height, text=f"Family Details /", align="L", new_x="RIGHT", new_y='TOP', border=0)
    report.cell(w=None, h=default_cell_height, text=f'पारिवारिक विवरण:', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7, style="")
    initial_coordinates_before_family_table_header = {'x': report.get_x(), 'y': report.get_y()}
    ##Printing Family Details headers
    report.cell(w=width_of_columns['family_details_serial'], h=default_table_cell_height, text=f"S/N", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_serial'], h=default_table_cell_height, text=f"क्रमांक", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])

    report.cell(w=width_of_columns['family_details_name'], h=default_table_cell_height, text=f"Name", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_name'], h=default_table_cell_height, text=f"नाम", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])
    
    report.cell(w=width_of_columns['family_details_relation'], h=default_table_cell_height, text=f"Relation", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_relation'], h=default_table_cell_height, text=f"सम्बन्ध", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])

    report.cell(w=width_of_columns['family_details_age'], h=default_table_cell_height, text=f"Age", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_age'], h=default_table_cell_height, text=f"आयु", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y'])
    
    report.cell(w=width_of_columns['family_details_address'], h=default_table_cell_height, text=f"Address", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['family_details_address'], h=default_table_cell_height, text=f"पता", align='C', new_x="LMARGIN", new_y="NEXT", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_family_table_header['y']+default_table_cell_height*2)

    ##Printing Family Details values
    family_details = EmployeeFamilyNomineeDetial.objects.filter(employee=employee)
    print(f'Family Details: {family_details}')
    for index in range(8):
        family_member = None
        try: family_member = family_details[index]
        except: pass
        border = 'LR'
        if index==7:
            border='BLR'
        report.cell(w=width_of_columns['family_details_serial'], h=default_table_cell_height, text=f"{index+1}.", align='C', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_name'], h=default_table_cell_height, text=f"{family_member.name if family_member and family_member.name else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_relation'], h=default_table_cell_height, text=f"{family_member.relation if family_member and family_member.relation else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_age'], h=default_table_cell_height, text=f"{family_member.calculate_age() if family_member and family_member.dob else ''}", align='L', new_x="RIGHT", new_y="TOP", border=border)
        report.cell(w=width_of_columns['family_details_address'], h=default_table_cell_height, text=f"{family_member.address if family_member and family_member.address else ''}", align='L', new_x="LMARGIN", new_y="NEXT", border=border)

    report.set_font('noto-sans-devanagari', size=9, style="")
    #Printing References
    report.cell(w=width_of_columns['serial'], h=default_cell_height, text='18.', align="C", new_x="RIGHT", new_y="TOP", border=0)
    report.cell(w=210-left_margin-right_margin-width_of_columns['serial'], h=default_cell_height, text=f"Give Names, Phone No. and Address of two people (excluding relatives) who know you well.", align="L", new_x="LEFT", new_y='NEXT', border=0)
    report.cell(w=210-left_margin-right_margin-width_of_columns['serial'], h=default_cell_height, text=f'दो व्यक्त्तियों के नाम, फ़ोन नंबर और पता (सगे सम्बन्धियों को छोड़कर ) जो आपको भलीभाँति जानते हों', align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    report.set_font('noto-sans-devanagari', size=7, style="")
    initial_coordinates_before_references_table_header = {'x': report.get_x(), 'y': report.get_y()}
    ##Printing References headers
    report.cell(w=width_of_columns['references_serial'], h=default_table_cell_height, text=f"S/N", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['references_serial'], h=default_table_cell_height, text=f"क्रमांक", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_references_table_header['y'])

    report.cell(w=width_of_columns['references_name'], h=default_table_cell_height, text=f"Name", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['references_name'], h=default_table_cell_height, text=f"नाम", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_references_table_header['y'])
    
    report.cell(w=width_of_columns['references_relation'], h=default_table_cell_height, text=f"Relation", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['references_relation'], h=default_table_cell_height, text=f"सम्बन्ध", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_references_table_header['y'])
    
    report.cell(w=width_of_columns['references_phone'], h=default_table_cell_height, text=f"Phone No.", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['references_phone'], h=default_table_cell_height, text=f"फ़ोन नंबर", align='C', new_x="RIGHT", new_y="TOP", border='BLR')
    report.set_xy(x=report.get_x(), y=initial_coordinates_before_references_table_header['y'])
    
    report.cell(w=width_of_columns['references_address'], h=default_table_cell_height, text=f"Address", align='C', new_x="LEFT", new_y="NEXT", border='TLR')
    report.cell(w=width_of_columns['references_address'], h=default_table_cell_height, text=f"पता", align='C', new_x="LMARGIN", new_y="NEXT", border='BLR')

    ##Printing Previous Experince table values
    #Serial
    report.cell(w=width_of_columns['references_serial'], h=default_table_cell_height, text=f"1.", align='C', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['references_serial'], h=default_table_cell_height, text=f"2.", align='C', new_x="LEFT", new_y="NEXT", border='BLR')

    #Reference Name
    report.set_xy(x=initial_coordinates_before_references_table_header['x']+width_of_columns['references_serial'], y=initial_coordinates_before_references_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['references_name'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_reference_name or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['references_name'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_reference_name or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')
    
    #Reference Relation
    report.set_xy(x=initial_coordinates_before_references_table_header['x']+width_of_columns['references_serial']+width_of_columns['references_name'], y=initial_coordinates_before_references_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['references_relation'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_reference_relation or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['references_relation'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_reference_relation or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')
    
    #Reference Phone
    report.set_xy(x=initial_coordinates_before_references_table_header['x']+width_of_columns['references_serial']+width_of_columns['references_name']+width_of_columns['references_relation'], y=initial_coordinates_before_references_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['references_phone'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_reference_phone or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['references_phone'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_reference_phone or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')
    
    #Reference Address
    report.set_xy(x=initial_coordinates_before_references_table_header['x']+width_of_columns['references_serial']+width_of_columns['references_name']+width_of_columns['references_relation']+width_of_columns['references_phone'], y=initial_coordinates_before_references_table_header['y']+default_table_cell_height*2)
    report.cell(w=width_of_columns['references_address'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.first_reference_address or ''}", align='L', new_x="LEFT", new_y="NEXT", border='LR')
    report.cell(w=width_of_columns['references_address'], h=default_table_cell_height, text=f"{employee.employee_professional_detail.second_reference_address or ''}", align='L', new_x="LEFT", new_y="NEXT", border='BLR')

    report.set_font('noto-sans-devanagari', size=9, style="")
    report.set_xy(x=210-left_margin-right_margin-width_of_columns['signature'], y=297-10-default_table_cell_height*2)
    report.cell(w=width_of_columns['signature'], h=default_table_cell_height, text=f"Signature of Applicant/Left Thumb Impression", align='C', new_x="LEFT", new_y="NEXT")
    report.cell(w=width_of_columns['signature'], h=default_table_cell_height, text=f"अभ्यार्थी के हस्ताक्षर ", new_x="LEFT", align='C', new_y="NEXT")


    # # Save the pdf with name .pdf
    # buffer = bytes(report.output())
    # yield buffer