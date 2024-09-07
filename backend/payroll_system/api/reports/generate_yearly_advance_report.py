from fpdf import FPDF
import os
from ..models import CompanyDetails, EmployeeGenerativeLeaveRecord, LeaveGrade, EmployeeSalaryEarning, EarnedAmount, LeaveGrade, EarningsHead, EmployeeLeaveOpening, EmployeeAdvanceEmiRepayment, EmployeeAdvancePayment, EmployeeSalaryPrepared
from datetime import date
import calendar
from django.db.models import Q, Sum
from django.db.models import Prefetch

# from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

#A4 size 210 x 297 mm
width_of_columns = {
       "right_intro_header": 80,
       "summary_header": 30,
       "summary_value": 20,
       "summary_gap": 10,
       #Main Table
       "advance_period": 35,
       "advance_taken_amt_date": 168,
       "advance_deducted": 22,
       "earnings_rate": 22,
       "total_earned": 37,
    }

def generate_yearly_advance_report(user, request_data, employees):
    default_cell_height = 5.5
    default_cell_height_small = 4
    default_cell_height_extra_small = 3.5
    default_cell_height_for_heading = 8
    left_margin = 6
    right_margin = 7
    bottom_margin = 3
    top_margin = 6
    height_of_table_header = 18 
    height_of_table_row = 8.5

    yearly_advance_report = FPDF(orientation="L", unit="mm", format="A4")

    #Page settings
    yearly_advance_report.set_margins(left=left_margin, top=top_margin, right=right_margin)
    yearly_advance_report.add_page()
    yearly_advance_report.set_auto_page_break(auto=True, margin = bottom_margin)
    initial_coordinates = {"x": yearly_advance_report.get_x(), "y": yearly_advance_report.get_y()}
    yearly_advance_report.set_font("Helvetica", size=9)

    months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
    ]
    grand_total = {
        "advance_taken_amount": 0,
        "advance_deducted": 0,
        "rate": 0,
        "total_earned": 0,
    }

    employees = employees.prefetch_related(
        Prefetch('earnings', queryset=EmployeeSalaryEarning.objects.all()),
        Prefetch('salaries_prepared', queryset=EmployeeSalaryPrepared.objects.filter(user=user, date__year=request_data['year'])),  # Prefetching salaries prepared
        Prefetch('salaries_prepared__current_salary_earned_amounts', queryset=EarnedAmount.objects.filter(user=user)),  # Prefetching earned amounts within salaries prepared
        Prefetch('advance_payments', queryset=EmployeeAdvancePayment.objects.filter(date__year__lte=request_data['year'])),
        Prefetch('salaries_prepared__emis_with_salary_prepared', queryset=EmployeeAdvanceEmiRepayment.objects.filter(user=user, salary_prepared__date__year=request_data['year'])),
        Prefetch('advance_payments__all_emis_of_advance', queryset=EmployeeAdvanceEmiRepayment.objects.filter(user=user, salary_prepared__date__year__lte=request_data['year'])),
        Prefetch('company__earnings_heads', queryset=EarningsHead.objects.filter(company_id=request_data['company'])),
    ).select_related(
        'employee_professional_detail__designation', 
        'employee_professional_detail__department',
        'company'  # Select related to optimize fetching of company data
    )
    print(employees.first().advance_payments.first().all_emis_of_advance.all())

    
    for index, employee in enumerate(employees):
        yearly_advance_report.set_line_width(width=0.4)
        ##Intro on left
        #ACN
        yearly_advance_report.set_font("Helvetica", size=9, style='')
        yearly_advance_report.cell(w=0, h=default_cell_height, text=f"ACN : {employee.attendance_card_no}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        #Department
        employee_department = ''
        try: employee_department = employee.employee_professional_detail.department.name
        except: pass
        yearly_advance_report.cell(w=0, h=default_cell_height, text=f"Department : {employee_department}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        #DOJ
        employee_doj = ''
        try: employee_doj = employee.employee_professional_detail.date_of_joining.strftime('%d-%b-%Y')
        except: pass
        yearly_advance_report.cell(w=0, h=default_cell_height, text=f"Date of Joining: {employee_doj}", align="L", new_x="LMARGIN", new_y='NEXT', border=0)

        ##Center Heading
        yearly_advance_report.set_xy(x=initial_coordinates['x'], y=initial_coordinates['y'])
        yearly_advance_report.set_font("Helvetica", size=16, style='B')
        yearly_advance_report.cell(w=0, h=default_cell_height_for_heading, text=f'Yearly Advance Report', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
        #yearly_advance_report.set_font("Helvetica", size=9, style='')
        #yearly_advance_report.cell(w=0, h=default_cell_height, text=f'Year: {request_data["year"]}', align="C", new_x="LMARGIN", new_y='NEXT', border=0)
        yearly_advance_report.set_font("Helvetica", size=12, style='')
        #Centering the Company Name
        name_heading_width = yearly_advance_report.get_string_width(f'Name of Organization : {employee.company.name}')
        yearly_advance_report.set_xy(x=(297-name_heading_width)/2-4, y=yearly_advance_report.get_y())
        yearly_advance_report.cell(w=None, h=default_cell_height, text=f'Name of Organization :', align="L", new_x="RIGHT", new_y='TOP', border=0)
        yearly_advance_report.set_font("Helvetica", size=12, style='B')
        yearly_advance_report.cell(w=None, h=default_cell_height, text=f'{employee.company.name}', align="L", new_x="LMARGIN", new_y='NEXT', border=0)
        
        ##Intro on right
        yearly_advance_report.set_xy(x=(297-right_margin-width_of_columns['right_intro_header']), y=initial_coordinates['y'])
        yearly_advance_report.set_font("Helvetica", size=9, style='')
        #Paycode
        yearly_advance_report.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f'Paycode : {employee.paycode}', align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Name
        yearly_advance_report.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f'Name : {employee.name}', align="L", new_x="LEFT", new_y='NEXT', border=0)
        #Father Name
        yearly_advance_report.cell(w=width_of_columns['right_intro_header'], h=default_cell_height, text=f"Father's/Husband's Name : {employee.father_or_husband_name if employee.father_or_husband_name else ''}", align="L", new_x="LEFT", new_y='NEXT', border=0)
        
        ##Table Headers
        yearly_advance_report.set_xy(x=left_margin, y=yearly_advance_report.get_y()+default_cell_height) #NEXT line
        yearly_advance_report.set_font("Helvetica", size=8, style='B')
        initial_coordinates_before_table_headers = {"x": yearly_advance_report.get_x(), "y": yearly_advance_report.get_y()}
        #Advance Report Period
        yearly_advance_report.cell(w=width_of_columns['advance_period'], h=height_of_table_header/3, text=f"Advance Report Period", align="C", new_x="LEFT", new_y="NEXT", border="TLR")
        yearly_advance_report.cell(w=width_of_columns['advance_period'], h=height_of_table_header/3, text=f"From: Jan {request_data['year']}", align="L", new_x="LEFT", new_y="NEXT", border="LR")
        yearly_advance_report.cell(w=width_of_columns['advance_period'], h=height_of_table_header/3, text=f"To: Dec {request_data['year']}", align="L", new_x="RIGHT", new_y="NEXT", border="LRB")

        #Advance Taken Amount and Date
        yearly_advance_report.set_xy(x=yearly_advance_report.get_x(), y=initial_coordinates_before_table_headers['y'])
        yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date'], h=height_of_table_header/4, text=f"Advance Taken", align="C", new_x="LEFT", new_y="NEXT", border="TLR")
        yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date'], h=height_of_table_header/4, text=f"Amount", align="C", new_x="LEFT", new_y="NEXT", border="LR")
        yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date'], h=height_of_table_header/4, text=f"Date", align="C", new_x="LEFT", new_y="NEXT", border="LR")
        yearly_advance_report.set_font("Helvetica", size=6.5, style='')
        yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date'], h=height_of_table_header/4, text=f"Note: Max of 10 advances taken in a month will be visible here", align="L", new_x="RIGHT", new_y="NEXT", border="LRB")
        
        #Advance Deducted 
        yearly_advance_report.set_xy(x=yearly_advance_report.get_x(), y=initial_coordinates_before_table_headers['y'])
        yearly_advance_report.set_font("Helvetica", size=8, style='B')
        yearly_advance_report.cell(w=width_of_columns['advance_deducted'], h=height_of_table_header/2, text=f"Advance", align="C", new_x="LEFT", new_y="NEXT", border="TLR")
        yearly_advance_report.cell(w=width_of_columns['advance_deducted'], h=height_of_table_header/2, text=f"Deducted", align="C", new_x="RIGHT", new_y="NEXT", border="LRB")

        #Rate
        yearly_advance_report.set_xy(x=yearly_advance_report.get_x(), y=initial_coordinates_before_table_headers['y'])
        yearly_advance_report.set_font("Helvetica", size=8, style='B')
        yearly_advance_report.cell(w=width_of_columns['earnings_rate'], h=height_of_table_header, text=f"Rate", align="C", new_x="RIGHT", new_y="TOP", border=1)

        #Totol EarnedAmount
        yearly_advance_report.cell(w=width_of_columns['total_earned'], h=height_of_table_header/3, text=f"Total", align="C", new_x="LEFT", new_y="NEXT", border="TLR")
        yearly_advance_report.cell(w=width_of_columns['total_earned'], h=height_of_table_header/3, text=f"Earned", align="C", new_x="LEFT", new_y="NEXT", border="LR")
        yearly_advance_report.cell(w=width_of_columns['total_earned'], h=height_of_table_header/3, text=f"(incl OT, Incentive, Arrear)", align="C", new_x="RIGHT", new_y="NEXT", border="LRB")
        
        yearly_advance_report.set_xy(x=left_margin, y=yearly_advance_report.get_y())
        yearly_advance_report.set_line_width(width=0.3)
        ##Main Table Rows
        yearly_advance_report.set_font("Helvetica", size=7, style='')
        for month_index, month in enumerate(months):
            #Prepared Salary
            current_month_salary = None
            try: current_month_salary = employee.salaries_prepared.filter(date__month=month_index+1, date__day=1).first()
            except: pass
            
            #Earned Amounts
            earned_amounts = None
            if current_month_salary:
                earned_amounts = current_month_salary.current_salary_earned_amounts.all()
            
            #Total Earned (incl OT, Incentive and Arrear)
            total_earnings_amount = None
            if earned_amounts and earned_amounts.exists():
                total_earnings_amount = 0
                for earned in earned_amounts:
                    total_earnings_amount += (earned.earned_amount)
            if total_earnings_amount!=None and current_month_salary!=None:
                total_earnings_amount += current_month_salary.net_ot_amount_monthly
                total_earnings_amount += current_month_salary.incentive_amount

            #Advance Period
            yearly_advance_report.cell(w=width_of_columns['advance_period'], h=default_cell_height*2, text=f"{month}", align="C", new_x="RIGHT", new_y='TOP', border=1)

            #Advance Taken amount date
            yearly_advance_report.rect(x=yearly_advance_report.get_x(), y=yearly_advance_report.get_y(), w=width_of_columns["advance_taken_amt_date"], h=default_cell_height*2)
            yearly_advance_report.set_line_width(width=0.1)
            # advances_taken_current_month = EmployeeAdvancePayment.objects.filter(
            #         employee=employee,
            #         date__year=request_data['year'],
            #         date__month=month_index+1,
            #     ).order_by('date')
            advances_taken_current_month = employee.advance_payments.filter(date__year=request_data['year'], date__month=month_index+1)

            for count in range(10):
                advance_taken = None
                try:
                    advance_taken = advances_taken_current_month[count]
                    if advance_taken!=None:
                        grand_total['advance_taken_amount'] += advance_taken.principal
                except: pass
                yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date']/10, h=default_cell_height, text=f"{advance_taken.principal if advance_taken != None else ''}", align="L", new_x="LEFT", new_y='NEXT', border=1)
                yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date']/10, h=default_cell_height, text=f"{advance_taken.date.strftime('%d-%b-%Y') if advance_taken!=None else ''}", align="L", new_x="RIGHT", new_y='TOP', border=1)
                yearly_advance_report.set_xy(x=yearly_advance_report.get_x(), y=yearly_advance_report.get_y()-default_cell_height)
            
            #Advance deducted (getting from EmployeeAdvanceEmiRepayment)
            related_repayments = None
            total_amount = None
            try:
                #related_repayments = EmployeeAdvanceEmiRepayment.objects.filter(user=user, salary_prepared=current_month_salary)
                related_repayments = current_month_salary.emis_with_salary_prepared.all()
                total_amount = related_repayments.aggregate(total=Sum('amount'))['total']
            except: pass
            if total_amount==None:
                if current_month_salary!=None:
                    total_amount = 0
            yearly_advance_report.set_line_width(width=0.3)
            yearly_advance_report.cell(w=width_of_columns['advance_deducted'], h=default_cell_height*2, text=f"{total_amount if total_amount!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)
            grand_total['advance_deducted'] += total_amount if total_amount != None else 0

            #Salary Rate
            # total_earnings_rate = None
            # try:
            #     total_earnings_rate = 0
            #     earnings_heads = employee.company.earnings_heads.all()
            #     #earnings_heads = EarningsHead.objects.filter(company_id=request_data['company'])
            #     #employee_salary_rates = EmployeeSalaryEarning.objects.filter(employee=employee, from_date__lte=date(request_data['year'], month_index+1, 1), to_date__gte=date(request_data['year'], month_index+1, 1))
            #     employee_salary_rates = employee.earnings.filter(from_date__lte=date(request_data['year'], month_index+1, 1), to_date__gte=date(request_data['year'], month_index+1, 1))
            #
            #     for head in earnings_heads:
            #         salary_for_particular_earning_head = employee_salary_rates.filter(earnings_head=head)
            #
            #         if salary_for_particular_earning_head.exists():
            #             total_earnings_rate += salary_for_particular_earning_head.first().value
            total_earnings_rate = None
            try:
                total_earnings_rate = 0
                earnings_heads = employee.company.earnings_heads.all()
                
                # Filter employee earnings for the given month and year
                employee_salary_rates = employee.earnings.filter(
                    from_date__lte=date(request_data['year'], month_index+1, 1), 
                    to_date__gte=date(request_data['year'], month_index+1, 1)
                )
                
                # Aggregate the total value across all relevant earnings
                total_earnings_rate = employee_salary_rates.filter(
                    earnings_head__in=earnings_heads
                ).aggregate(total=Sum('value'))['total'] or 0
            except: 
                pass
            yearly_advance_report.cell(w=width_of_columns['earnings_rate'], h=default_cell_height*2, text=f"{total_earnings_rate if total_earnings_rate!=None else ''}", align="R", new_x="RIGHT", new_y='TOP', border=1)
            grand_total['rate'] += total_earnings_rate if total_earnings_rate != None else 0

            #Totol EarnedAmount
            yearly_advance_report.cell(w=width_of_columns['total_earned'], h=default_cell_height*2, text=f"{total_earnings_amount if total_earnings_amount!=None else ''}", align="R", new_x="LMARGIN", new_y='NEXT', border=1)
            grand_total["total_earned"] += total_earnings_amount if total_earnings_amount!=None else 0

        #Total
        yearly_advance_report.set_font("Helvetica", size=7, style='B')
        yearly_advance_report.cell(w=width_of_columns['advance_period'], h=default_cell_height, text=f"Total", align="C", new_x="RIGHT", new_y='TOP', border=1)
        yearly_advance_report.cell(w=width_of_columns['advance_taken_amt_date'], h=default_cell_height, text=f"{grand_total['advance_taken_amount']}", align="R", new_x="RIGHT", new_y='TOP', border=1)
        yearly_advance_report.cell(w=width_of_columns['advance_deducted'], h=default_cell_height, text=f"{grand_total['advance_deducted']}", align="R", new_x="RIGHT", new_y='TOP', border=1)
        yearly_advance_report.cell(w=width_of_columns['earnings_rate'], h=default_cell_height, text=f"{grand_total['rate']}", align="R", new_x="RIGHT", new_y='TOP', border=1)
        yearly_advance_report.cell(w=width_of_columns['total_earned'], h=default_cell_height, text=f"{grand_total['total_earned']}", align="R", new_x="LMARGIN", new_y='NEXT', border=1)

        #Advance Left to be repaid until this year
        # advance_payments = EmployeeAdvancePayment.objects.filter(
        #     employee=employee,
        #     date__year__lte=request_data['year']
        # )
        # advance_payments = employee.advance_payments.all()
        advance_payments = employee.advance_payments.all()

        remaining_advance_total = 0

        for advance in advance_payments:
            #Use the repaid_amount property to get the total amount repaid
            repaid_amount = EmployeeAdvanceEmiRepayment.objects.filter(
                user=user,
                employee_advance_payment=advance,
                salary_prepared__date__year__lte=request_data['year']
            ).aggregate(total_repaid=Sum('amount'))['total_repaid'] or 0
            #repaid_amount = advance.all_emis_of_advance.aggregate(total_repaid=Sum('amount'))['total_repaid'] or 0
            remaining_amount = advance.principal - repaid_amount
            remaining_advance_total += remaining_amount

        yearly_advance_report.cell(w=0, h=default_cell_height, text=f"Advance left to be repaid (by the end of {request_data['year']}): {remaining_advance_total}", align="L", new_x="RIGHT", new_y='TOP', border=1)


        



    #Add Next Page
        if index!=len(employees)-1:
            yearly_advance_report.add_page()
            yearly_advance_report.set_xy(x=yearly_advance_report.get_x(), y=yearly_advance_report.get_y())

    buffer = bytes(yearly_advance_report.output())
    yield buffer
