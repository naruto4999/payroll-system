# Overtime Rate Multiplier Logic

## Effective Rule

The overtime multiplier is controlled by the authenticated account role and the employee's configured overtime rate:

| Account role | Employee overtime rate | Multiplier |
| --- | --- | --- |
| `REGULAR` | `S` | `2` |
| `REGULAR` | `D` | `2` |
| `OWNER` | `S` | `1` |
| `OWNER` | `D` | `2` |

`REGULAR` refers to the authenticated user/account role, not an employee role or employment type.

## Controlling Implementations

### Frontend Manual Salary Preparation

File: `frontend/src/components/menu/Transaction/forms/SalaryPreparationForm/EditSalary.jsx`

The calculation defaults the multiplier to `2`. For an `OWNER` account, it instead derives the multiplier from the employee overtime rate:

```jsx
let overtimeRateMultiplier = new BigNumber(2);

if (auth.account.role == 'OWNER') {
    overtimeRateMultiplier = new BigNumber(
        currentEmployeeSalaryDetails?.overtimeRate == 'D' ? 2 : 1
    );
}
```

The multiplier is applied to both daily and monthly salary overtime calculations. The resulting `netOtAmountMonthly` is submitted to the backend, which validates and persists the submitted value without recalculating it.

### Backend Bulk Salary Preparation

File: `backend/payroll_system/api/managers.py`

```python
overtime_rate_multiplier = (
    2
    if employee_salary_detail.first().overtime_rate == 'D'
    or user.role == 'REGULAR'
    else 1
)
```

This is used by bulk salary preparation. It explicitly implements `D or REGULAR -> 2`, otherwise `1`.

The related overtime divisor behavior is:

- `REGULAR` accounts use `26`.
- `OWNER` accounts can use the applicable company overtime calculation configuration.

### Earned-Salary OT and Attendance Calculation

File: `backend/payroll_system/api/services/calculate_ot_attendance_using_earned_salary.py`

```python
overtime_rate_multiplier = (
    2
    if employee_salary_detail.first().overtime_rate == 'D'
    or user.role == 'REGULAR'
    else 1
)
```

This duplicates the bulk preparation condition. Here, the multiplier determines the hourly overtime rate and therefore the number of overtime hours generated to reach the target earned salary.

## Daily Overtime Report Inconsistency

File: `backend/payroll_system/api/reports/generate_overtime_sheet_daily.py`

```python
overtime_rate_multiplier = (
    2 if attendance.employee.employee_salary_detail.overtime_rate == 'D' else 1
)
```

This report calculation only considers the employee's `S` or `D` overtime rate. It does not apply the `REGULAR` account override.

Consequently, a `REGULAR` account with an employee overtime rate of `S` receives multiplier `2` during salary preparation but multiplier `1` in the daily overtime report calculation.

## Overtime Rate Configuration

The backend `S` and `D` choices are defined in:

- `backend/payroll_system/api/models.py`

The frontend employee salary editor is in:

- `frontend/src/components/menu/MasterEntry/forms/EmployeeEntryForm/EmployeeSalaryDetail.jsx`

The configured values are:

- `S`: Single
- `D`: Double

For `REGULAR` accounts, salary calculations force multiplier `2` even when the employee is configured with `S`.

## Risks and Test Coverage

- The primary rule is independently implemented in the frontend manual calculation, backend bulk preparation, and backend earned-salary service.
- The frontend defaults every non-`OWNER` role to `2`, while the backend explicitly checks for `REGULAR`. These remain equivalent only while `OWNER` and `REGULAR` are the only account roles.
- The daily overtime report does not implement the `REGULAR` override.
- Manual salary preparation trusts the frontend-calculated overtime amount rather than recalculating it on the backend.
- No tests currently assert the overtime multiplier behavior for `REGULAR`, `OWNER`, `S`, or `D` combinations.
