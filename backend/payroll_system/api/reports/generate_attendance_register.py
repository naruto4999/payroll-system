from fpdf import FPDF
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeAttendance, EmployeeSalaryDetail
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar

width_of_columns = {
        "serial_number": 4,
        "date": 8,
        "attendance_total": 12,
        "hrs_total": 20,
    }

max_days_in_month = 31

class FPDF(FPDF):
        def __init__(self, my_date, company_name, company_address, default_cell_height, *args, **kwargs):
            self.my_date = my_date
            self.company_name = company_name
            self.company_address = company_address
            self.default_cell_height = default_cell_height
            super().__init__(*args, **kwargs)

        def header(self):
            # Set Font for Company and add Company name
            self.set_font('Helvetica', 'B', 15)
            self.cell(0, 8, self.company_name, align="L", new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Address and add Address
            self.set_font('Helvetica', 'B', 9)
            self.cell(0, 4, self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Month and Year and add Month and Year
            self.cell(0, 6, self.my_date.strftime("Attendance Register for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

            #Drawing the instructoins on the top
            self.set_font('Helvetica', '', 8)
            self.cell(0, 5, '1.In Time    2.Out Time    3.Total Working Hours    4.Late Hours    5.O.T Hours    6.Attendance Status', align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

            # Drawing the column header for the Serial Number Column
            position_before_drawing_header_columns = {"x": self.get_x(), "y": self.get_y()}
            self.set_line_width(0.3)
            self.set_font('Helvetica', 'B', 6)
            self.cell(width_of_columns['serial_number'], self.default_cell_height, '', align="L", new_x="RIGHT", border=0)

            #Drawing the column header for all the date columns
            x_tracker = self.get_x()
            num_days_in_month = calendar.monthrange(self.my_date.year, self.my_date.month)[1]
            for date in range(max_days_in_month):
                if date+1 <= num_days_in_month: 
                    date_obj = self.my_date + relativedelta(days=date)
                    self.multi_cell(w=width_of_columns['date'], h=self.default_cell_height, txt=f'{date+1}\n{date_obj.strftime("%a")}', align="C", new_x='RIGHT', new_y='TOP', border=1)
                    x_tracker += width_of_columns['date']
                    self.set_xy(x=x_tracker, y=position_before_drawing_header_columns['y'])
                else:
                    self.multi_cell(w=width_of_columns['date'], h=self.default_cell_height*2, txt=f'', align="C", new_x='RIGHT', new_y='TOP', border=1)
                    x_tracker += width_of_columns['date']
                    self.set_xy(x=x_tracker, y=position_before_drawing_header_columns['y'])
            
            #Drawing Header for the Attendance Total and Hrs Total
            self.multi_cell(w=width_of_columns['attendance_total'], h=self.default_cell_height, txt=f'Atd\nTotal', align="C", border=1)
            x_tracker+= width_of_columns['attendance_total']
            self.set_xy(x=x_tracker, y=position_before_drawing_header_columns['y'])
            self.multi_cell(w=width_of_columns['hrs_total'], h=self.default_cell_height, txt=f'Hrs\nTotal', align="C", border=1, new_x="LMARGIN", new_y='NEXT')
            # self.set_xy(x=position_before_drawing_header_columns['x'], y=position_before_drawing_header_columns['y'])




# Create instance of FPDF class
def generate_attendance_register(request_data, employees):
    print('starting to create the attendance register')
    generative_leaves = LeaveGrade.objects.filter(company_id=request_data['company'], generate_frequency__isnull=False)
    default_cell_height = 3
    employee_intro_cell_height = 4
    default_number_of_cells_in_row = max(6, len(generative_leaves)+2)
    group_by_department_cell_height = 5
    #210-33-10 = 167 (33 is header height and 10 is total of top and bottom margin)
    rows_per_page = 167//(employee_intro_cell_height+(default_number_of_cells_in_row*default_cell_height))

    if request_data['filters']['group_by'] != 'none':
        rows_per_page = 167//(employee_intro_cell_height+(default_number_of_cells_in_row*default_cell_height)+group_by_department_cell_height)
    print(f"Rows Per Page: {rows_per_page}")


    #Dimensions of A4 sheet is 210 x 297 mm and there is 6 mm margin on left and right leaving us with 285mm
    employee_intro_width = {
        'serial_number': 20,
        'paycode': 35,
        'acn': 20,
        'name' : 70,
        # 'shift' : 40,
        'designation' : 50,
        'paid_work_days' : 45
    }


    # default_number_of_cells_in_row = max(len(generative_leaves)+2, 8, len(earnings_head)+1)
    company_details = None
    try: company_details = CompanyDetails.objects.filter(company_id=request_data['company']).first()
    except: pass
    attendance_register = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=company_details.company.name if company_details else '',company_address=company_details.address if company_details else '',default_cell_height=default_cell_height, orientation="L", unit="mm", format="A4")
    
    #Page settings
    attendance_register.set_margins(left=6, top=4, right=6)
    attendance_register.add_page()
    attendance_register.set_auto_page_break(auto=True, margin = 4)
    initial_coordinates_after_header = {"x": attendance_register.get_x(), "y": attendance_register.get_y()}
    print(attendance_register.get_y())

    row_number = 0
    num_days_in_month = calendar.monthrange(request_data['year'], request_data['month'])[1]
    for employee_index, employee in enumerate(employees):
        salary_detail = EmployeeSalaryDetail.objects.filter(employee=employee)
        print(salary_detail)
        if not salary_detail.exists():
            continue
        row_number += 1
        attendance_records = EmployeeAttendance.objects.filter(employee=employee, date__range=[date(request_data['year'], request_data['month'], 1), date(request_data['year'], request_data['month'], num_days_in_month)])
        totals = {
            'total_working_hrs': 0,
            'total_late': 0
        }

        if request_data['filters']['group_by'] != 'none':
            try:
                current_employee_department = employee.employee_professional_detail.department
                previous_employee_department = employees[employee_index-1].employee_professional_detail.department if employee_index!=0 else None
                if employee_index == 0 or current_employee_department != previous_employee_department:
                    attendance_register.set_font("Helvetica", size=10, style="B")
                    attendance_register.cell(w=0, h=group_by_department_cell_height, text=f'{current_employee_department.name if current_employee_department else "No Department"}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
            except:
                pass
        ##Employee Intro Details
        attendance_register.set_font('Helvetica', 'B', 7)
        designation = ''
        try: designation = employee.employee_professional_detail.designation.name
        except: pass
        attendance_register.cell(w=employee_intro_width['serial_number'], h=employee_intro_cell_height, text=f'SN : {employee_index+1}', align="L",  new_x="RIGHT", new_y='TOP', border=0)
        attendance_register.cell(employee_intro_width['paycode'], employee_intro_cell_height, f'Paycode : {employee.paycode}', align="L",  new_x="RIGHT", new_y='TOP', border=0)
        attendance_register.cell(employee_intro_width['acn'], employee_intro_cell_height, f'ACN : {employee.attendance_card_no}', align="L",  new_x="RIGHT",new_y='TOP', border=0)
        attendance_register.cell(employee_intro_width['name'], employee_intro_cell_height, f'Name : {employee.name}', align="L",  new_x="RIGHT", new_y='TOP', border=0)
        attendance_register.cell(employee_intro_width['designation'], employee_intro_cell_height, f'Desig : {designation}', align="L",  new_x="RIGHT", new_y='TOP', border=0)
        #Paid/Present Days
        paid_days_count = ''
        present_count = ''
        weekly_off_days_count = ''
        holiday_days_count = ''
        employee_monthly_details = None
        try:
            employee_monthly_details = employee.monthly_attendance_details.filter(date=date(request_data['year'], request_data['month'], 1)).first()
            paid_days_count = int(employee_monthly_details.paid_days_count/2) if employee_monthly_details.paid_days_count/2%1==0 else employee_monthly_details.paid_days_count/2
            present_count = int(employee_monthly_details.present_count/2) if employee_monthly_details.present_count/2%1==0 else employee_monthly_details.present_count/2
            weekly_off_days_count = int(employee_monthly_details.weekly_off_days_count/2) if employee_monthly_details.weekly_off_days_count/2%1==0 else employee_monthly_details.weekly_off_days_count/2
            holiday_days_count = int(employee_monthly_details.holiday_days_count/2) if employee_monthly_details.holiday_days_count/2%1==0 else employee_monthly_details.holiday_days_count/2
        except:
            pass
        #Generative Leave
        generative_leave_text = ''
        employee_generative_leaves = None
        try:
            employee_generative_leaves = EmployeeGenerativeLeaveRecord.objects.filter(employee=employee, date=date(request_data['year'], request_data['month'], 1)).order_by('leave__name')
            generative_leave_text = "\n".join(f"{leave.leave.name} : {int(leave.leave_count/2) if leave.leave_count/2%1==0 else leave.leave_count/2}" for leave in employee_generative_leaves)
        except:
            pass
        attendance_register.cell(employee_intro_width['paid_work_days'], employee_intro_cell_height, f'Paid / Work Days : {paid_days_count} / {present_count}', align="L",  new_x="LMARGIN", new_y='NEXT', border=0)
        attendance_register.set_font('Helvetica', '', 6)
        attendance_register.set_line_width(0.2)
        attendance_register.multi_cell(w=width_of_columns['serial_number'], h=default_cell_height, txt=f'1\n2\n3\n4\n5\n6', align="C", border=1, new_x="RIGHT", new_y='TOP')
        
        coordinates_after_intro = {"x": attendance_register.get_x(), "y": attendance_register.get_y()}
        ##Cell of Attendance Register
        for day in range(num_days_in_month):
            attendance_register.set_xy(x=attendance_register.get_x(), y=coordinates_after_intro['y'])
            current_date = date(request_data['year'], request_data['month'], day+1)
            specific_date_record = None
            try: specific_date_record = attendance_records.filter(date=current_date).first()
            except: pass
            in_time_str = ''
            out_time_str = ''
            total_working = ''
            late_hrs = ''
            ot_hrs = ''
            attendance_status = ' '
            #Getting in Time and Out time
            in_time = None
            out_time = None
            if specific_date_record:
                if specific_date_record.manual_in:
                    in_time = specific_date_record.manual_in
                    in_time_str = in_time.strftime('%H:%M')
                elif specific_date_record.machine_in:
                    in_time = specific_date_record.machine_in
                    in_time_str = in_time.strftime('%H:%M')
                if specific_date_record.manual_out:
                    out_time = specific_date_record.manual_out
                    out_time_str = out_time.strftime('%H:%M')
                elif specific_date_record.machine_out:
                    out_time = specific_date_record.machine_out
                    out_time_str = out_time.strftime('%H:%M')
                if in_time is not None and out_time is not None:
                    # in_time = datetime.strptime(in_time_str, '%H:%M').time()
                    # out_time = datetime.strptime(out_time_str, '%H:%M').time()
                    # Convert time objects to datetime objects with a common date
                    common_date = datetime(1900, 1, 1)
                    in_datetime = datetime.combine(common_date, in_time)
                    out_datetime = datetime.combine(common_date, out_time)

                    if out_time < in_time:
                        out_datetime += timedelta(hours=24)

                    # Calculate the time difference
                    time_difference = out_datetime - in_datetime
                    totals['total_working_hrs'] += time_difference.seconds
                    hours, remainder = divmod(time_difference.seconds, 3600)
                    minutes = remainder // 60
                    total_working = f'{hours:02d}:{minutes:02d}'
                #Calculating late min and hrs
                if specific_date_record.late_min is not None:
                    totals['total_late'] += specific_date_record.late_min*60
                    latehours, lateminutes = divmod(specific_date_record.late_min, 60)
                    late_hrs = f'{latehours:02d}:{lateminutes:02d}'

                #Calculating OT min and hrs
                if specific_date_record.ot_min is not None:
                    othours, otminutes = divmod(specific_date_record.ot_min, 60)
                    ot_hrs = f'{othours:02d}:{otminutes:02d}'
                
                #Attendance Status
                if specific_date_record.first_half is not None and specific_date_record.second_half is not None:
                    attendance_status = f'{specific_date_record.first_half.name}:{specific_date_record.second_half.name}'
            attendance_register.rect(x=attendance_register.get_x(), y=attendance_register.get_y(), w=width_of_columns['date'], h=default_cell_height*default_number_of_cells_in_row)
            attendance_register.multi_cell(w=width_of_columns['date'], h=default_cell_height, txt=f'{in_time_str}\n{out_time_str}\n{total_working}\n{late_hrs}\n{ot_hrs}', align="C", new_x='LEFT', new_y='TOP', border=0)

            #Printing just the attendance status in smaller font
            attendance_register.set_font('Helvetica', '', 4.5)
            attendance_register.set_xy(x=attendance_register.get_x(), y=attendance_register.get_y()+(default_cell_height*5))
            attendance_register.cell(width_of_columns['date'], default_cell_height, attendance_status, new_x="RIGHT", new_y='TOP', align='C', border=0)
            attendance_register.set_font('Helvetica', '', 6)
        
        #Attendance Total
        attendance_register.set_xy(x=attendance_register.get_x(), y=coordinates_after_intro['y'])
        attendance_register.rect(x=attendance_register.get_x(), y=attendance_register.get_y(), w=width_of_columns['attendance_total'], h=default_cell_height*default_number_of_cells_in_row)
        attendance_register.multi_cell(w=width_of_columns['attendance_total'], h=default_cell_height, txt=f'WO : {weekly_off_days_count}\nHD : {holiday_days_count}\n{generative_leave_text}', align="L", new_x='RIGHT', new_y='TOP', border=0)
        
        attendance_register.rect(x=attendance_register.get_x(), y=attendance_register.get_y(), w=width_of_columns['hrs_total'], h=default_cell_height*default_number_of_cells_in_row)
        #Total Working hrs text
        hours, remainder = divmod(totals['total_working_hrs'], 3600)
        minutes = remainder // 60
        total_working_hrs_text = f'{hours:02d}:{minutes:02d}'

        tota_ot_hrs_text = ''
        total_late_hrs_text = ''
        if employee_monthly_details:
            #Total OT hrs text
            print(f"Employee: {employee.name}")
            othours, otminutes = divmod(employee_monthly_details.net_ot_minutes_monthly, 60)
            tota_ot_hrs_text = f'{othours:02d}:{otminutes:02d}'

            #Total Late hrs text
            hours, remainder = divmod(totals['total_late'], 3600)
            minutes = remainder // 60
            total_late_hrs_text = f'{hours:02d}:{minutes:02d}'

        attendance_register.multi_cell(w=width_of_columns['hrs_total'], h=(default_cell_height*default_number_of_cells_in_row)/3, txt=f'T.hrs : {total_working_hrs_text}\nOT.hrs : {tota_ot_hrs_text}\nLt.hrs : {total_late_hrs_text}', align="L", new_x='LMARGIN', new_y='NEXT', border=0)

        if (row_number)%rows_per_page==0 and row_number!=0 and row_number<(len(employees)):
            attendance_register.add_page()
            attendance_register.set_xy(x=initial_coordinates_after_header['x'], y=initial_coordinates_after_header['y'])
        
    # Save the pdf with name .pdf
    buffer = bytes(attendance_register.output())
    yield buffer