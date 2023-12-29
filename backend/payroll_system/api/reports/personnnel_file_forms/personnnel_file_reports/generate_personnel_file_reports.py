from fpdf import FPDF
import os
# from ....models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount
from datetime import date
from .generate_biodata import generate_biodata
from .generate_application_form import generate_application_form
from .generate_employee_orientation import generate_employee_orientation
from .generate_employee_personal_details import generate_employee_personal_details
from .generate_form_no_16 import generate_form_no_16
from .generate_form_f_front import generate_form_f_front
from .generate_form_f_back import generate_form_f_back
from .generate_confirmation_letter import generate_confirmation_letter
from .generate_esi_form_1 import generate_esi_form_1
from .generate_duty_join import generate_duty_join
from .generate_pf_form_2_front import generate_pf_form_2_front
from .generate_pf_form_2_back import generate_pf_form_2_back
from .generate_probation import generate_probation
from .generate_form_11 import generate_form_11
from .generate_appointment_letter_front_english import generate_appointment_letter_front_english
from .generate_appointment_letter_back_english import generate_appointment_letter_back_english
from .generate_appointment_letter_front_hindi import generate_appointment_letter_front_hindi
from .generate_appointment_letter_back_hindi import generate_appointment_letter_back_hindi


def generate_personnel_file_reports(request_data, employees):
    default_cell_height = 5
    default_cell_height_for_heading = 8
    left_margin = 6
    right_margin = 7
    bottom_margin = 8
    personnel_file_reports = FPDF(orientation="P", unit="mm", format="A4")

    #Page settings
    personnel_file_reports.set_margins(left=left_margin, top=6, right=right_margin)
    personnel_file_reports.set_auto_page_break(auto=True, margin = bottom_margin)
    # initial_coordinates_after_header = {"x": personnel_file_reports.get_x(), "y": personnel_file_reports.get_y()}
    # personnel_file_reports.cell(w=0, h=default_cell_height, text='YOOOO', align="C", new_x="RIGHT", new_y='TOP', border=1)
    for employee in employees:
        if 'biodata' in request_data['filters']['personnel_file_reports_selected']:
            generate_biodata(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)

        if 'application_form' in request_data['filters']['personnel_file_reports_selected']:
            generate_application_form(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'employee_orientation' in request_data['filters']['personnel_file_reports_selected']:
            generate_employee_orientation(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'employee_personal_details' in request_data['filters']['personnel_file_reports_selected']:
            generate_employee_personal_details(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)

        if 'form_no_16' in request_data['filters']['personnel_file_reports_selected']:
            generate_form_no_16(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'form_f_front' in request_data['filters']['personnel_file_reports_selected']:
            generate_form_f_front(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'form_f_back' in request_data['filters']['personnel_file_reports_selected']:
            generate_form_f_back(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'confirmation_letter' in request_data['filters']['personnel_file_reports_selected']:
            generate_confirmation_letter(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'esi_form_1' in request_data['filters']['personnel_file_reports_selected']:
            generate_esi_form_1(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'duty_join' in request_data['filters']['personnel_file_reports_selected']:
            generate_duty_join(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'pf_form_2_front' in request_data['filters']['personnel_file_reports_selected']:
            generate_pf_form_2_front(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'pf_form_2_back' in request_data['filters']['personnel_file_reports_selected']:
            generate_pf_form_2_back(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'probation' in request_data['filters']['personnel_file_reports_selected']:
            generate_probation(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'form_11' in request_data['filters']['personnel_file_reports_selected']:
            generate_form_11(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
        if 'appointment_letter_front' in request_data['filters']['personnel_file_reports_selected']:
            if request_data['filters']['language'] == 'english':
                generate_appointment_letter_front_english(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
            else:
                generate_appointment_letter_front_hindi(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)


        if 'appointment_letter_back' in request_data['filters']['personnel_file_reports_selected']:
            if request_data['filters']['language'] == 'english':
                generate_appointment_letter_back_english(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
            else:
                generate_appointment_letter_back_hindi(personnel_file_reports, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin)
        
    buffer = bytes(personnel_file_reports.output())
    yield buffer