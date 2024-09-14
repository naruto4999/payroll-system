from fpdf import FPDF
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeAttendance, EmployeeSalaryDetail, EmployeeSalaryEarning, EarnedAmount
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar
import os

# Get the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the relative path to the font file
noto_sans_dev_regular = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Regular.ttf')
noto_sans_dev_bold = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Bold.ttf')

class FPDF(FPDF):
        def __init__(self, company_name, company_address, default_cell_height, *args, **kwargs):
            # self.my_date = my_date
            self.company_name = company_name
            self.company_address = company_address
            self.default_cell_height = default_cell_height
            super().__init__(*args, **kwargs)

        def header(self):
            # Set Font for Company and add Company name
            self.set_font('noto-sans-devanagari', size=15, style="B")
            self.cell(0, 8, self.company_name, align="C", new_x="LMARGIN", new_y='NEXT', border=0)

            # Set Font for Address and add Address
            self.set_font('noto-sans-devanagari', size=9, style="B")
            self.cell(0, 5, self.company_address, align="C",  new_x="LMARGIN", new_y='NEXT', border=0)
            self.cell(w=210/2-6, h=5, text='Full And Final Report', align="R",  new_x="RIGHT", new_y='TOP', border=0)
            self.cell(w=210/2-7, h=5, text='/ पूर्ण एवं अंतिम भुगतान', align="L",  new_x="LMARGIN", new_y='NEXT', border=0)

        

# Create instance of FPDF class
def generate_full_and_final_report(user, request_data, employee):
    print('starting to create the attendance register')
    generative_leaves = LeaveGrade.objects.filter(company_id=request_data['company'], generate_frequency__isnull=False)
    default_cell_height = 5
    default_cell_height_large = 7
    left_margin = 6
    right_margin = 7
    top_margin = 6
    bottom_margin = 8
    minimum_salary_table_rows = 7

    max_name_earning_head_name_length = 6


    #Dimensions of A4 sheet is 210 x 297 mm and there is 6 mm margin on left and right leaving us with 285mm
    width_of_columns = {
        'intro_header': 20,
        'intro_value': 56,
        'intro_header_date': 25,
        'intro_value_date': 20,
        #Payment Related
        "salary_wage_rate": 32,
        "earnings": 16,
        "arrears": 16,
        "deductions": 55,
        "net_amount": 16,
        "prepared_by_column": 62
    }

    # default_number_of_cells_in_row = max(len(generative_leaves)+2, 8, len(earnings_head)+1)
    company_details = None
    try: company_details = CompanyDetails.objects.filter(company_id=request_data['company']).first()
    except: pass
    full_and_final_report = FPDF(company_name=company_details.company.name if company_details else '',company_address=company_details.address if company_details else '',default_cell_height=default_cell_height, orientation="P", unit="mm", format="A4")
    #Adding Hindi Font
    full_and_final_report.add_font("noto-sans-devanagari",fname=noto_sans_dev_regular)
    full_and_final_report.add_font("noto-sans-devanagari", fname=noto_sans_dev_bold, style="B")
    full_and_final_report.set_text_shaping(True)
    #Page settings
    full_and_final_report.set_margins(left=left_margin, top=top_margin, right=right_margin)
    full_and_final_report.add_page()
    full_and_final_report.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates_after_header = {"x": full_and_final_report.get_x(), "y": full_and_final_report.get_y()}


    full_and_final_report.set_font('noto-sans-devanagari', size=8, style="")
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height_large) #blank line

    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=210-left_margin-right_margin, h=default_cell_height_large*3)
    ##Employee Intro
    #Paycode
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"Paycode :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{employee.employee.paycode}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Card No
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"ACN :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{employee.employee.attendance_card_no}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #DOJ
    date_of_joining = None
    try: date_of_joining = employee.date_of_joining
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header_date'], h=default_cell_height_large, text=f"DOJ :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value_date'], h=default_cell_height_large, text=f"{date_of_joining.strftime('%d-%b-%Y') if date_of_joining else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

    #Name
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"Name :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{employee.employee.name}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Designation
    designation = None
    try: designation = employee.designation
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"Designation :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{designation.name if designation else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Resignation Date
    resignation_date = None
    try: resignation_date = employee.resignation_date
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header_date'], h=default_cell_height_large, text=f"Resignation Date :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value_date'], h=default_cell_height_large, text=f"{resignation_date.strftime('%d-%b-%Y') if resignation_date else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    
    #F/H NAme
    father_or_husband_name = None
    try: father_or_husband_name = employee.employee.father_or_husband_name
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"F/H Name :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{father_or_husband_name if father_or_husband_name else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)

    #Department
    department = None
    try: department = employee.department
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header'], h=default_cell_height_large, text=f"Department :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value'], h=default_cell_height_large, text=f"{department.name if department else ''}", align="L", new_x="RIGHT", new_y='TOP', border=0)
    
    #Full And Final Date
    full_and_final_date = None
    try: full_and_final_date = employee.employee.full_and_final.filter(user=user).first().full_and_final_date
    except: pass
    full_and_final_report.cell(w=width_of_columns['intro_header_date'], h=default_cell_height_large, text=f"Full & Final Date :", align="L", new_x="RIGHT", new_y='TOP', border=0)
    full_and_final_report.cell(w=width_of_columns['intro_value_date'], h=default_cell_height_large, text=f"{full_and_final_date.strftime('%d-%b-%Y') if full_and_final_date else ''}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
    coordinates_before_any_table = {"x": full_and_final_report.get_x(), "y": full_and_final_report.get_y()}


    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height*5) #blank line
    ##Earnings Table
    full_and_final_report.set_font('noto-sans-devanagari', size=8, style="B")
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['arrears']+width_of_columns['earnings'], h=default_cell_height, text=f"Earnings", align="C", new_x="RIGHT", new_y='TOP', border=1)
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height*2, text=f"Deductions", align="C", new_x="RIGHT", new_y='TOP', border=1)
    full_and_final_report.cell(w=width_of_columns['net_amount'], h=default_cell_height*2, text=f"Net Amt.", align="C", new_x="LMARGIN", new_y='NEXT', border=1)

    # Salary Wage Rate
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()-default_cell_height)
    employee_salary_rates = EmployeeSalaryEarning.objects.filter(from_date__lte=resignation_date.replace(day=1), to_date__gte=resignation_date.replace(day=1), employee=employee.employee).order_by('earnings_head__id')
    
    coordinates_before_table = {"x": full_and_final_report.get_x(), "y": full_and_final_report.get_y()}

    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate'], h=default_cell_height, text=f"Salary/Wage Rate", new_x="LMARGIN", new_y="NEXT",align='C', border=1)
    
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns["salary_wage_rate"], h=(default_cell_height)*minimum_salary_table_rows)
    full_and_final_report.set_font('noto-sans-devanagari', size=7)
    total_earnings_rate = 0
    for index, salary_rate in enumerate(employee_salary_rates):
        full_and_final_report.set_xy(x=coordinates_before_table['x'], y=full_and_final_report.get_y())
        full_and_final_report.cell(w=width_of_columns['salary_wage_rate'], h=default_cell_height, text=f'{salary_rate.earnings_head.name[:max_name_earning_head_name_length]}', align='L', new_x="LEFT", new_y='TOP')
        full_and_final_report.cell(w=width_of_columns['salary_wage_rate'], h=default_cell_height, text=f'{salary_rate.value}', align='R', new_x="LEFT", new_y='NEXT')
        total_earnings_rate += salary_rate.value
    
    #Printing Blank lines if the earnings heads are less than min table rows
    if len(employee_salary_rates)<minimum_salary_table_rows:
        for blank_index in range(minimum_salary_table_rows-len(employee_salary_rates)):
            full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height) #blank line

    # Printing Total
    full_and_final_report.set_xy(x=coordinates_before_table['x'], y=full_and_final_report.get_y())
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate'], h=default_cell_height, text=f"Total", new_x="LMARGIN", new_y="TOP",align='L', border=0)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate'], h=default_cell_height, text=f"{total_earnings_rate}", new_x="LMARGIN", new_y="NEXT",align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    #Earnings
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate'], y=coordinates_before_table["y"])
    full_and_final_report.cell(w=width_of_columns['earnings'], h=default_cell_height, text=f"Earnings", new_x="LEFT", new_y="NEXT", align='C', border=1)

    salary_prepared_resign_month = employee.employee.salaries_prepared.filter(user=user, date=resignation_date.replace(day=1)).first()
    earned_amounts = EarnedAmount.objects.filter(salary_prepared = salary_prepared_resign_month.id).order_by('earnings_head__id')
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns["earnings"], h=(default_cell_height)*minimum_salary_table_rows)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')
    total_earned_amount = 0
    for index, earned in enumerate(earned_amounts):
        full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate'], y=full_and_final_report.get_y())
        full_and_final_report.cell(w=width_of_columns['earnings'], h=default_cell_height, text=f'{earned.earned_amount-earned.arear_amount}', new_x="LEFT", new_y='NEXT', align='R')
        total_earned_amount += earned.earned_amount-earned.arear_amount
        print(earned.earned_amount-earned.arear_amount)

    #Printing Blank lines if the earned amounts are less than min table rows
    if len(earned_amounts)<minimum_salary_table_rows:
        for blank_index in range(minimum_salary_table_rows-len(earned_amounts)):
            full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height) #blank line

    
    # Printing Total
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate'], y=full_and_final_report.get_y())
    full_and_final_report.cell(w=width_of_columns['earnings'], h=default_cell_height, text=f"{total_earned_amount}", new_x="LMARGIN", new_y="NEXT",align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    #Arrears
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate']+width_of_columns['earnings'], y=coordinates_before_table["y"])
    full_and_final_report.cell(w=width_of_columns['arrears'], h=default_cell_height, text=f"Arrears", new_x="LEFT", new_y="NEXT", align='C', border=1)

    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns["earnings"], h=(default_cell_height)*minimum_salary_table_rows)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')
    total_arrears_amount = 0
    for index, earned in enumerate(earned_amounts):
        full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate']+width_of_columns["earnings"], y=full_and_final_report.get_y())
        full_and_final_report.cell(w=width_of_columns['arrears'], h=default_cell_height, text=f'{earned.arear_amount}', new_x="LEFT", new_y='NEXT', align='R')
        total_arrears_amount += earned.arear_amount
        print(earned.arear_amount)

    #Printing Blank lines if the earned amounts are less than min table rows
    if len(earned_amounts)<minimum_salary_table_rows:
        for blank_index in range(minimum_salary_table_rows-len(earned_amounts)):
            full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height) #blank line

    
    # Printing Total
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate']+width_of_columns['earnings'], y=full_and_final_report.get_y())
    full_and_final_report.cell(w=width_of_columns['arrears'], h=default_cell_height, text=f"{total_arrears_amount}", new_x="LMARGIN", new_y="NEXT",align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    ##Deductions Table
    full_and_final_report.set_xy(x=coordinates_before_table['x']+width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], y=coordinates_before_table['y'] + default_cell_height)
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns["deductions"], h=default_cell_height*7)

    full_and_final_report.set_font('noto-sans-devanagari', size=7)
    total_deductions = 0
    
    #PF
    # payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*2))
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'PF', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.pf_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.pf_deducted
    
    #ESI
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'ESI', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.esi_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.esi_deducted

    #VPF
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'VPF', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.vpf_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.vpf_deducted

    #Advance
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'Advance', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.advance_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.advance_deducted
    
    #TDS
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'TDS', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.tds_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.tds_deducted

    #Others
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'Other', new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{salary_prepared_resign_month.others_deducted}', new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.others_deducted

    #LWF
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f"{'LWF' if salary_prepared_resign_month.company.pf_esi_setup_details.enable_labour_welfare_fund else ''}", new_x="LEFT", new_y='TOP', align='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f"{salary_prepared_resign_month.labour_welfare_fund_deducted if salary_prepared_resign_month.company.pf_esi_setup_details.enable_labour_welfare_fund else ''}", new_x="LEFT", new_y='NEXT', align='R')
    total_deductions += salary_prepared_resign_month.labour_welfare_fund_deducted

    #Printing Total
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f"{total_deductions}", new_x="RIGHT", new_y="TOP",align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    ##Net Amount
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=coordinates_before_table['y'] + default_cell_height)
    full_and_final_report.cell(w=width_of_columns['net_amount'], h=default_cell_height*7, text=f'', new_x="LEFT", new_y='NEXT', align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['net_amount'], h=default_cell_height, text=f'{total_earned_amount+total_arrears_amount-total_deductions}', new_x="LEFT", new_y='NEXT', align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')


    coordinates_before_full_and_final_table = {"x": full_and_final_report.get_x(), "y": full_and_final_report.get_y()}
    employee_full_and_final = employee.employee.full_and_final.filter(user=user).first()
    ##Earnings in full and final
    full_and_final_earnings = 0
    full_and_final_report.set_xy(x=coordinates_before_table['x'], y=full_and_final_report.get_y())
    
    #EL Encashment
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{int(employee_full_and_final.el_encashment_days/2) if (employee_full_and_final.el_encashment_days/2)%1==0 else employee_full_and_final.el_encashment_days/2} No. of EL Encashed', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.el_encashment_amount}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.el_encashment_amount
    
    #Previous Bonus
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Bonus {resignation_date.year-2}-{resignation_date.year-1}', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.bonus_prev_year}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.bonus_prev_year
    
    #Current Bonus
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Bonus {resignation_date.year-1}-{resignation_date.year}', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.bonus_current_year}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.bonus_current_year
    
    #Gratuity
    gratuity_duration_text = '0 years'
    duration_worked = relativedelta(employee.resignation_date, employee.date_of_joining)
    if duration_worked.years==4 and duration_worked.months>=6:
        gratuity_duration_text = '5 years'
    elif duration_worked.years>4:
        gratuity_duration_text = f"{duration_worked.years} Years and {duration_worked.months} Months"
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Gratuity for {gratuity_duration_text}', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.gratuity}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.gratuity

    #Service Compensation
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Service Compensation for {employee_full_and_final.service_compensation_days} Days', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.service_compensation_amount}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.service_compensation_amount

    #Notice Pay
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Notice Period Pay for {employee_full_and_final.earnings_notice_period_days} Days', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.earnings_notice_period_amount}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.earnings_notice_period_amount

    #Over Time
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Over Time for {employee_full_and_final.ot_min/60} Hrs', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.ot_amount}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_earnings += employee_full_and_final.ot_amount

    #Others
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Others', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{employee_full_and_final.earnings_others}', new_x="LEFT", new_y='NEXT', align='R', border='RB')
    full_and_final_earnings += employee_full_and_final.earnings_others

    #Grand Total Earnings
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'Grand Total', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], h=default_cell_height, text=f'{full_and_final_earnings+total_earned_amount+total_arrears_amount}', new_x="RIGHT", new_y='NEXT', align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    ##Deductions in Full and Final
    full_and_final_deductions = 0
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=coordinates_before_full_and_final_table['y'])
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns['deductions'], h=default_cell_height*8)

    #Notice Pay Deduction
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'Notice Period Ded. for {employee_full_and_final.deductions_notice_period_days} Days', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{employee_full_and_final.deductions_notice_period_amount}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_deductions += employee_full_and_final.deductions_notice_period_amount
    
    #Other Deduction
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'Others', new_x="LEFT", new_y='TOP', align='L', border='L')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{employee_full_and_final.deductions_others}', new_x="LEFT", new_y='NEXT', align='R', border='R')
    full_and_final_deductions += employee_full_and_final.deductions_others

    #Grand Total Deductions
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=coordinates_before_full_and_final_table['y']+default_cell_height*8)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.cell(w=width_of_columns['deductions'], h=default_cell_height, text=f'{total_deductions+full_and_final_deductions}', new_x="RIGHT", new_y='TOP', align='R', border=1)
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    ##Net Grand Total
    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='B')
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=coordinates_before_full_and_final_table['y'], w=width_of_columns['net_amount'], h=default_cell_height*8)
    full_and_final_report.cell(w=width_of_columns['net_amount'], h=default_cell_height, text=f'{(full_and_final_earnings+total_earned_amount+total_arrears_amount)-(total_deductions+full_and_final_deductions)}', new_x="RIGHT", new_y='TOP', align='R', border=1)
    coordinates_after_table = {"x": full_and_final_report.get_x(), "y": full_and_final_report.get_y()}

    full_and_final_report.set_font('noto-sans-devanagari', size=7, style='')

    ###Rest of the stuff not including the table
    full_and_final_report.set_font('noto-sans-devanagari', size=8, style='')
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=coordinates_before_any_table['y'])
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=width_of_columns['prepared_by_column'], h=default_cell_height*27)
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*2, text=f'Payment Mode:', new_x="LEFT", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*2, text=f'Date:', new_x="LEFT", new_y='NEXT', align='L', border=0)
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height*4) #blank line
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*4, text=f'Prepared By:', new_x="LEFT", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*4, text=f'Checked By:', new_x="LEFT", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*4, text=f'HR Manager:', new_x="LEFT", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=width_of_columns['prepared_by_column'], h=default_cell_height*4, text=f'Account Manager:', new_x="LMARGIN", new_y='NEXT', align='L', border=0)


    ##Declaration
    full_and_final_report.set_font('noto-sans-devanagari', size=12, style='B')
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height*8) #blank line
    full_and_final_report.rect(x=full_and_final_report.get_x(), y=full_and_final_report.get_y(), w=210-left_margin-right_margin, h=default_cell_height*8 + default_cell_height_large)
    full_and_final_report.cell(w=0, h=default_cell_height_large, text=f'Declaration / घोषणा', new_x="LMARGIN", new_y='NEXT', align='C', border=0)
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height) #blank line
    full_and_final_report.set_font('noto-sans-devanagari', size=8, style='')
    #Address
    text=''
    if employee.employee.local_address:
        text += employee.employee.local_address
    if employee.employee.local_district:
        if len(text) !=0:
            text += ', '
        text += employee.employee.local_district
    if employee.employee.local_state_or_union_territory:
        if len(text) !=0:
            text += ', '
        text += employee.employee.local_state_or_union_territory
    if employee.employee.local_pincode:
        if len(text) !=0:
            text += ', '
        text += employee.employee.local_pincode
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"मै  {employee.employee.name}  सुपुत्र / सुपुत्री / पत्नी  {employee.employee.father_or_husband_name or ''}  निवासी  {text}", new_x="LMARGIN", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"कुल रुपये  {(full_and_final_earnings+total_earned_amount+total_arrears_amount)-(total_deductions+full_and_final_deductions)} M/S  {employee.company.name}  से पूर्ण एवं अंतिम भुगतान के रूप में सधन्यवाद प्राप्त किये हैं |", new_x="LMARGIN", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"जिसमें मेरा आज तक का अर्जित वेतन, छुट्टियों का पैसा, आज तक का बोनस, नोटिस के बदले वेतन, ग्रेच्यूटी, सेवा काल का हर्जाना इत्यादि शामिल है | इस रकम की प्राप्ति के पश्चात अब कम्पनी की", new_x="LMARGIN", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"और मेरी किसी भी प्रकार की कोई बकाया राशि नहीं रह जाती है |", new_x="LMARGIN", new_y='NEXT', align='L', border=0)
    full_and_final_report.set_xy(x=full_and_final_report.get_x(), y=full_and_final_report.get_y()+default_cell_height) #blank line
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"मैंने अपना पूर्ण एवं अंतिम हिसाब ले लिया है | आज के बाद मेरा अपनी नौकरी पर भी कोई अधिकार नहीं रह जाता है | ", new_x="LMARGIN", new_y='NEXT', align='L', border=0)
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"दिनांक :  {full_and_final_date.strftime('%d-%b-%Y') if full_and_final_date else ''}", new_x="LMARGIN", new_y='TOP', align='L', border=0)
    full_and_final_report.cell(w=0, h=default_cell_height, text=f"हस्ताक्षर :  {employee.employee.name}", new_x="LMARGIN", new_y='NEXT', align='R', border=0)





    # Save the pdf with name .pdf
    buffer = bytes(full_and_final_report.output())
    yield buffer
