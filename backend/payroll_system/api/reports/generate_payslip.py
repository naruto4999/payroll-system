from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount
from datetime import date


# Get the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the relative path to the font file
noto_sans_dev_regular = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Regular.ttf')
noto_sans_dev_bold = os.path.join(script_dir, 'font', 'NotoSansDevanagari-Bold.ttf')

width_of_columns = {
        "attendance": 40,
        "salary_wage_rate": 46,
        "earnings": 16,
        "arrears": 16,
        "deductions": 38,
        "net_salary": 40,
        "form_x_center": 48,
        "top_left": 75,
        "top_right": 75
    }

class FPDF(FPDF):
    def footer(self):
        # Position at 1 cm from the bottom
        self.set_y(-10)
        # Set font
        self.set_font('noto-sans-devanagari', size=6)
        # Page number
        self.cell(0, 5, 'Page %s' % self.page_no(), 0, 0, 'R')

def generate_payslip(request_data, employee_salaries):
    intro_cell_height = 5
    company_details = CompanyDetails.objects.filter(company_id=request_data['company']).first()
    language = request_data['filters']['language']
    generative_leaves = LeaveGrade.objects.filter(company_id=request_data['company'], generate_frequency__isnull=False)
    default_number_of_cells_in_main_row = max(9, len(generative_leaves)+6)
    main_table_cell_height = 4
    max_name_earning_head_name_length = 10
    cell_height_for_dashed_line = 4.5
    rows_per_page = 3
    page_width = 210
    left_margin = 7
    right_margin = 7



    payslip = FPDF(unit="mm", format="A4")
    #Adding Hindi Font
    payslip.add_font("noto-sans-devanagari",fname=noto_sans_dev_regular)
    payslip.add_font("noto-sans-devanagari", fname=noto_sans_dev_bold, style="B")

    #Page settings
    payslip.set_margins(left=left_margin, top=4, right=right_margin)
    payslip.add_page()
    payslip.set_auto_page_break(auto=True, margin = 4)
    initial_coordinates_after_header = {"x": payslip.get_x(), "y": payslip.get_y()}
    payslip.set_text_shaping(True)


    # payslip.set_font('NotoSansDevanagari-Regular', size=14)

    # Add a cell
    for employee_index, salary in enumerate(employee_salaries):
        current_payslip_initial_coordinates = {"x": payslip.get_x(), "y": payslip.get_y()}
        #Draw Rect for this employee salary slip
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=page_width-left_margin-right_margin, h=intro_cell_height*8 + main_table_cell_height*(default_number_of_cells_in_main_row+1))

        payslip.set_font('noto-sans-devanagari', size=12, style="B")
        payslip.cell(w=0, h=intro_cell_height, text=f"{company_details.company.name}", align="C", new_x="LMARGIN", new_y="NEXT", border=0)
        payslip.set_font('noto-sans-devanagari', size=10, style="B")
        payslip.cell(w=0, h=intro_cell_height, text=f"{company_details.address}", align="C", new_x="LMARGIN", new_y="NEXT", border=0)
        
        #Drawing the Top Left Corner Details
        # payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns['top_left'], h=intro_cell_height*6)
        payslip.set_font('noto-sans-devanagari', size=7)
        payslip.multi_cell(w=width_of_columns['top_left'], h=intro_cell_height, text=f"Paycode{' / कोड न०' if language=='hindi' else ''}: {salary.employee.paycode}\nName{' / नाम' if language=='hindi' else''}: {salary.employee.name}",new_x="LMARGIN", new_y="NEXT", border=0)
        payslip.cell(w=None, h=intro_cell_height, text=f'Father/Husband{" /" if language=="hindi" else ""}', border=0)
        if language=='hindi':
            payslip.cell(w=None, h=intro_cell_height, text='पिता/पति')
        payslip.cell(w=None, h=intro_cell_height, text=f': {salary.employee.father_or_husband_name}', new_x="LMARGIN", new_y="NEXT", border=0)
        payslip.multi_cell(w=width_of_columns['top_left'], h=intro_cell_height, text=f"Desig{' / पद' if language=='hindi' else ''}: {salary.employee.employee_professional_detail.designation.name if salary.employee.employee_professional_detail.designation else ''}",new_x="LMARGIN", new_y="NEXT", border=0)
        #Department
        payslip.cell(w=None, h=intro_cell_height, text=f'Department{" /" if language=="hindi" else ""}', border=0)
        if language=='hindi':
            payslip.cell(w=None, h=intro_cell_height, text='विभाग')
        payslip.cell(w=None, h=intro_cell_height, text=f': {salary.employee.employee_professional_detail.department.name if salary.employee.employee_professional_detail.department else ""}', new_x="LMARGIN", new_y="NEXT", border=0)
        #DOJ
        payslip.cell(w=None, h=intro_cell_height, text=f'DOJ{" /" if language=="hindi" else ""}', border=0)
        if language=='hindi':
            payslip.cell(w=None, h=intro_cell_height, text='नियुक्त्ति तिथि')
        payslip.cell(w=None, h=intro_cell_height, text=f': {salary.employee.employee_professional_detail.date_of_joining.strftime("%d-%b-%Y")}', new_x="LMARGIN", new_y="NEXT", border=0)
        # Ask if attendance card number needs to be included ACN{' / ए.सी.एन' if language=='hindi' else ''}: {salary.employee.attendance_card_no}
        
        #Drawing the Middle small heading with Form X
        payslip.set_font('noto-sans-devanagari', size=10, style='B')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['top_left'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*3)
        payslip.cell(w=width_of_columns["form_x_center"], h=intro_cell_height, text="Form X", align='C', new_x="LEFT", new_y="NEXT", border=0)
        payslip.set_font('noto-sans-devanagari', size=8)
        payslip.cell(w=width_of_columns["form_x_center"], h=intro_cell_height, text="(Rule 26)", align='C', new_x="LEFT", new_y="NEXT", border=0)
        #Printing the month in 2 blocks
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["form_x_center"], h=intro_cell_height*2 if language=='hindi' else intro_cell_height)
        payslip.cell(w=width_of_columns["form_x_center"]*2/3, h=intro_cell_height, text=f"Payslip for the month", align='C', new_x="LEFT", new_y="NEXT", border=0)
        if language=='hindi':
            payslip.cell(w=width_of_columns["form_x_center"]*2/3, h=intro_cell_height, text=f"वेतन पर्ची माह", align='C', new_x="LEFT", new_y="NEXT", border=0)
        payslip.set_xy(x=current_payslip_initial_coordinates["x"]+width_of_columns['top_left']+width_of_columns["form_x_center"]*2/3, y=current_payslip_initial_coordinates["y"]+intro_cell_height*5)
        payslip.set_font('noto-sans-devanagari', size=8, style='B')
        payslip.cell(w=width_of_columns["form_x_center"]/3, h=intro_cell_height*2 if language=='hindi' else intro_cell_height, text=f"{date(request_data['year'], request_data['month'], 1).strftime('%b-%Y')}", align='C', new_x="LEFT", new_y="NEXT", border=0)
        
        #Drawing the Top Right Corner Details
        payslip.set_font('noto-sans-devanagari', size=7)
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['top_left']+width_of_columns['form_x_center'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*2)
        # payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["top_right"], h=intro_cell_height*6)
        payslip.cell(w=width_of_columns['top_right'], h=intro_cell_height, text=f'ACN{" / कार्ड न०" if language=="hindi" else ""}: {salary.employee.attendance_card_no}', new_x="LEFT", new_y="NEXT", border=0)
        payslip.cell(w=width_of_columns['top_right'], h=intro_cell_height, text=f'Bank A/C No.{" / बैंक खाता सं०" if language=="hindi" else ""}: {salary.employee.employee_salary_detail.account_number}', new_x="LEFT", new_y="NEXT", border=0)
        payslip.cell(w=width_of_columns['top_right'], h=intro_cell_height, text=f'PF No.{" / ई.पी.एफ" if language=="hindi" else ""}: {salary.employee.employee_pf_esi_detail.pf_number}', new_x="LEFT", new_y="NEXT", border=0)
        payslip.cell(w=width_of_columns['top_right'], h=intro_cell_height, text=f'UAN No.{" / यू.ए.एन" if language=="hindi" else ""}: {salary.employee.employee_pf_esi_detail.uan_number}', new_x="LEFT", new_y="NEXT", border=0)
        payslip.cell(w=width_of_columns['top_right'], h=intro_cell_height, text=f'ESI No.{" / ई.एस.आई" if language=="hindi" else ""}: {salary.employee.employee_pf_esi_detail.esi_number}', new_x="LEFT", new_y="NEXT", border=0)

        """
        Drawing the Main Salary Slip Table
        """
        #Attendance Details
        employee_monthly_details = salary.employee.monthly_attendance_details.filter(date=date(request_data['year'], request_data['month'], 1)).first()
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["attendance"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Attendance Details", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f"उपस्थिति विवरण", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        #Attendance Headings
        payslip.set_font('noto-sans-devanagari', size=7)
        #For WD
        payslip.cell(w=None, h=main_table_cell_height, text=f'WD{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'कार्य दिवस')
        #Value
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*2)
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(employee_monthly_details.present_count/2) if (employee_monthly_details.present_count/2)%1==0 else employee_monthly_details.present_count/2}', new_x="RIGHT", align='R')
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*3)
        #For WO
        payslip.cell(w=None, h=main_table_cell_height, text=f'WO{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'साप्ताहिक अवकाश')
        #Value
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*3)
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(employee_monthly_details.weekly_off_days_count/2) if (employee_monthly_details.weekly_off_days_count/2)%1==0 else employee_monthly_details.weekly_off_days_count/2}', new_x="RIGHT", align='R')
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*4)

        #For HD
        payslip.cell(w=None, h=main_table_cell_height, text=f'HD{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अवकाश')
        #Value
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*4)
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(employee_monthly_details.holiday_days_count/2) if (employee_monthly_details.holiday_days_count/2)%1==0 else employee_monthly_details.holiday_days_count/2}', new_x="RIGHT", align='R')
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*5)
        #For Absent
        payslip.cell(w=None, h=main_table_cell_height, text=f'A{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अनुपस्थिति')
        #Value
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*5)
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(employee_monthly_details.not_paid_days_count/2) if (employee_monthly_details.not_paid_days_count/2)%1==0 else employee_monthly_details.not_paid_days_count/2}', new_x="RIGHT", align='R')
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*6)
        #Generative Leaves
        employee_generative_leaves = EmployeeGenerativeLeaveRecord.objects.filter(employee=salary.employee, date=date(request_data['year'], request_data['month'], 1)).order_by('leave__name')
        for index, generative_leave in enumerate(employee_generative_leaves):
            payslip.cell(w=None, h=main_table_cell_height, text=f'{generative_leave.leave.name}{" /" if language=="hindi" and generative_leave.leave.name in ("EL", "CL", "SL") else ""}', new_x="RIGHT")
            if language=="hindi" and generative_leave.leave.name in ("EL", "CL", "SL"):
                leave_name = generative_leave.leave.name
                text = (
                    'वेतन सहित अवकाश' if leave_name == "EL" else
                    'आकस्मिक अवकाश' if leave_name == "CL" else
                    'बीमारी अवकाश' if leave_name == "SL" else
                    ''
                )                
                payslip.cell(w=None, h=main_table_cell_height, text=text)
            #Value
            payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*(6+index))
            payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(generative_leave.leave_count/2) if (generative_leave.leave_count/2)%1==0 else generative_leave.leave_count/2}', new_x="RIGHT", align='R')
            payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*(6+index+1))
        
        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['attendance'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.cell(w=None, h=main_table_cell_height, text=f'Paid Days{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'देय कार्यदिवस')
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['attendance'], h=main_table_cell_height, text=f'{int(employee_monthly_details.paid_days_count/2) if (employee_monthly_details.paid_days_count/2)%1==0 else employee_monthly_details.paid_days_count/2}', new_x="RIGHT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)

        #Salary Wage Rate
        employee_salary_rates = EmployeeSalaryEarning.objects.filter(from_date__lte=salary.date, to_date__gte=salary.date, employee=salary.employee.id).order_by('earnings_head__id')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["salary_wage_rate"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['salary_wage_rate'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Salary/Wage Rate", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['salary_wage_rate'], h=main_table_cell_height, text=f"वेतन दर", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        payslip.set_font('noto-sans-devanagari', size=7)
        total_earnings_rate = 0
        for index, salary_rate in enumerate(employee_salary_rates):
            payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*(2+index)))
            payslip.cell(w=None, h=main_table_cell_height, text=f'{salary_rate.earnings_head.name[:max_name_earning_head_name_length]}{" /" if language=="hindi" and salary_rate.earnings_head.name in ("Basic", "Conveyance", "SL", "HRA", "Medical", "Other") else ""}', new_x="RIGHT")
            if language=="hindi" and salary_rate.earnings_head.name in ("Basic", "Conveyance", "SL", "HRA", "Medical", "Other"):
                earning_head_name = salary_rate.earnings_head.name
                text = (
                    'मूल वेतन' if earning_head_name == "Basic" else
                    'मकान भत्ता' if earning_head_name == "HRA" else
                    'यातायात भत्ता' if earning_head_name == "Conveyance" else
                    'बीमारी भत्ता' if earning_head_name == "Medical" else
                    'अतिरिक्त्त भत्ता' if earning_head_name == "Other" else
                    ''
                )                
                payslip.cell(w=None, h=main_table_cell_height, text=text)
            #Value
            payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*(2+index))
            payslip.cell(w=width_of_columns['salary_wage_rate'], h=main_table_cell_height, text=f'{salary_rate.value}', new_x="RIGHT", align='R')
            total_earnings_rate += salary_rate.value

        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['salary_wage_rate'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.cell(w=None, h=main_table_cell_height, text=f'Total Rate{" /" if language=="hindi" else ""}', new_x="RIGHT")
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'योग')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['salary_wage_rate'], h=main_table_cell_height, text=f'{total_earnings_rate}', new_x="RIGHT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)


        #Earnings
        earned_amounts = EarnedAmount.objects.filter(salary_prepared = salary.id).order_by('earnings_head__id')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["earnings"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['earnings'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Earnings", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['earnings'], h=main_table_cell_height, text=f"अर्जित वेतन", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        payslip.set_font('noto-sans-devanagari', size=7)
        total_earned_amount = 0
        for index, earned in enumerate(earned_amounts):
            payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*(2+index)))
            payslip.cell(w=width_of_columns['earnings'], h=main_table_cell_height, text=f'{earned.earned_amount-earned.arear_amount}', new_x="RIGHT", align='R')
            total_earned_amount += earned.earned_amount-earned.arear_amount
            print(earned.earned_amount-earned.arear_amount)
        
        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['earnings'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['earnings'], h=main_table_cell_height, text=f'{total_earned_amount}', new_x="RIGHT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)
        
        #Arrears
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns['earnings'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["arrears"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['arrears'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Arrears", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['arrears'], h=main_table_cell_height, text=f"बकाया", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        payslip.set_font('noto-sans-devanagari', size=7)
        total_arrears_amount = 0
        for index, earned in enumerate(earned_amounts):
            payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*(2+index)))
            payslip.cell(w=width_of_columns['earnings'], h=main_table_cell_height, text=f'{earned.arear_amount}', new_x="RIGHT", align='R')
            total_arrears_amount += earned.arear_amount
            print(earned.arear_amount)
        
        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns["earnings"], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['arrears'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['arrears'], h=main_table_cell_height, text=f'{total_arrears_amount}', new_x="RIGHT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)

        #Deductions
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["deductions"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Deductions", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f"कटौतियाँ", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        payslip.set_font('noto-sans-devanagari', size=7)
        total_deductions = 0
        #PF
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*2))
        payslip.cell(w=None, h=main_table_cell_height, text=f'PF{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'ई.पी.एफ')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*2))
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{salary.pf_deducted}', new_x="RIGHT", align='R')
        total_deductions += salary.pf_deducted
        #ESI
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*3))
        payslip.cell(w=None, h=main_table_cell_height, text=f'ESI{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'ई.एस.आई')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*3))
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{salary.esi_deducted}', new_x="RIGHT", align='R')
        total_deductions += salary.esi_deducted
        #Advance
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*4))
        payslip.cell(w=None, h=main_table_cell_height, text=f'Advance{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अग्रिम')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*4))
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{salary.advance_deducted}', new_x="RIGHT", align='R')
        total_deductions += salary.advance_deducted
        #TDS
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*5))
        payslip.cell(w=None, h=main_table_cell_height, text=f'TDS{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'टी.डी.एस')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*5))
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{salary.tds_deducted}', new_x="RIGHT", align='R')
        total_deductions += salary.tds_deducted
        #Others
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*6))
        payslip.cell(w=None, h=main_table_cell_height, text=f'Other{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अतिरिक्त्त')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*6))
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{salary.others_deducted}', new_x="RIGHT", align='R')
        total_deductions += salary.others_deducted

        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns["earnings"]+width_of_columns['arrears'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['deductions'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['deductions'], h=main_table_cell_height, text=f'{total_deductions}', new_x="RIGHT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)

        #Net Salary
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns['earnings']+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8)
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=width_of_columns["net_salary"], h=(default_number_of_cells_in_main_row+1)*main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height if language=='hindi' else main_table_cell_height*2, text=f"Net Salary", new_x="LEFT", new_y="NEXT",align='C', border='TLR' if language=='hindi' else 1)
        if language=='hindi':
            payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height, text=f"कुल देय वेतन", new_x="LEFT", new_y="NEXT",align='C', border='BLR')

        #OT Hrs
        payslip.set_font('noto-sans-devanagari', size=7)
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*2))
        payslip.cell(w=None, h=main_table_cell_height, text=f'OT Hrs{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अतिरिक्त्त घंटे')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*2))
        payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height, text=f'{salary.net_ot_minutes_monthly/60}', new_x="RIGHT", align='R')

        #OT Amount
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*3))
        payslip.cell(w=None, h=main_table_cell_height, text=f'OT Amt{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'अतिरिक्त्त वेतन')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*3))
        payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height, text=f'{salary.net_ot_amount_monthly}', new_x="RIGHT", align='R')

        #Incentive
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*4))
        payslip.cell(w=None, h=main_table_cell_height, text=f'Incentive{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'प्रोत्साहन')
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns["salary_wage_rate"]+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates["y"]+intro_cell_height*8+(main_table_cell_height*4))
        payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height, text=f'{salary.incentive_amount}', new_x="RIGHT", align='R')


        net_salary = (total_earned_amount+total_arrears_amount+salary.net_ot_amount_monthly+salary.incentive_amount) - total_deductions        
        #Printing Total
        payslip.set_xy(x=current_payslip_initial_coordinates['x']+width_of_columns['attendance']+width_of_columns['salary_wage_rate']+width_of_columns["earnings"]+width_of_columns['arrears']+width_of_columns['deductions'], y=current_payslip_initial_coordinates['y']+intro_cell_height*8+main_table_cell_height*default_number_of_cells_in_main_row)
        payslip.set_line_width(width=0.1)
        payslip.line(x1=payslip.get_x(), x2=payslip.get_x()+width_of_columns['net_salary'], y1=payslip.get_y(), y2=payslip.get_y())
        payslip.set_line_width(width=0.2)
        payslip.set_font('noto-sans-devanagari', size=7, style='B')
        payslip.cell(w=width_of_columns['net_salary'], h=main_table_cell_height, text=f'{net_salary}', new_x="LMARGIN", new_y="NEXT", align='R')
        payslip.set_font('noto-sans-devanagari', size=7) 

        #Signature Row
        payslip.rect(x=payslip.get_x(), y=payslip.get_y(), w=page_width-left_margin-right_margin, h=main_table_cell_height)
        payslip.cell(w=None, h=main_table_cell_height, text=f'Authorised Signature{" /" if language=="hindi" else ""}', new_x="RIGHT", align='L')
        if language=="hindi":
            payslip.cell(w=None, h=main_table_cell_height, text=f'हस्ताक्षर प्रमाणित कर्ता', new_x='RIGHT')

        #get_string_width
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=payslip.get_y())
        employee_signature_hindi_width = payslip.get_string_width("हस्ताक्षर कर्मचारी")
        payslip.cell(w=(page_width-left_margin-right_margin)-employee_signature_hindi_width-2 if language=='hindi' else page_width-left_margin-right_margin, h=main_table_cell_height, text=f"Employee's Signature{' /' if language=='hindi' else ''}", new_x="RIGHT", align='R')
        if language=="hindi":
            payslip.cell(w=employee_signature_hindi_width, h=main_table_cell_height, text=f'हस्ताक्षर कर्मचारी', new_x='RIGHT')

        #This is computer generated payslip
        payslip.set_xy(x=current_payslip_initial_coordinates['x'], y=payslip.get_y()+main_table_cell_height)
        payslip.set_font('noto-sans-devanagari', size=4)
        payslip.cell(w=(page_width-left_margin-right_margin), h=2, text=f'This is a computer generated pay slip and does not require signature', new_x="LMARGIN", align='R')
        payslip.set_font('noto-sans-devanagari', size=7)

        if (employee_index+1)%rows_per_page==0 and employee_index!=0 and employee_index<(len(employee_salaries)-1):
            #Adding new page
            payslip.add_page()
            payslip.set_xy(x=initial_coordinates_after_header['x'], y=initial_coordinates_after_header['y'])
        else:
            #Drawing Dashed Line 
            payslip.set_dash_pattern(dash=1, gap=1)
            payslip.line(x1=payslip.get_x(), y1=payslip.get_y()+cell_height_for_dashed_line, x2=204, y2=payslip.get_y()+cell_height_for_dashed_line)
            payslip.set_dash_pattern(dash=0)
            #Setting Position for next
            payslip.set_xy(x=current_payslip_initial_coordinates['x'],y=payslip.get_y()+cell_height_for_dashed_line*2)

    buffer = bytes(payslip.output())
    yield buffer