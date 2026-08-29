# Repository Guidance

## API Naming

- Frontend API payloads and responses use camelCase. Django REST Framework's `djangorestframework-camel-case` middleware, parser, and renderer convert between camelCase and snake_case at the API boundary.
- Do not report or fix camelCase request fields as backend naming mismatches.

## Overtime Calculation

- `REGULAR` calculations always use the company system `ALL_DAYS_DOUBLE` policy. `OWNER` calculations use the employee's explicit overtime policy or the active company default.
- Use the selected policy's category multipliers without applying an additional legacy `overtime_rate` (`S`/`D`) multiplier.
- For daily salaries, overtime amount is `(total salary rate / 8) * net OT hours * overtime multiplier`.
- For monthly salaries, overtime amount is `(total salary rate / overtime divisor / 8) * net OT hours * overtime multiplier`.
- `REGULAR` accounts use an overtime divisor of `26`. `OWNER` accounts use the applicable company overtime calculation configuration.
- Within each attendance row, combine policy-eligible chunks that have the same multiplier and round that multiplier bucket once. Round chunks with different multipliers separately; never combine different attendance rows before rounding.
- Allocate each bucket's rounding difference back to its day-type chunks deterministically before deducting late minutes. Round total monthly late minutes once with the existing `30/20` rule, deduct by `late_deduction_priority`, and do not round net overtime again.
- Keep the manual frontend calculation and backend bulk calculation aligned when changing this rule.
- The earned-salary reverse-calculation feature is deprecated. Disable and remove it according to `backend-overtime-blockers-fix-plan.md`; do not repair or align its calculation logic.
- The controlling implementations are:
  - `frontend/src/components/menu/Transaction/forms/SalaryPreparationForm/EditSalary.jsx`
  - `backend/payroll_system/api/managers.py`
