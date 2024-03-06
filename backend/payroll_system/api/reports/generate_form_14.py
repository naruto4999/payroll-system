from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount, LeaveGrade, EarningsHead
from datetime import date
import calendar
from django.db.models import Q
# from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

#A4 size 210 x 297 mm
width_of_columns = {
       "right_intro_header": 80,
       "summary_header": 30,
       "summary_value": 20,
       "summary_gap": 10,
       #Main Table
       "wages_period": 20,
       "wages_earned": 15,
       "no_of_days_worked": 35,
       "total_of_columns": 10,
       "leave_of_credit": 30,
       "total_of_columns_8_9": 8,
       "whether_leave_in_accordance": 12,
       "leave_enjoyed": 60,
       "balance_of_leave_of_credit": 10,
       "rate_of_wages": 15,
       "cash_equivalent": 16,
       "rate_of_wages_for_leave_period": 12,
       "cl": 9,
       "sl": 9,
       "blank": 8,
       "remarks": 15
    }

def generate_form_14(user, request_data, employees):
    default_cell_height = 5
    default_cell_height_small = 4
    default_cell_height_extra_small = 3.5
    default_cell_height_for_heading = 8
    left_margin = 6
    right_margin = 7
    bottom_margin = 3
    top_margin = 6
    height_of_table_header = 30
    height_of_table_row = 8.5

    form_14 = FPDF(orientation="L", unit="mm", format="A4")

    #Page settings
    form_14.set_margins(left=left_margin, top=top_margin, right=right_margin)
    form_14.add_page()
    form_14.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates = {"x": form_14.get_x(), "y": form_14.get_y()}
    form_14.set_font("Helvetica", size=9)

    months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
    ]

    def generate_vertical_text_at_current_pos(width, height, text, lines_expected):
        a=90
        x=form_14.get_x()
        y=form_14.get_y() + height
        form_14.set_xy(x=x, y=y)
        with form_14.rotation(angle=a, x=x, y=y):
            form_14.multi_cell(w=height, h=width/lines_expected, text=text, align='L', border=1)


    for index, employee in enumerate(employees):
        form_14.set_line_width(width=0.4)
        ##Intro on left
        #ACN
        form_14.set_font("Helvetica", size=9, style='')
        form_14.cell(w=0, h=default_cell_height, text=f"ACN : {employee.employee.attendance_card_no}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        #Department
        employee_department = ''
        try: employee_department = employee.department.name
        except: pass
        form_14.cell(w=0, h=default_cell_height, text=f"Department : {employee_department}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        #Adult Child Worker
        form_14.cell(w=0, h=default_cell_height, text=f"Serial No. in Register Adult/Child/Worker : ", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        #DOJ
        employee_doj = ''
        try: employee_doj = employee.date_of_joining.strftime('%d-%b-%Y')
        except: pass
        form_14.cell(w=0, h=default_cell_height, text=f"Date of Entry into Service : {employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        ##Center Heading
        form_14.set_xy(x=initial_coordinates['x'], y=initial_coordinates['y'])
        form_14.set_font("Helvetica", size=16, style='B')
        form_14.cell(w=0, h=default_cell_height_for_heading, text=f'Form No. 14', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
        form_14.set_font("Helvetica", size=9, style='')
        form_14.cell(w=0, h=default_cell_height, text=f'(Rule No. 102)', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
        form_14.set_font("Helvetica", size=16, style='B')
        form_14.cell(w=0, h=default_cell_height_for_heading, text=f'LEAVE WITH WAGES REGISTERS', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
        form_14.set_font("Helvetica", size=12, style='')
        #Centering the Company Name
        name_heading_width = form_14.get_string_width(f'Name of Organization : {employee.company.name}')
        form_14.set_xy(x=(297-name_heading_width)/2-4, y=form_14.get_y())
        form_14.cell(w=None, h=default_cell_height, text=f'Name of Organization :', align="L", new_x="RIGHT", new_y='TOP', border=0)
        form_14.set_font("Helvetica", size=12, style='B')
        form_14.cell(w=None, h=default_cell_height, text=f'{employee.company.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        
        ##Intro on right
        form_14.set_xy(x=(297-right_margin-width_of_columns['right_intro_header']), y=initial_coordinates['y'])
        form_14.set_font("Helvetica", size=9, style='')
        #Paycode
        form_14.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f'Paycode : {employee.employee.paycode}', align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Name
        form_14.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f'Name : {employee.employee.name}', align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Father Name
        form_14.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f"Father's/Husband's Name : {employee.employee.father_or_husband_name if employee.employee.father_or_husband_name else ''}", align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Resign date (add when resignation option is implemented)
        form_14.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f"Date of Discharge :", align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Lieu
        form_14.multi_cell(w=width_of_columns['right_intro_header']-35, h=default_cell_height, text=f"Date and Amount of Payment made in Lieu of leave due", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        
        form_14.set_font("Helvetica", size=6.5, style='B')
        initial_coordinates_before_table_headers = {"x": form_14.get_x(), "y": form_14.get_y()}
        ##Table Headers 
        #Wages Period
        form_14.cell(w=width_of_columns['wages_period'], h=height_of_table_header/3, text=f"Wages Period", align="C", new_x="LEFT", new_y='NEXT', border='TLR')
        form_14.cell(w=width_of_columns['wages_period'], h=height_of_table_header/3, text=f"From: Jan {request_data['year']}", align="L", new_x="LEFT", new_y='NEXT', border='LR')
        form_14.cell(w=width_of_columns['wages_period'], h=height_of_table_header/3, text=f"To: Dec {request_data['year']}", align="L", new_x="RIGHT", new_y='NEXT', border='BLR')
        # form_14.cell(w=width_of_columns['wages_period'], h=3.5, text=f"1", align="C", new_x="RIGHT", new_y='NEXT', border='BLR')

        #Wages Earned
        form_14.set_xy(x=form_14.get_x(), y=initial_coordinates_before_table_headers['y'])
        form_14.rect(x=form_14.get_x(), y=form_14.get_y(), w=width_of_columns['wages_earned'], h=height_of_table_header)
        generate_vertical_text_at_current_pos(width_of_columns['wages_earned'], height_of_table_header, "Wages earned during wages period", 2)

        #Number of days worked
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned'], y=initial_coordinates_before_table_headers['y'])
        form_14.multi_cell(w=width_of_columns['no_of_days_worked'], h=default_cell_height_small, text=f"No. of days worked during the calendar year", align="C", new_x="LEFT", new_y='NEXT', border=1)
        #Number of work days per
        generate_vertical_text_at_current_pos((width_of_columns['no_of_days_worked'])/4, height_of_table_header-(default_cell_height_small*2), "No. of work days per", 2)
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']/4, y=initial_coordinates_before_table_headers['y']+(default_cell_height_small*2))
        generate_vertical_text_at_current_pos((width_of_columns['no_of_days_worked'])/4, height_of_table_header-(default_cell_height_small*2), "No. of days lays off", 2)
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']/4*2, y=initial_coordinates_before_table_headers['y']+(default_cell_height_small*2))
        generate_vertical_text_at_current_pos((width_of_columns['no_of_days_worked'])/4, height_of_table_header-(default_cell_height_small*2), "No. of maternity leave days", 2)
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']/4*3, y=initial_coordinates_before_table_headers['y']+(default_cell_height_small*2))
        generate_vertical_text_at_current_pos((width_of_columns['no_of_days_worked'])/4, height_of_table_header-(default_cell_height_small*2), "Leave enjoyed days E/L", 2)

        #Total of columns
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked'], y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['total_of_columns'], height_of_table_header, "Total of columns 3 and 6", 1)

        #Leave of Credit
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns'], y=initial_coordinates_before_table_headers['y'])
        form_14.cell(w=width_of_columns['leave_of_credit'], h=default_cell_height_small, text=f"Leave Credit", align="C", new_x="LEFT", new_y='NEXT', border=1)
        form_14.rect(x=form_14.get_x(), y=form_14.get_y(), w=width_of_columns['leave_of_credit']/2, h=height_of_table_header-default_cell_height_small)
        form_14.multi_cell(w=width_of_columns['leave_of_credit']/2, h=default_cell_height_small, text=f"Balance of leave from preceeding year", align="C", new_x="RIGHT", new_y='TOP', border=0)
        form_14.rect(x=form_14.get_x(), y=form_14.get_y(), w=width_of_columns['leave_of_credit']/2, h=height_of_table_header-default_cell_height_small)
        form_14.multi_cell(w=width_of_columns['leave_of_credit']/2, h=default_cell_height_small, text=f"Leave earned during the year mentioned in column", align="C", new_x="RIGHT", new_y='TOP', border=0)
        
        #Total of columns
        form_14.set_xy(x=form_14.get_x(), y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['total_of_columns_8_9'], height_of_table_header, "Total of columns 8 and 9", 1)
        
        #whether_leave_in_accordance
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9'], y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['whether_leave_in_accordance'], height_of_table_header, "Whether leave in accordance with scheme under sec. 79(8) was refused", 4)
        
        #Leave Enjoyed
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9']+width_of_columns['whether_leave_in_accordance'], y=initial_coordinates_before_table_headers['y'])
        form_14.cell(w=width_of_columns['leave_enjoyed'], h=default_cell_height_small, text=f"Leave Enjoyed", align="C", new_x="LEFT", new_y='NEXT', border=1)
        form_14.multi_cell(w=width_of_columns['leave_enjoyed']/5*4, h=(height_of_table_header-default_cell_height_small), text=f"Date of leave enjoyed", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.multi_cell(w=width_of_columns['leave_enjoyed']/5, h=(height_of_table_header-default_cell_height_small)/2, text=f"No. of Days", align="C", new_x="RIGHT", new_y='TOP', border=1)
        # generate_vertical_text_at_current_pos(width_of_columns['leave_enjoyed'], height_of_table_header, "Whether leave in accordance with scheme under sec. 79(8) was refused", 4)
        
        #Balance of leave of credit
        form_14.set_xy(x=form_14.get_x(), y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['balance_of_leave_of_credit'], height_of_table_header, "Balance of leave of credit", 1)
        
        #Rate of Wages
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9']+width_of_columns['whether_leave_in_accordance']+width_of_columns['leave_enjoyed']+width_of_columns['balance_of_leave_of_credit'], y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['rate_of_wages'], height_of_table_header, "Normal rate of wages per month / P.W.D", 2)
        
        #Cash Equivalent
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9']+width_of_columns['whether_leave_in_accordance']+width_of_columns['leave_enjoyed']+width_of_columns['balance_of_leave_of_credit']+width_of_columns['rate_of_wages'], y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['cash_equivalent'], height_of_table_header, "Cash equivalent of advantage according through concessional rate of food agains & other articles", 5)
        
        #Rate of wages for the leave period
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9']+width_of_columns['whether_leave_in_accordance']+width_of_columns['leave_enjoyed']+width_of_columns['balance_of_leave_of_credit']+width_of_columns['rate_of_wages']+width_of_columns['cash_equivalent'], y=initial_coordinates_before_table_headers['y'])
        generate_vertical_text_at_current_pos(width_of_columns['rate_of_wages_for_leave_period'], height_of_table_header, "Rate of wages for the leave period (Total of other articles)", 3)
        
        #CL
        form_14.set_xy(x=initial_coordinates_before_table_headers['x']+width_of_columns['wages_period']+width_of_columns['wages_earned']+width_of_columns['no_of_days_worked']+width_of_columns['total_of_columns']+width_of_columns['leave_of_credit']+width_of_columns['total_of_columns_8_9']+width_of_columns['whether_leave_in_accordance']+width_of_columns['leave_enjoyed']+width_of_columns['balance_of_leave_of_credit']+width_of_columns['rate_of_wages']+width_of_columns['cash_equivalent']+width_of_columns['rate_of_wages_for_leave_period'], y=initial_coordinates_before_table_headers['y'])
        form_14.cell(w=width_of_columns['cl'], h=height_of_table_header, text=f"CL", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #SL
        form_14.cell(w=width_of_columns['cl'], h=height_of_table_header, text=f"SL", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #Blank
        form_14.cell(w=width_of_columns['blank'], h=height_of_table_header, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
        #Remarks
        form_14.cell(w=width_of_columns['remarks'], h=height_of_table_header, text=f"Remarks", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

        ##Columns Numbering
        form_14.cell(w=width_of_columns['wages_period'], h=default_cell_height_small, text=f"1", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['wages_earned'], h=default_cell_height_small, text=f"2", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=default_cell_height_small, text=f"3", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=default_cell_height_small, text=f"4", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=default_cell_height_small, text=f"5", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=default_cell_height_small, text=f"6", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['total_of_columns'], h=default_cell_height_small, text=f"7", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['leave_of_credit']/2, h=default_cell_height_small, text=f"8", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['leave_of_credit']/2, h=default_cell_height_small, text=f"9", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['total_of_columns_8_9'], h=default_cell_height_small, text=f"10", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['whether_leave_in_accordance'], h=default_cell_height_small, text=f"11", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['leave_enjoyed']/5*4, h=default_cell_height_small, text=f"12", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['leave_enjoyed']/5, h=default_cell_height_small, text=f"13", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['balance_of_leave_of_credit'], h=default_cell_height_small, text=f"14", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['rate_of_wages'], h=default_cell_height_small, text=f"15", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['cash_equivalent'], h=default_cell_height_small, text=f"16", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['rate_of_wages_for_leave_period'], h=default_cell_height_small, text=f"17", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['cl'], h=default_cell_height_small, text=f"18", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['sl'], h=default_cell_height_small, text=f"19", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['blank'], h=default_cell_height_small, text=f"20", align="C", new_x="RIGHT", new_y='TOP', border=1)
        form_14.cell(w=width_of_columns['remarks'], h=default_cell_height_small, text=f"21", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

        ##Main Table rows
        form_14.set_font("Helvetica", size=6.5, style='')
        form_14.set_line_width(width=0.3)

        current_year_current_emp_el_credit = 0
        leaves_dict = {
            'EL': {
                'leave_earned': 0,
                'leave_availed': 0
            },
            'CL': {
                'leave_earned': 0,
                'leave_availed': 0
            },
            'SL': {
                'leave_earned': 0,
                'leave_availed': 0
            }
        }

        total_work_days = 0
        for month_index, month in enumerate(months):
            #Prepared Salary
            current_month_salary = None
            try: current_month_salary = employee.employee.salaries_prepared.filter(date=date(request_data['year'], month_index+1, 1)).first()
            except: pass
            
            #Earned Amounts
            earned_amounts = None
            if current_month_salary:
                earned_amounts = current_month_salary.current_salary_earned_amounts.all()
            
            #Total Earned
            total_earnings_amount = None
            if earned_amounts and earned_amounts.exists():
                total_earnings_amount = 0
                for earned in earned_amounts:
                    total_earnings_amount += (earned.earned_amount-earned.arear_amount)
            # print(f"Total Earned for the month: {month}: {total_earnings_amount}")

            # #Total Deductions
            # net_payable = None
            # if current_month_salary:
            #     total_deductions = current_month_salary.pf_deducted+current_month_salary.esi_deducted+current_month_salary.vpf_deducted+current_month_salary.advance_deducted+current_month_salary.tds_deducted
            #     net_payable = total_earnings_amount-total_deductions

            form_14.cell(w=width_of_columns['wages_period'], h=height_of_table_row, text=f"{month}", align="C", new_x="RIGHT", new_y='TOP', border=1)
            form_14.cell(w=width_of_columns['wages_earned'], h=height_of_table_row, text=f"{total_earnings_amount if total_earnings_amount else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

            #Work Days
            working_days_str = ''
            try: 
                employee_monthly_attendance_details = employee.employee.monthly_attendance_details.filter(user=user, date=date(request_data['year'], month_index+1, 1)).first()
                working_days = employee_monthly_attendance_details.present_count
                total_work_days += working_days
                working_days_str =  working_days/2
            except: 
                pass

            form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=height_of_table_row, text=f"{working_days_str}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Lays Off
            form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Maternity Leave
            form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
            #EL days/leave enjoyed
            leave_grades = LeaveGrade.objects.filter(user=employee.user, company_id=request_data['company'])

            el_days_str = ''
            el = leave_grades.filter(name="EL").first()

            try:
                montly_el = employee.employee.generative_leave_record.filter(user=user, date=date(request_data['year'], month_index+1, 1), leave=el).first()
                number_of_el = montly_el.leave_count
                leaves_dict['EL']['leave_availed'] +=(number_of_el/2)
                if number_of_el>0:
                    current_year_current_emp_el_credit += number_of_el
                    el_days_str =  number_of_el/2
            except:
                pass
            form_14.cell(w=width_of_columns['no_of_days_worked']/4, h=height_of_table_row, text=f"{el_days_str}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Updating leaves dict
            # try:
            #     print(f"Number of EL: {number_of_el/2} Month: {month_index}")
            #     leaves_dict['EL']['leave_availed'] +=(number_of_el/2)
            # except:
            #     pass

            #Total of columns
            work_days = 0
            el_days = 0
            if working_days_str != '':
                work_days = working_days_str
            if el_days_str != '':
                el_days = el_days_str
            total_of_columns = work_days + el_days
            form_14.cell(w=width_of_columns['total_of_columns'], h=height_of_table_row, text=f"{total_of_columns if total_of_columns !=0 else ''}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Leave of Credit
            form_14.cell(w=width_of_columns['leave_of_credit']/2, h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)
            form_14.cell(w=width_of_columns['leave_of_credit']/2, h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Total of columns
            form_14.cell(w=width_of_columns['total_of_columns_8_9'], h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Whether Leave in accordance
            form_14.cell(w=width_of_columns['whether_leave_in_accordance'], h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Date of leaves
            first_day_of_month = date(request_data['year'], month_index+1, 1)
            num_days_in_month = calendar.monthrange(request_data['year'], month_index+1)[1]
            last_day_of_month = date(request_data['year'], month_index+1, num_days_in_month)

            dates_of_el_str = ''
            try:
                employee_attendance_objects = employee.employee.attendance.filter(
                    Q(first_half=el) | Q(second_half=el),
                    date__gte=first_day_of_month,
                    date__lte=last_day_of_month,
                    user=user
                )
                for attendance in employee_attendance_objects:
                    if dates_of_el_str != '':
                        dates_of_el_str += ','
                    dates_of_el_str += str(attendance.date.day)
            except:
                pass
            
            # form14_initial_coordinates = {"x": form_14.get_x(), "y": form_14.get_y()}
            form_14.rect(x=form_14.get_x(), y=form_14.get_y(), w=width_of_columns['leave_enjoyed']/5*4, h=height_of_table_row)
            form_14.multi_cell(w=width_of_columns['leave_enjoyed']/5*4, h=height_of_table_row/2, text=f"{dates_of_el_str}", align="L", new_x="RIGHT", new_y='TOP', border=0)
            # form_14.set_xy(x=form14_initial_coordinates['x'])

            #EL Days
            form_14.cell(w=width_of_columns['leave_enjoyed']/5, h=height_of_table_row, text=f"{el_days_str}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Balance of leave of credit
            form_14.cell(w=width_of_columns['balance_of_leave_of_credit'], h=height_of_table_row, text=f"{current_year_current_emp_el_credit/2 if current_year_current_emp_el_credit/2>0 else''}", align="C", new_x="RIGHT", new_y='TOP', border=1)
        
            #Rate of Wages
            total_earnings_rate = None
            try:
                total_earnings_rate = 0
                earnings_heads = EarningsHead.objects.filter(company=employee.company, user=employee.user)
                employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee.employee, from_date__lte=first_day_of_month, to_date__gte=first_day_of_month)
                for head in earnings_heads:
                    salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
                    if salary_for_particular_earning_head.exists():
                        total_earnings_rate += salary_for_particular_earning_head.first().value
            except: 
                pass
            form_14.cell(w=width_of_columns['rate_of_wages'], h=height_of_table_row, text=f"{total_earnings_rate if total_earnings_rate else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)

            #Cash Equivalent
            form_14.cell(w=width_of_columns['cash_equivalent'], h=height_of_table_row, text=f"", align="c", new_x="RIGHT", new_y='TOP', border=1)

            #rate_of_wages_for_leave_period
            form_14.cell(w=width_of_columns['rate_of_wages_for_leave_period'], h=height_of_table_row, text=f"", align="c", new_x="RIGHT", new_y='TOP', border=1)

            #CL
            cl_days_str = ''
            cl = leave_grades.filter(name="CL").first()
            try:
                montly_cl = employee.employee.generative_leave_record.filter(user=user, date=date(request_data['year'], month_index+1, 1), leave=cl).first()
                number_of_cl = montly_cl.leave_count
                leaves_dict['CL']['leave_availed'] +=(number_of_cl/2)
                if number_of_cl>0:
                    cl_days_str =  number_of_cl/2
            except:
                pass

            #Updating leaves dict
            # try:
            #     leaves_dict['CL']['leave_availed'] +=(number_of_cl/2)
            # except:
            #     pass
            form_14.cell(w=width_of_columns['cl'], h=height_of_table_row, text=f"{cl_days_str}", align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #SL
            sl_days_str = ''
            sl = leave_grades.filter(name="SL").first()
            try:
                montly_sl = employee.employee.generative_leave_record.filter(user=user, date=date(request_data['year'], month_index+1, 1), leave=sl).first()
                number_of_sl = montly_sl.leave_count
                leaves_dict['SL']['leave_availed'] +=(number_of_sl/2)
                if number_of_sl>0:
                    sl_days_str =  number_of_sl/2
            except:
                pass

            #Updating leaves dict
            # try:
            #     leaves_dict['SL']['leave_availed'] +=(number_of_sl/2)
            # except:
            #     pass
            form_14.cell(w=width_of_columns['sl'], h=height_of_table_row, text=f"{sl_days_str}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Blank
            form_14.cell(w=width_of_columns['blank'], h=height_of_table_row, text=f"", align="C", new_x="RIGHT", new_y='TOP', border=1)
            
            #Remarks
            form_14.cell(w=width_of_columns['remarks'], h=height_of_table_row, text=f"", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

        #Total Work Days
        form_14.cell(width_of_columns['wages_period']+width_of_columns['wages_earned'], h=default_cell_height, text=f'Total Days Worked :', align="L", new_x="RIGHT", new_y='TOP', border='TBL')
        form_14.cell(width_of_columns['no_of_days_worked']/4, h=default_cell_height, text=f'{total_work_days/2}', align="R", new_x="LMARGIN", new_y='NEXT', border='TBR')

        initial_coordinates_before_summary = {"x": form_14.get_x(), "y": form_14.get_y()}
        #EL days
        form_14.set_font("Helvetica", size=6.5, style='B')
        try:
            leaves_dict['EL']['leave_earned'] +=(total_work_days/2)//el.generate_frequency
        except:
            pass
        form_14.cell(width_of_columns['summary_header']+width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f'EL', align="C", new_x="LMARGIN", new_y='NEXT', border='TLR')
        form_14.set_font("Helvetica", size=6.5, style='')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Due (Prv. Yr.)', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Earned', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['EL']['leave_earned']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Availed', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['EL']['leave_availed']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Balance Leave', align="L", new_x="RIGHT", new_y='TOP', border='LB')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['EL']['leave_earned']-leaves_dict['EL']['leave_availed']}", align="R", new_x="RIGHT", new_y='TOP', border='RB')
        
        #CL days
        form_14.set_xy(x=form_14.get_x() + width_of_columns['summary_gap'], y=initial_coordinates_before_summary['y'])
        form_14.set_font("Helvetica", size=6.5, style='B')
        try:
            leaves_dict['CL']['leave_earned'] +=(total_work_days/2)//cl.generate_frequency
        except:
            pass
        form_14.cell(width_of_columns['summary_header']+width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f'CL', align="C", new_x="LEFT", new_y='NEXT', border='TLR')
        form_14.set_font("Helvetica", size=6.5, style='')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Due (Prv. Yr.)', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'], y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Earned', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['CL']['leave_earned']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'], y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Availed', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['CL']['leave_availed']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'], y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Balance Leave', align="L", new_x="RIGHT", new_y='TOP', border='LB')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['CL']['leave_earned']-leaves_dict['CL']['leave_availed']}", align="R", new_x="RIGHT", new_y='TOP', border='RB')
        
        #SL days
        form_14.set_xy(x=form_14.get_x() + width_of_columns['summary_gap'], y=initial_coordinates_before_summary['y'])
        form_14.set_font("Helvetica", size=6.5, style='B')
        try:
            leaves_dict['SL']['leave_earned'] +=(total_work_days/2)//sl.generate_frequency
        except:
            pass
        form_14.cell(width_of_columns['summary_header']+width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f'SL', align="C", new_x="LEFT", new_y='NEXT', border='TLR')
        form_14.set_font("Helvetica", size=6.5, style='')
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Due (Prv. Yr.)', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+(width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'])*2, y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Earned', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['SL']['leave_earned']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+(width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'])*2, y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Leave Availed', align="L", new_x="RIGHT", new_y='TOP', border='L')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['SL']['leave_availed']}", align="R", new_x="LMARGIN", new_y='NEXT', border='R')
        form_14.set_xy(x=form_14.get_x()+(width_of_columns['summary_header']+width_of_columns['summary_value']+width_of_columns['summary_gap'])*2, y= form_14.get_y())
        form_14.cell(width_of_columns['summary_header'], h=default_cell_height_extra_small, text=f'Balance Leave', align="L", new_x="RIGHT", new_y='TOP', border='LB')
        form_14.cell(width_of_columns['summary_value'], h=default_cell_height_extra_small, text=f"{leaves_dict['SL']['leave_earned']-leaves_dict['SL']['leave_availed']}", align="R", new_x="LMARGIN", new_y='NEXT', border='RB')
        
        form_14.set_xy(x=form_14.get_x(), y=210-bottom_margin-7)
        form_14.cell(w=0, h=default_cell_height_extra_small, text=f"Signature of Employee", align="L", new_x="LMARGIN", new_y='TOP', border=0)

        if index!=len(employees)-1:
            form_14.add_page()
            form_14.set_xy(x=form_14.get_x(), y=form_14.get_y())

    # Save the pdf with name .pdf
    buffer = bytes(form_14.output())
    yield buffer