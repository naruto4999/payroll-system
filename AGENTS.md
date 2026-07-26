# Repository Guidance

## Overtime Calculation

- The overtime multiplier is `2` when the authenticated account role is `REGULAR` or the employee's overtime rate is `D` (double). Otherwise, it is `1`.
- For daily salaries, overtime amount is `(total salary rate / 8) * net OT hours * overtime multiplier`.
- For monthly salaries, overtime amount is `(total salary rate / overtime divisor / 8) * net OT hours * overtime multiplier`.
- `REGULAR` accounts use an overtime divisor of `26`. `OWNER` accounts use the applicable company overtime calculation configuration.
- Keep the manual frontend calculation and backend bulk/earned-salary calculations aligned when changing this rule.
- The controlling implementations are:
  - `frontend/src/components/menu/Transaction/forms/SalaryPreparationForm/EditSalary.jsx`
  - `backend/payroll_system/api/managers.py`
