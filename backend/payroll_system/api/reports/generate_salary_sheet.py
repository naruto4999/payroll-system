from fpdf import FPDF
from ..models import EmployeeSalaryPrepared, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeePfEsiDetail, EmployeeSalaryDetail, LeaveGrade, EmployeeGenerativeLeaveRecord, EmployeeMonthlyAttendanceDetails, CompanyDetails, EarningsHead, EmployeeSalaryEarning, EarnedAmount, PfEsiSetup
from datetime import date
from django.db.models import Case, When, Value, CharField
import math



width_of_columns = {
        "paycode": 22,
        "employee_name": 54,
        "attendance_detail": 30,
        "salary_wage_rate": 30,
        "earnings": 15,
        "arrears": 15,
        "ot_incentive": 28,
        "total_earnings": 16,
        "deductions": 32,
        "net_payable": 20,
        "signature": 22
    }

# default_cell_height = 5
default_number_of_cells_in_row = 8
header_height = 0
max_name_earning_head_name_length = 5
# default_row_height = 40
#default_number_of_cells_in_row = max(len(generative_leaves)+3, 8) #do this before even starting to draw the row of the slaray of employee



class FPDF(FPDF):
        def __init__(self, my_date, company_name, company_address, *args, **kwargs):
            self.my_date = my_date
            self.company_name = company_name
            self.company_address = company_address
            super().__init__(*args, **kwargs)

        def header(self):
            # Set Font for Company and add Company name
            self.set_font('Arial', 'B', 15)
            self.cell(0, 8, self.company_name, align="L", new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Address and add Address
            self.set_font('Arial', 'B', 9)
            self.cell(0, 4, self.company_address, align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Month and Year and add Month and Year
            self.cell(0, 6, self.my_date.strftime("Salary for the month of %B, %Y"), align="L", new_x="LMARGIN", new_y='NEXT', border=0)

            position_before_drawing_box_for_paycode = {"x": self.get_x(), "y": self.get_y()}

            # Define the coordinates and dimensions of the text block

            self.set_font('Arial', 'B', 8)

            self.set_line_width(0.5)
            self.rect(self.get_x(), self.get_y(), w=width_of_columns["paycode"], h=15)

            #Add Paycode, DOJ, SN header
            self.multi_cell(w=width_of_columns["paycode"], h=5, txt="Pay Code\nS/N\nDOJ", align='C', border=0)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"], y=position_before_drawing_box_for_paycode["y"])

            #Add Employee Name header
            self.multi_cell(w=width_of_columns["employee_name"], h=3.75, txt="Employee Name\nEmployee F/H Name\nDesignation\nDepartment", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"], y=position_before_drawing_box_for_paycode["y"])

            #Add Attendance Detail
            self.multi_cell(w=width_of_columns["attendance_detail"], h=7.5, txt="Attendance\nDetails", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"], y=position_before_drawing_box_for_paycode["y"])

            #Add Salary/Wage Rate
            self.multi_cell(w=width_of_columns["salary_wage_rate"], h=7.5, txt="Salary/Wage\nRate", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"], y=position_before_drawing_box_for_paycode["y"])

            #Add Earnings
            self.multi_cell(w=width_of_columns["earnings"], h=15, txt="Earnings", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=position_before_drawing_box_for_paycode["y"])

            #Add Arrears
            self.multi_cell(w=width_of_columns["arrears"], h=15, txt="Arrears", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"], y=position_before_drawing_box_for_paycode["y"])

            # Add Ot/Incentives
            self.multi_cell(w=width_of_columns["ot_incentive"], h=7.5, txt="O.T\nIncentive", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"], y=position_before_drawing_box_for_paycode["y"])

            # Add Total Earnings
            self.multi_cell(w=width_of_columns["total_earnings"], h=7.5, txt="Total\nEarnings", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"], y=position_before_drawing_box_for_paycode["y"])

            # Add Deductions
            self.multi_cell(w=width_of_columns["deductions"], h=15, txt="Deductions", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"], y=position_before_drawing_box_for_paycode["y"])

            # Add Net Payable
            self.multi_cell(w=width_of_columns["net_payable"], h=7.5, txt="Net\nPayable", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"]+width_of_columns["net_payable"], y=position_before_drawing_box_for_paycode["y"])

            # Add Signature of employee and Remarks
            self.multi_cell(w=width_of_columns["signature"], h=5, txt="Signature of\nemployee/\nRemarks", align='C', border=1)
            self.set_xy(x=position_before_drawing_box_for_paycode["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"]+width_of_columns["net_payable"]+width_of_columns["signature"], y=position_before_drawing_box_for_paycode["y"])

            self.set_xy(x=position_before_drawing_box_for_paycode["x"], y=position_before_drawing_box_for_paycode["y"]+15)


def generate_salary_sheet(user, request_data, prepared_salaries):
    print(f"Salary Sheet User: {user.id}")
    global default_cell_height
    global default_number_of_cells_in_row
    default_cell_height = 5


    earnings_grand_total_dict = {}
    generative_leaves = LeaveGrade.objects.filter(company_id=request_data['company'], generate_frequency__isnull=False)
    earnings_head = EarningsHead.objects.filter(company_id=request_data['company']).order_by("id")
    for head in earnings_head:
        earnings_grand_total_dict[head.id] = {"name":head.name, "amount": 0, "arrear_amount": 0}

    default_number_of_cells_in_row = max(len(generative_leaves)+2, 8, len(earnings_head)+1)
    company_details = CompanyDetails.objects.filter(company=generative_leaves[0].company.id)
    salary_sheet_pdf = FPDF(my_date=date(request_data['year'], request_data['month'], 1),company_name=generative_leaves[0].company.name,company_address=company_details.first().address if company_details.exists() else '', orientation="L", unit="mm", format="A4")
    salary_sheet_pdf.set_margins(left=6, top=4, right=6)

    salary_sheet_pdf.set_font('Arial', '', 8)
    salary_sheet_pdf.add_page()

    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.set_auto_page_break(auto=True, margin = 8)
    grand_total_ot_incentive = {
        "ot_amount": 0,
        "incentive": 0
    }


    initial_cursor_position_before_row = {"x": salary_sheet_pdf.get_x(), "y": salary_sheet_pdf.get_y()}
    header_height = initial_cursor_position_before_row["y"]
    rows_per_page = min(((salary_sheet_pdf.h-header_height-8)/(default_number_of_cells_in_row*default_cell_height)), 4) #8 represents the botton marging


    group_by_filter_heading_height = 6


    if request_data['filters']['group_by'] != 'none':
        print(f"Y: {salary_sheet_pdf.get_y()} In goupby cell height {(salary_sheet_pdf.h-header_height-8-((rows_per_page//1)*group_by_filter_heading_height))/((default_number_of_cells_in_row*(rows_per_page//1))+(rows_per_page//1))}")
        default_cell_height = (salary_sheet_pdf.h-header_height-8-((rows_per_page//1)*group_by_filter_heading_height))/((default_number_of_cells_in_row*(rows_per_page//1))+(rows_per_page//1))
        default_cell_height = math.floor(default_cell_height * 10) / 10

        print(default_cell_height)
    group_by_filter_total_height = default_cell_height


    company_pf_esi_setup = PfEsiSetup.objects.get(company=request_data['company'])
    grand_total_deductions = {
        "pf": 0,
        "esi": 0,
        "vpf": 0,
        "advance": 0,
        "tds": 0
    }
    grand_total_net_payable = 0
    if company_pf_esi_setup.enable_labour_welfare_fund:
        grand_total_deductions["lwf"] = 0
    grand_total_earnings_including_ot_arrear = 0
    grand_total_epf_esic_dict = {
        "pf_employees_number": 0,
        "pf_wages_total": 0,
        "esi_employees_number": 0,
        "esi_wages_total": 0,
    }

    department_grand_total = {}

    employee_department_list = []
    for index, salary in enumerate(prepared_salaries):
        employee_professional_details = EmployeeProfessionalDetail.objects.get(employee=salary.employee.id)
        employee_pf_esi_details = EmployeePfEsiDetail.objects.get(employee=salary.employee.id)
        employee_salary_details = EmployeeSalaryDetail.objects.get(employee=salary.employee.id)
        employee_monthly_attendance_details = EmployeeMonthlyAttendanceDetails.objects.get(user=user, employee=salary.employee.id, date=salary.date)
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(from_date__lte=salary.date, to_date__gte=salary.date, employee=salary.employee.id).order_by('earnings_head__id')
        earned_amounts = EarnedAmount.objects.filter(user=user, salary_prepared = salary.id).order_by('earnings_head__id')
        basic_earned = earned_amounts.filter(earnings_head__name="Basic").first()

        #For Department Name Header and Total if the group_by is not none
        if request_data['filters']['group_by'] == 'department':
            employee_department = employee_professional_details.department
            if employee_department:
                employee_department_list.append(employee_department.name)
                if index == 0:
                    salary_sheet_pdf.set_font('Arial', 'BU', 10)
                    salary_sheet_pdf.cell(0, group_by_filter_heading_height, employee_department.name, align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    salary_sheet_pdf.set_font('Arial', 'B', 8)
                    department_totals = {
                        'salary_wage_rate_total': 0,
                        'earnings_total': 0, 
                        'arrears_total': 0,
                        'ot_incentive_total': 0,
                        'total_earnings_total': 0,
                        'deductions_total': 0,
                        'net_payable_total': 0,
                    }
                    department_grand_total[employee_department.name] = department_totals
                    initial_cursor_position_before_row['y'] = initial_cursor_position_before_row['y'] + group_by_filter_heading_height
                elif (index>0 and employee_department.name != employee_department_list[index-1]):
                    #Print Total of previous department
                    salary_sheet_pdf.set_font('Arial', 'BU', 10)
                    # salary_sheet_pdf.cell(0, group_by_filter_total_height, f"{employee_department_list[index-1]} END", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    salary_sheet_pdf.cell(0, group_by_filter_heading_height, employee_department.name, align="L", new_x="LMARGIN", new_y='NEXT', border=0)
                    salary_sheet_pdf.set_font('Arial', 'B', 8)
                    department_totals = {
                        'salary_wage_rate_total': 0,
                        'earnings_total': 0, 
                        'arrears_total': 0,
                        'ot_incentive_total': 0,
                        'total_earnings_total': 0,
                        'deductions_total': 0,
                        'net_payable_total': 0,
                    }
                    department_grand_total[employee_department.name] = department_totals

                    initial_cursor_position_before_row['y'] = initial_cursor_position_before_row['y'] + (group_by_filter_heading_height)


        # if index!=0:
        #     employee_department = employee_professional_details.department
            # if employee_department:
                # print(f"Employee Name: {salary.employee.name}  Dept Name: {employee_department.name}")
        if employee_pf_esi_details.pf_limit_ignore_employee == False and employee_pf_esi_details.pf_allow == True:
            grand_total_epf_esic_dict['pf_wages_total'] += min(company_pf_esi_setup.ac_1_epf_employee_limit, basic_earned.earned_amount+basic_earned.arear_amount)
            grand_total_epf_esic_dict['pf_employees_number'] += 1
        elif employee_pf_esi_details.pf_limit_ignore_employee == True and employee_pf_esi_details.pf_allow == True:
            if employee_pf_esi_details.pf_limit_ignore_employee_value != None:
                current_employee_pf_limit = employee_pf_esi_details.pf_limit_ignore_employee_value
                grand_total_epf_esic_dict['pf_wages_total'] += min(current_employee_pf_limit, basic_earned.earned_amount+basic_earned.arear_amount)
                grand_total_epf_esic_dict['pf_employees_number'] += 1
            else:
                grand_total_epf_esic_dict['pf_wages_total'] += basic_earned.earned_amount+basic_earned.arear_amount
                grand_total_epf_esic_dict['pf_employees_number'] += 1


        for column_name, column_width in width_of_columns.items():

            #Add the Paycode part of Row
            if column_name == "paycode":
                employee_pay_code = salary.employee.paycode #Get actual paycode from db and replace this
                sn = index+1
                doj = employee_professional_details.date_of_joining.strftime("%d-%b-%Y") #Get actual doj from db and replace this
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height*default_number_of_cells_in_row/3, txt=f"{employee_pay_code}\n{sn}\n{doj}", align='C', border=1)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"], y=initial_cursor_position_before_row["y"])


            if column_name == "employee_name":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                employee_name = salary.employee.name #Get actual employee name from db and replace this
                employee_father_husband_name = salary.employee.father_or_husband_name or "" #If exists then get from db and replace this else in null set as empty string
                designation = employee_professional_details.designation.name if employee_professional_details.designation and hasattr(employee_professional_details.designation, 'name') else ""
                department = employee_professional_details.department.name if employee_professional_details.department and hasattr(employee_professional_details.department, 'name') else ""
                pf_number = employee_pf_esi_details.pf_number or ""
                uan_number = employee_pf_esi_details.uan_number or ""
                esi_number = employee_pf_esi_details.esi_number or ""
                bank_account_number = employee_salary_details.account_number or "" #Display this only if the payment mode is bank
                row_text = f"{employee_father_husband_name}\n{designation}\n{department}\nPF No. : {pf_number}\nUAN No. : {uan_number}\nESI No. : {esi_number}\nBank : {bank_account_number}"

                #Printing Employee Name with bold
                salary_sheet_pdf.set_font('Arial', 'B', 8)
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{employee_name}\n", align='L', border=0)
                salary_sheet_pdf.set_font('Arial', '', 8)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"], y=initial_cursor_position_before_row["y"]+default_cell_height)



                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=row_text, align='L', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"], y=initial_cursor_position_before_row["y"])

            
            if column_name == "attendance_detail":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["attendance_detail"], h=default_cell_height*default_number_of_cells_in_row)
                employee_generative_leaves = EmployeeGenerativeLeaveRecord.objects.filter(user=user, employee=salary.employee.id, date=salary.date).order_by('leave__name')
                # generative_leaves = [{"name": "EL", "amount":4}, {"name":"CL", "amount":2}, {"name":"SL", "amount":1}] #Get actual data from db and replace this                
                generative_leave_text = "\n".join(f"{leave.leave.name} : {int(leave.leave_count/2) if leave.leave_count/2%1==0 else leave.leave_count/2}" for leave in employee_generative_leaves)
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=generative_leave_text, align='L', border=0)

                #Draw another multicell for non generative leaves which are permament in every company
                #Get EmployeeMonthlyAttendanceDetails model data and plug them here

                working_days = employee_monthly_attendance_details.present_count/2
                weekly_off = employee_monthly_attendance_details.weekly_off_days_count/2
                holiday_off = employee_monthly_attendance_details.holiday_days_count/2
                #Store compensation off in monthly attendance details and ask if it is actually compensaton off
                absent_days = employee_monthly_attendance_details.not_paid_days_count/2
                paid_days_count = employee_monthly_attendance_details.paid_days_count/2
                compensation_off_days_count = employee_monthly_attendance_details.compensation_off_days_count/2

                # Format the numbers to show the decimal part only if it exists
                working_days_str = f"{working_days:.1f}" if working_days % 1 != 0 else str(int(working_days))
                weekly_off_str = f"{weekly_off:.1f}" if weekly_off % 1 != 0 else str(int(weekly_off))
                holiday_off_str = f"{holiday_off:.1f}" if holiday_off % 1 != 0 else str(int(holiday_off))
                absent_days_str = f"{absent_days:.1f}" if absent_days % 1 != 0 else str(int(absent_days))
                paid_days_str = f"{paid_days_count:.1f}" if paid_days_count % 1 != 0 else str(int(paid_days_count))
                compensation_off_days_str = f"{compensation_off_days_count:.1f}" if compensation_off_days_count % 1 != 0 else str(int(compensation_off_days_count))

                # Then use the formatted strings in your multi_cell
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+(width_of_columns["attendance_detail"]/2), y=initial_cursor_position_before_row["y"])
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=f"WD : {working_days_str}\nWO : {weekly_off_str}\nHD : {holiday_off_str}\nCO : {compensation_off_days_str}\nA    : {absent_days_str}", align='J', border=0)
                # salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+(width_of_columns["attendance_detail"]/2), y=initial_cursor_position_before_row["y"])
                # salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=f"WD : {working_days}\nWO : {weekly_off}\nHD : {holiday_off}\nCO: 1\nA   : {absent_days}", align='J', border=0)

                #Total of attendances
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)

                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"Paid Days : {paid_days_str}\n", align='J', border=0)
                salary_sheet_pdf.set_line_width(0.3)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"], y=initial_cursor_position_before_row["y"])

            if column_name == "salary_wage_rate":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["salary_wage_rate"], h=default_cell_height*default_number_of_cells_in_row)
                
                total_earnings_rate = 0
                earnings_rate_text = ""
                earnings_head_names_text = ""
                for salary_rate in employee_salary_rates:
                    total_earnings_rate += salary_rate.value
                    earnings_rate_text += f"{salary_rate.value}\n"
                    truncated_name = salary_rate.earnings_head.name[:max_name_earning_head_name_length]
                    earnings_head_names_text += f"{truncated_name}\n"

                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['salary_wage_rate_total'] += total_earnings_rate

                #Printing earnings head names
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=earnings_head_names_text, align='L', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)

                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=f"Total\n", align='L', border=0)
                

                #Printing the salary rates and the total salary
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+(width_of_columns["salary_wage_rate"]/2), y=initial_cursor_position_before_row["y"])
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=earnings_rate_text, align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+(width_of_columns["salary_wage_rate"]/2), y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=f"{total_earnings_rate}\n", align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"], y=initial_cursor_position_before_row["y"])
                

            if column_name == "earnings":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)

                total_earnings_amount = 0
                earned_amounts_text = ""
                for earned in earned_amounts:
                    total_earnings_amount += (earned.earned_amount-earned.arear_amount)
                    earned_amounts_text += f"{earned.earned_amount-earned.arear_amount}\n"
                    earnings_grand_total_dict[earned.earnings_head.id]["amount"] += earned.earned_amount
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=earned_amounts_text, align='R', border=0)

                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['earnings_total'] += total_earnings_amount

                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{total_earnings_amount}\n", align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=initial_cursor_position_before_row["y"])

            if column_name == "arrears":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)

                total_arrear_amount = 0
                arrear_amounts_text = ""
                for earned in earned_amounts:
                    total_arrear_amount += earned.arear_amount
                    arrear_amounts_text += f"{earned.arear_amount}\n"
                    earnings_grand_total_dict[earned.earnings_head.id]['arrear_amount']+=earned.arear_amount
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=arrear_amounts_text, align='R', border=0)

                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['arrears_total'] += total_arrear_amount

                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)

                #For epf and esic summary
                if employee_pf_esi_details.esi_allow == True:
                    if employee_pf_esi_details.esi_on_ot == True:
                        grand_total_epf_esic_dict["esi_wages_total"] += salary.net_ot_amount_monthly
                    grand_total_epf_esic_dict["esi_wages_total"] += min(total_earnings_amount+total_arrear_amount, company_pf_esi_setup.esi_employee_limit)
                    grand_total_epf_esic_dict["esi_employees_number"] += 1

                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{total_arrear_amount}\n", align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"], y=initial_cursor_position_before_row["y"])


            if column_name == "ot_incentive":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                salary_sheet_pdf.multi_cell(w=column_width/2, h=(default_cell_height*default_number_of_cells_in_row)/3, txt=f"O.T Hrs\nO.T Amt\nIncentive", align='L', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+(width_of_columns["ot_incentive"]/2), y=initial_cursor_position_before_row["y"])
                salary_sheet_pdf.multi_cell(w=column_width/2, h=(default_cell_height*default_number_of_cells_in_row)/3, txt=f"{salary.net_ot_minutes_monthly/60}\n{salary.net_ot_amount_monthly}\n{salary.incentive_amount}", align='R', border=0)
                grand_total_ot_incentive["ot_amount"] += salary.net_ot_amount_monthly
                grand_total_ot_incentive["incentive"] += salary.incentive_amount
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"], y=initial_cursor_position_before_row["y"])
                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['ot_incentive_total'] += salary.net_ot_amount_monthly


            if column_name == "total_earnings":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                salary_sheet_pdf.set_xy(x=salary_sheet_pdf.get_x(), y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)
                total_earnings_including_ot_arrrear = total_earnings_amount+total_arrear_amount+salary.net_ot_amount_monthly+salary.incentive_amount
                grand_total_earnings_including_ot_arrear += total_earnings_including_ot_arrrear
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{total_earnings_including_ot_arrrear}", align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"], y=initial_cursor_position_before_row["y"])
                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['total_earnings_total'] += total_earnings_including_ot_arrrear


            if column_name == "deductions":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                deductions_name_text = f"PF\nESI\nVPF\nAdvance\nTDS"
                deductions_amount_text = f"{salary.pf_deducted}\n{salary.esi_deducted}\n{salary.vpf_deducted}\n{salary.advance_deducted}\n{salary.tds_deducted}"
                if company_pf_esi_setup.enable_labour_welfare_fund:
                    deductions_name_text += "\nLWF"
                    deductions_amount_text += f"\n{salary.labour_welfare_fund_deducted}"
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=deductions_name_text, align='L', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+(width_of_columns["deductions"]/2), y=initial_cursor_position_before_row["y"])
                salary_sheet_pdf.multi_cell(w=column_width/2, h=default_cell_height, txt=deductions_amount_text, align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)

                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)

                #Total amount Deducted
                total_deductions = salary.pf_deducted+salary.esi_deducted+salary.vpf_deducted+salary.advance_deducted+salary.tds_deducted
                grand_total_deductions["pf"] += salary.pf_deducted
                grand_total_deductions["esi"] += salary.esi_deducted
                grand_total_deductions["vpf"] += salary.vpf_deducted
                grand_total_deductions["advance"] += salary.advance_deducted
                grand_total_deductions["tds"] += salary.tds_deducted
                if company_pf_esi_setup.enable_labour_welfare_fund:
                    total_deductions += salary.labour_welfare_fund_deducted
                    grand_total_deductions["lwf"] += salary.labour_welfare_fund_deducted
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{total_deductions}", align='R', border=0)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"], y=initial_cursor_position_before_row["y"])
                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['deductions_total'] += total_deductions




            if column_name == "net_payable":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"], y=initial_cursor_position_before_row["y"]+(default_number_of_cells_in_row-1)*default_cell_height)
                #Dasehd Line
                salary_sheet_pdf.set_line_width(0.1)
                salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), salary_sheet_pdf.get_x()+column_width, salary_sheet_pdf.get_y(), dash_length = 1, space_length = 1)
                salary_sheet_pdf.set_line_width(0.3)
                net_payable = (total_earnings_amount+total_arrear_amount+salary.net_ot_amount_monthly+salary.incentive_amount) - total_deductions
                grand_total_net_payable += net_payable
                salary_sheet_pdf.set_font('Arial', 'B', 8)
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{net_payable}", align='R', border=0)
                salary_sheet_pdf.set_font('Arial', '', 8)
                salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"]+width_of_columns["net_payable"], y=initial_cursor_position_before_row["y"])
                if request_data['filters']['group_by'] != 'none':
                    if employee_department:
                        department_grand_total[employee_department.name]['net_payable_total'] += net_payable


            if column_name == "signature":
                salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=column_width, h=default_cell_height*default_number_of_cells_in_row)
                salary_sheet_pdf.multi_cell(w=column_width, h=default_cell_height, txt=f"{employee_salary_details.get_payment_mode_display()}", align='C', border=0)

                if ((index+1) % (rows_per_page//1)) == 0:
                    if request_data['filters']['group_by'] == 'department':
                        if index<(len(prepared_salaries)):
                                next_employee_department = None
                                if index<(len(prepared_salaries)-1):
                                    next_employee_professional_details = EmployeeProfessionalDetail.objects.get(employee=prepared_salaries[index+1].employee.id)
                                    next_employee_department = next_employee_professional_details.department
                                if (not next_employee_department or (employee_professional_details.department and employee_professional_details.department.name != next_employee_department.name)) and employee_professional_details.department:
                                    salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"], y=salary_sheet_pdf.get_y()+((default_number_of_cells_in_row-1)*default_cell_height))

                                    #Printing Department Totals
                                    salary_sheet_pdf.set_font('Arial', 'B', 8)
                                    salary_sheet_pdf.cell(width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns['attendance_detail'], group_by_filter_total_height, f"{employee_department_list[-1]} Total", align="L", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['salary_wage_rate'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['salary_wage_rate_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['earnings'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['earnings_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['arrears'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['arrears_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['ot_incentive'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['ot_incentive_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['total_earnings'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['total_earnings_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['deductions'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['deductions_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['net_payable'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['net_payable_total']}", align="R", border=0)
                                    salary_sheet_pdf.set_font('Arial', '', 8)


                    salary_sheet_pdf.add_page()
                    initial_cursor_position_before_row["y"] = header_height
                    salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"], y=initial_cursor_position_before_row["y"])
                else:
                    #Did default_number_of_cells_in_row-1 because signature column only utilizes one row
                    initial_cursor_position_before_row["y"] = salary_sheet_pdf.get_y()+((default_number_of_cells_in_row-1)*default_cell_height)

                    salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"], y=initial_cursor_position_before_row["y"])
                    if request_data['filters']['group_by'] == 'department':
                        if index<(len(prepared_salaries)):
                                next_employee_department = None
                                if index<(len(prepared_salaries)-1):
                                    next_employee_professional_details = EmployeeProfessionalDetail.objects.get(employee=prepared_salaries[index+1].employee.id)
                                    next_employee_department = next_employee_professional_details.department
                                if (not next_employee_department or (employee_professional_details.department and employee_professional_details.department.name != next_employee_department.name)) and employee_professional_details.department:
                                    #Printing Department Totals
                                    salary_sheet_pdf.set_font('Arial', 'B', 8)
                                    salary_sheet_pdf.cell(width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns['attendance_detail'], group_by_filter_total_height, f"{employee_department_list[-1]} Total", align="L", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['salary_wage_rate'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['salary_wage_rate_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['earnings'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['earnings_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['arrears'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['arrears_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['ot_incentive'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['ot_incentive_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['total_earnings'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['total_earnings_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['deductions'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['deductions_total']}", align="R", border=0)
                                    salary_sheet_pdf.cell(width_of_columns['net_payable'], group_by_filter_total_height, f"{department_grand_total[employee_professional_details.department.name]['net_payable_total']}", align="R", border=0)
                                    salary_sheet_pdf.set_font('Arial', '', 8)


                                    salary_sheet_pdf.set_xy(x=initial_cursor_position_before_row["x"], y=initial_cursor_position_before_row["y"]+group_by_filter_total_height)
                                    initial_cursor_position_before_row["y"] = initial_cursor_position_before_row["y"]+group_by_filter_total_height






    

    cursor_position_after_all_rows = {"x":salary_sheet_pdf.get_x(), "y":salary_sheet_pdf.get_y()}
    # Grand Total takes about 40mm of height that is 40 mm of Y


    if (salary_sheet_pdf.h-8)-cursor_position_after_all_rows['y']<40:
        salary_sheet_pdf.add_page()
        cursor_position_after_all_rows['y'] = header_height

    # Printing Grand Total
    salary_sheet_pdf.set_xy(x=salary_sheet_pdf.get_x(), y=salary_sheet_pdf.get_y()+default_cell_height)
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["paycode"], h=default_cell_height, txt=f"Grand Total", align='L', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    grand_total_number_of_cells = max(len(earnings_grand_total_dict.items()), len(grand_total_deductions.items()))
    #Setting Up Grand Total variables and texts
    grand_total_earnings_head_name_text = ""
    grand_total_earnings_head_amount_text = ""
    grand_total_earnings_head_amount = 0
    grand_total_arrear_text = ""
    grand_total_arrear_amount = 0
    for id, earnings_head_dict in earnings_grand_total_dict.items():
        grand_total_earnings_head_name_text += f"{earnings_head_dict['name'][:5]}\n"
        grand_total_earnings_head_amount_text +=f"{earnings_head_dict['amount']}\n"
        grand_total_earnings_head_amount += earnings_head_dict['amount']
        grand_total_arrear_text += f"{earnings_head_dict['arrear_amount']}\n"
        grand_total_arrear_amount += earnings_head_dict['arrear_amount']

    #Printing ESIC EPF Summary:
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["employee_name"]+width_of_columns["attendance_detail"], h=grand_total_number_of_cells*default_cell_height)
    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.cell(w=width_of_columns["employee_name"]+width_of_columns["attendance_detail"], h=default_cell_height, txt="EPF ESIC Summary", align='C', border=0, new_x="LEFT", new_y="NEXT")
    salary_sheet_pdf.set_font('Arial', '', 8)
    salary_sheet_pdf.multi_cell(w=(width_of_columns["employee_name"]+width_of_columns["attendance_detail"])/2, h=default_cell_height, txt="PF Employees No.\nPF Wages\nESI Employees No.\nESI Wages", align='L', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+(width_of_columns["employee_name"]+width_of_columns["attendance_detail"])/2, y=cursor_position_after_all_rows["y"]+default_cell_height*2)
    salary_sheet_pdf.multi_cell(w=(width_of_columns["employee_name"]+width_of_columns["attendance_detail"])/2, h=default_cell_height, txt=f"{grand_total_epf_esic_dict['pf_employees_number']}\n{grand_total_epf_esic_dict['pf_wages_total']}\n{grand_total_epf_esic_dict['esi_employees_number']}\n{grand_total_epf_esic_dict['esi_wages_total']}", align='R', border=0)





    #Printing Grand Total Earnings
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], h=grand_total_number_of_cells*default_cell_height)
    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.multi_cell(w=width_of_columns["salary_wage_rate"], h=default_cell_height, txt=grand_total_earnings_head_name_text, align='L', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.multi_cell(w=width_of_columns["earnings"], h=default_cell_height, txt=grand_total_earnings_head_amount_text, align='R', border=0)
    #Dasehd Line
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.dashed_line(salary_sheet_pdf.get_x(), cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)), salary_sheet_pdf.get_x()+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+width_of_columns["deductions"]+width_of_columns["net_payable"]+width_of_columns["signature"], cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)), dash_length = 1, space_length = 1)
    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"], y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["earnings"], h=default_cell_height, txt=f"{grand_total_earnings_head_amount}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    #Printing Grand Total Arrears
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["arrears"], h=grand_total_number_of_cells*default_cell_height)
    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.multi_cell(w=width_of_columns["arrears"], h=default_cell_height, txt=grand_total_arrear_text, align='R', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["earnings"], h=default_cell_height, txt=f"{grand_total_arrear_amount}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    #Printing Grand Total OT and incentive
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["ot_incentive"], h=grand_total_number_of_cells*default_cell_height)
    salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.multi_cell(w=width_of_columns["ot_incentive"]/2, h=((default_cell_height*grand_total_number_of_cells)/3), txt=f" \nO.T Amt\nIncentive", align='L', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+(width_of_columns["ot_incentive"]/2), y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.multi_cell(w=width_of_columns["ot_incentive"]/2, h=((default_cell_height*grand_total_number_of_cells)/3), txt=f" \n{grand_total_ot_incentive['ot_amount']}\n{grand_total_ot_incentive['incentive']}", align='R', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+(width_of_columns["ot_incentive"]/2), y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["ot_incentive"]/2, h=default_cell_height, txt=f"{grand_total_ot_incentive['incentive']+grand_total_ot_incentive['ot_amount']}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    #Printing Grand Total Earnings Including OT and Arrear
    # salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    # salary_sheet_pdf.set_line_width(0.1)
    # salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["total_earnings"], h=grand_total_number_of_cells*default_cell_height)
    # salary_sheet_pdf.set_line_width(0.3)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"], y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["total_earnings"], h=default_cell_height, txt=f"{grand_total_earnings_including_ot_arrear}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)


    #Printing Grand Total Deductions
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"], y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.set_line_width(0.1)
    salary_sheet_pdf.rect(salary_sheet_pdf.get_x(), salary_sheet_pdf.get_y(), w=width_of_columns["deductions"], h=grand_total_number_of_cells*default_cell_height)
    salary_sheet_pdf.set_line_width(0.3)
    grand_total_deductions_name_text = f"PF\nESI\nVPF\nAdvance\nTDS"
    grand_total_deductions_amount_text = f"{grand_total_deductions['pf']}\n{grand_total_deductions['esi']}\n{grand_total_deductions['vpf']}\n{grand_total_deductions['advance']}\n{grand_total_deductions['tds']}"
    grand_total_deductions_amount = grand_total_deductions['pf']+grand_total_deductions['esi']+grand_total_deductions['vpf']+grand_total_deductions['advance']+grand_total_deductions['tds']
    if company_pf_esi_setup.enable_labour_welfare_fund:
        grand_total_deductions_name_text += "\nLWF"
        grand_total_deductions_amount_text += f"\n{grand_total_deductions['lwf']}"
        grand_total_deductions_amount += grand_total_deductions['lwf']
    salary_sheet_pdf.multi_cell(w=width_of_columns["deductions"]/2, h=default_cell_height, txt=grand_total_deductions_name_text, align='L', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+(width_of_columns["deductions"]/2), y=cursor_position_after_all_rows["y"]+default_cell_height)
    salary_sheet_pdf.multi_cell(w=width_of_columns["deductions"]/2, h=default_cell_height, txt=grand_total_deductions_amount_text, align='R', border=0)
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+(width_of_columns["deductions"]/2), y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["deductions"]/2, h=default_cell_height, txt=f"{grand_total_deductions_amount}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    #Printing Grand Total Net Payable
    salary_sheet_pdf.set_xy(x=cursor_position_after_all_rows["x"]+width_of_columns["paycode"]+width_of_columns["employee_name"]+width_of_columns["attendance_detail"]+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns["arrears"]+width_of_columns["ot_incentive"]+width_of_columns["total_earnings"]+(width_of_columns["deductions"]), y=cursor_position_after_all_rows['y']+(default_cell_height*(grand_total_number_of_cells+1)))
    salary_sheet_pdf.set_font('Arial', 'B', 8)
    salary_sheet_pdf.multi_cell(w=width_of_columns["net_payable"], h=default_cell_height, txt=f"{grand_total_net_payable}", align='R', border=0)
    salary_sheet_pdf.set_font('Arial', '', 8)

    # Grand Total takes about 40mm of height that is 40 mm of Y




    


    

    # salary_sheet_pdf.cell(40, 10, 'Hello World!', border=1)

    # salary_sheet_pdf.output("salary_sheet.pdf")
    buffer = bytes(salary_sheet_pdf.output())
    yield buffer
        