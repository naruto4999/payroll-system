# Repository Guidance

## Overtime Calculation

- `REGULAR` calculations always use the company system `ALL_DAYS_DOUBLE` policy. `OWNER` calculations use the employee's explicit overtime policy or the active company default.
- Use the selected policy's category multipliers without applying an additional legacy `overtime_rate` (`S`/`D`) multiplier.
- For daily salaries, overtime amount is `(total salary rate / 8) * net OT hours * overtime multiplier`.
- For monthly salaries, overtime amount is `(total salary rate / overtime divisor / 8) * net OT hours * overtime multiplier`.
- `REGULAR` accounts use an overtime divisor of `26`. `OWNER` accounts use the applicable company overtime calculation configuration.
- Keep the manual frontend calculation and backend bulk calculation aligned when changing this rule.
- The earned-salary reverse-calculation feature is deprecated. Disable and remove it according to `backend-overtime-blockers-fix-plan.md`; do not repair or align its calculation logic.
- The controlling implementations are:
  - `frontend/src/components/menu/Transaction/forms/SalaryPreparationForm/EditSalary.jsx`
  - `backend/payroll_system/api/managers.py`
