from fpdf import FPDF
import os
from datetime import date

#A4 size 210 x 297 mm
width_of_columns = {
        "id_card_width": 85,
        "intro_headers": 15,
        "intro_values": 70,
    }

def generate_id_card_landscape(request_data, employees):
    
    default_cell_height = 3.75
    default_cell_height_large = 4
    # default_row_number_of_cells = 1
    left_margin = 6
    top_margin = 6
    right_margin = 7
    bottom_margin = 5
    photo_border_buffer = 0.3

    # company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    id_card = FPDF(orientation="P", unit="mm", format="A4")

    #Page settings
    id_card.set_margins(left=left_margin, top=top_margin, right=right_margin)
    id_card.add_page()
    id_card.set_auto_page_break(auto=True, margin = bottom_margin)
    id_card.set_line_width(0.3)
    compnay_address = ''
    try: compnay_address = employees.first().company.company_details.address
    except: pass

    for index, employee in enumerate(employees):
        
        if index%10==0 and index!=0:
            id_card.add_page()
        initial_coordinates_for_current_id_card = {"x": id_card.get_x(), "y": id_card.get_y()}
        #Rectangle for whole id card
        id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['id_card_width'], h=default_cell_height*8+(default_cell_height_large*6))

        #Headers
        id_card.set_font("Helvetica", size=7.5, style="B")
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"IDENTITY CARD", align="C", new_x="LEFT", new_y='NEXT', border='TLR')
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"{employee.company.name}", align="C", new_x="LEFT", new_y='NEXT', border='LR')
        id_card.set_font("Helvetica", size=7.5, style="")
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"{compnay_address}", align="C", new_x="LEFT", new_y='NEXT', border='BLR')

        ##Employee Details
        id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['intro_headers'], h=default_cell_height*8)
        #Paycode
        if employee.photo != '':
            id_card.image(employee.photo, x=id_card.get_x()+width_of_columns['id_card_width']-(20+photo_border_buffer), y=id_card.get_y()+photo_border_buffer, w=20, h=21.8)
        id_card.set_font("Helvetica", size=6.5, style="")
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Paycode :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        # id_card.set_font("Helvetica", size=6, style="B")
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.paycode}", align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Name
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Name :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.name}", align="L", new_x="LEFT", new_y='NEXT', border=0)

        #DOJ
        employee_doj = ''
        try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
        except: pass
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"DOJ :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_doj}", align="L", new_x="LEFT", new_y='NEXT', border=0)
        
        #Father Husband Name
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"F/H Name :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.father_or_husband_name if employee.father_or_husband_name else ''}", align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Department
        employee_department = ''
        try: employee_department = employee.employee_professional_detail.department.name
        except: pass
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Department :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_department}", align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Designation
        employee_designation = ''
        try: employee_designation = employee.employee_professional_detail.designation.name
        except: pass
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Designation :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_designation}", align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Adress
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
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Address :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.multi_cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{text}", align="L", new_x="RIGHT", new_y='TOP', border=0)

        #Authorised Signature
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y()+default_cell_height*2)
        id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['id_card_width'], h=default_cell_height_large*3)
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y()+default_cell_height_large*2)
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"Authorised Signature", align="L", new_x="LMARGIN", new_y='NEXT', border='LR')

        if (index+1)%2!=0:
            id_card.set_xy(x=210-right_margin-width_of_columns['id_card_width'], y=initial_coordinates_for_current_id_card['y'])
        else:
            id_card.set_xy(x=id_card.get_x(), y=id_card.get_y()+default_cell_height_large)
        


    # Save the pdf with name .pdf
    buffer = bytes(id_card.output())
    yield buffer