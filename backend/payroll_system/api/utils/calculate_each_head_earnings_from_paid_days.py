from ..models import EmployeeSalaryEarning
from datetime import date
import calendar
from decimal import Decimal, ROUND_HALF_UP

def calculate_each_head_earnings_from_paid_days(month, year, employee, company_id, user, paid_days_count): 
    """
    Calculates earnings for each salary head based on the employee's paid days in a given month.

    Parameters:
    - month (int): The month for which earnings are calculated (1-12).
    - year (int): The year for which earnings are calculated.
    - employee (EmployeePersonalDetails Object): The employee object for whom earnings are being calculated.
    - company_id (int): The ID of the company the employee belongs to.
    - user (User): The user requesting the calculation (for permissions/logging if needed).
    - paid_days_count (int): The number of paid days recorded for the employee. 
    (Each paid day count represents half a day, hence it is divided by 2 to get actual working days.)

    Returns:
    - dict: A dictionary where keys are earning head IDs and values contain the rate, earned amount, and arrear amount.
    """
    employee_salary_earnings_for_each_head = EmployeeSalaryEarning.objects.filter(user=user if user.role=='OWNER' else user.regular_to_owner.owner, company_id=company_id, from_date__lte=date(year=year, month=month, day=1), to_date__gte=date(year=year, month=month, day=1), employee=employee)

    days_in_month = calendar.monthrange(year, month)[1]
    total_salary_rate = 0
    total_earned_amount = 0
    earned_amount_dict = {}
    for salary_earning in employee_salary_earnings_for_each_head:
        current_earning_earned_amount = (Decimal(salary_earning.value)*(Decimal(paid_days_count)/Decimal(2)))/Decimal(days_in_month)
        # rounded_earning = math.ceil(current_earning_earned_amount) if current_earning_earned_amount >= 0.5 else math.floor(current_earning_earned_amount)
        rounded_earning = current_earning_earned_amount.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        total_earned_amount += rounded_earning
        total_salary_rate += salary_earning.value
        earned_amount_dict[salary_earning.earnings_head.id] = {
            'rate' : salary_earning.value,
            'earned_amount' : rounded_earning,
            'arear_amount': 0,
        }
    print(earned_amount_dict)
    return earned_amount_dict



