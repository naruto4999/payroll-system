from fpdf import FPDF
import os
from datetime import date
from fpdf.enums import MethodReturnValue, XPos, YPos, Align
from ...pdf_utils.custom_fpdf import CustomFPDF

#A4 size 210 x 297 mm
width_of_columns = {
        "id_card_width": 54,
        "id_card_height": 85,
        "intro_headers": 15,
        "intro_values": 39,
    }

def generate_id_card_portrait(request_data, employees):
    
    default_cell_height = 3.75
    default_cell_height_large = 4
    # default_row_number_of_cells = 1
    left_margin = 8
    top_margin = 6
    right_margin = 8
    bottom_margin = 5
    photo_border_buffer = 0.2

    # company_details = CompanyDetails.objects.filter(company_id=request_data['company'])
    id_card = CustomFPDF(orientation="P", unit="mm", format="A4")

    #Page settings
    id_card.set_margins(left=left_margin, top=top_margin, right=right_margin)
    id_card.add_page()
    id_card.set_auto_page_break(auto=True, margin = bottom_margin)
    id_card.set_line_width(0.3)
    compnay_address = ''
    try: compnay_address = employees.first().company.company_details.address
    except: pass

    for index, employee in enumerate(employees):
        
        if index%9==0 and index!=0:
            id_card.add_page()
        initial_coordinates_for_current_id_card = {"x": id_card.get_x(), "y": id_card.get_y()}
        #Rectangle for whole id card
        id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['id_card_width'], h=width_of_columns["id_card_height"])

        
        #Headers
        id_card.set_font("Helvetica", size=7.5, style="B")
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"IDENTITY CARD", align="C", new_x="LEFT", new_y='NEXT', border='TLR')
        id_card.multi_cell_with_limit(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"{employee.company.name} A long ass compnay name to test functionality", max_lines=1, border_each_line=False, align="C", new_x="LEFT", new_y='NEXT', border='LR')
        id_card.set_font("Helvetica", size=7.5, style="")
        id_card.multi_cell_with_limit(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"{compnay_address}", min_lines=2, max_lines=2, border_each_line=False, align="C",  new_x="LEFT", new_y='NEXT', border='BLR')

        #Employee Photo
        id_card.set_line_width(0.2)
        id_card.rect(x=id_card.get_x()+((width_of_columns["id_card_width"]-(22+photo_border_buffer*2))/2), y=id_card.get_y()+((default_cell_height*7)-(23.98+photo_border_buffer*2))/2, w=22+photo_border_buffer*2, h=23.98+photo_border_buffer*2)
        if employee.photo != '':
            id_card.image(employee.photo, x=id_card.get_x()+((width_of_columns["id_card_width"]-22)/2), y=id_card.get_y()+((default_cell_height*7)-(23.98))/2, w=22, h=23.98)
        id_card.set_xy(x=id_card.get_x(), y=id_card.get_y()+(default_cell_height*7))
        id_card.set_line_width(0.3)

        #Employee Detials
        id_card.set_font("Helvetica", size=6.5, style="")
        #id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['id_card_width'], h=default_cell_height*9)
        #id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['intro_headers'], h=default_cell_height*9)

        #Paycode
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Paycode :", align="L", new_x="RIGHT", new_y='TOP', border='TLR')
        id_card.cell(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.paycode}", align="L", new_x="LEFT", new_y='NEXT', border='T')

        #Name
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Name :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.multi_cell_with_limit(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.name}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="LEFT", new_y='NEXT', border=0)

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
        id_card.multi_cell_with_limit(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee.father_or_husband_name if employee.father_or_husband_name else ''}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Department
        employee_department = ''
        try: employee_department = employee.employee_professional_detail.department.name
        except: pass
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Department :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.multi_cell_with_limit(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_department}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="LEFT", new_y='NEXT', border=0)

        #Designation
        employee_designation = ''
        try: employee_designation = employee.employee_professional_detail.designation.name
        except: pass
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.cell(w=width_of_columns['intro_headers'], h=default_cell_height, text=f"Designation :", align="L", new_x="RIGHT", new_y='TOP', border='LR')
        id_card.multi_cell_with_limit(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{employee_designation}", min_lines=1, max_lines=1, border_each_line=False, align="L", new_x="LEFT", new_y='NEXT', border=0)


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
        id_card.multi_cell_with_limit(w=width_of_columns['intro_values'], h=default_cell_height, text=f"{text}", min_lines=3, max_lines=3, border_each_line=False, align="L", new_x="LEFT", new_y='NEXT', border='L')


        #Authorised Signature
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y())
        id_card.rect(x=id_card.get_x(), y=id_card.get_y(), w=width_of_columns['id_card_width'], h=width_of_columns['id_card_height']-((default_cell_height_large*4)+(default_cell_height*16)))
        id_card.set_xy(x=initial_coordinates_for_current_id_card['x'], y=id_card.get_y()+(width_of_columns['id_card_height']-((default_cell_height_large*4)+(default_cell_height*16)))-default_cell_height)
        id_card.cell(w=width_of_columns['id_card_width'], h=default_cell_height_large, text=f"Authorised Signature", align="L", new_x="RIGHT", new_y='NEXT', border='')




         
        if (index+1)%3!=0:
            id_card.set_xy(x=id_card.get_x()+(210-left_margin-right_margin-(width_of_columns['id_card_width']*3))/2, y=initial_coordinates_for_current_id_card['y'])
        else:
            id_card.set_xy(x=left_margin, y=id_card.get_y()+default_cell_height_large)
        


    # Save the pdf with name .pdf
    buffer = bytes(id_card.output())
    yield buffer
