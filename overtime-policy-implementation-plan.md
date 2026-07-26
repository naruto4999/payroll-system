# Configurable Overtime Policy Implementation Plan

## Recommendation

Use a dedicated, normalized overtime policy model. `ExtraFeaturesConfig` should remain limited to feature toggles; storing payroll rules there would become difficult to validate, audit, and extend.

The current calculation does use the sum of all active earning-head rates as the OT base in the frontend, bulk backend calculation, earned-salary service, and daily OT report.

## Proposed Model

```text
OvertimePolicy
- id
- company_id
- name
- code
- is_default
- is_active
- earnings_basis: ALL_EARNINGS | SELECTED_HEADS
- created_at / updated_at
```

```text
OvertimePolicyDayRule
- policy_id
- day_type: REGULAR | WEEKLY_OFF | HOLIDAY
- multiplier: Decimal
- late_deduction_priority: PositiveSmallInteger
```

```text
OvertimePolicyEarningsHead
- policy_id
- earnings_head_id
```

```text
EmployeeSalaryDetail
- overtime_policy_id: nullable FK
```

```text
EmployeeAttendanceOvertimeDetail
- attendance_id
- work_date
- day_type: REGULAR | WEEKLY_OFF | HOLIDAY
- source: EARLY_ARRIVAL | LATE_DEPARTURE | OFF_DAY_WORK | MANUAL | IMPORTED
- start_datetime: nullable
- end_datetime: nullable
- gross_minutes
- excluded_minutes
- eligible_minutes
- created_at / updated_at
```

Semantics:

- A null employee policy means "use the company default."
- Selecting another company policy is the employee override.
- A policy with no day rules means no overtime.
- The absence of a day rule means that day type is not OT-eligible.
- Extra-off days map to `WEEKLY_OFF`.
- A holiday takes precedence when a date is both a holiday and weekly off.
- `WO` and `WO*` share the weekly-off category; `HD` and `HD*` share the holiday category.
- Compensation off remains excluded until explicitly added as another day type.
- `late_deduction_priority=1` is deducted first, then `2`, and so on.
- Add unique constraints for `(policy, day_type)` and `(policy, late_deduction_priority)`.
- Store multipliers as `DecimalField`, not floating point. Three decimal places should cover values such as `1`, `1.2`, `1.25`, and `1.5`.
- Validate that multipliers are positive and selected earning heads belong to the same company.
- Do not add `user_id`; ownership is already available through `policy.company.user`.

`earnings_basis` is important for compatibility:

- Migrated legacy policies use `ALL_EARNINGS`, preserving the current behavior even when another earning head is added later.
- Pahwa's policy uses `SELECTED_HEADS` with only the Basic head.
- This is safer than populating a many-to-many relation with every currently existing head.

## Implementation Plan

### 1. Add the policy schema

- Add the three policy models and constraints in `backend/payroll_system/api/models.py`.
- Add the nullable policy FK to `EmployeeSalaryDetail`.
- Use `PROTECT` for assigned policies and deactivate policies instead of deleting them.
- Enforce one active default policy per company with a conditional unique constraint.
- Add serializer validation for company, employee, policy, and earning-head ownership.
- Add a company `post_save` receiver that creates the five standard system policies for every newly created company:

| Policy name | Stable code | Day rules | Multiplier | Earnings basis |
|---|---|---|---:|---|
| No overtime | `NO_OVERTIME` | None | N/A | All earnings |
| All days - single rate | `ALL_DAYS_SINGLE` | Regular, WO, HD | 1 | All earnings |
| WO/HD - single rate | `WO_HD_SINGLE` | WO, HD | 1 | All earnings |
| All days - double rate | `ALL_DAYS_DOUBLE` | Regular, WO, HD | 2 | All earnings |
| WO/HD - double rate | `WO_HD_DOUBLE` | WO, HD | 2 | All earnings |

- Mark these policies as system policies so their stable codes and required rules cannot be accidentally changed or deleted. Their display names may be editable only if the API keeps behavior tied to the stable code and rules, not the name.
- Make `NO_OVERTIME` the default policy for a new company, preserving the current new-employee behavior.
- Keep runtime policy creation in a reusable, atomic, idempotent service called by the receiver. Use `get_or_create` with `(company, code)` and repair/create missing standard day rules without creating duplicates.
- Run the receiver only when `created=True`, and return immediately when `raw=True` so fixture loading does not create duplicate related data.

### 2. Migrate existing records without changing payroll

Use a self-contained `RunPython` data migration with historical models to create the same five system policies for every existing company. Do not import the runtime receiver or service into the migration:

| Policy name | Stable code | Day rules | Multiplier | Earnings basis |
|---|---|---|---:|---|
| No overtime | `NO_OVERTIME` | None | N/A | All earnings |
| All days - single rate | `ALL_DAYS_SINGLE` | Regular, WO, HD | 1 | All earnings |
| WO/HD - single rate | `WO_HD_SINGLE` | WO, HD | 1 | All earnings |
| All days - double rate | `ALL_DAYS_DOUBLE` | Regular, WO, HD | 2 | All earnings |
| WO/HD - double rate | `WO_HD_DOUBLE` | WO, HD | 2 | All earnings |

- Map every existing employee's `overtime_type` and `overtime_rate` to an explicit policy.
- Map enabled records with a null/blank rate to single-rate because that matches existing runtime behavior.
- Map `no_overtime` records to the no-overtime policy regardless of stale S/D values.
- Abort and report unknown values instead of silently changing payroll.
- Make `NO_OVERTIME` the initial default for every existing company unless an explicit company default has already been configured during a staged rollout.
- Existing employees remain explicitly assigned to their migrated policy, as requested.
- Remove the legacy fields only after the new API and frontend are deployed and verified.

### 3. Centralize day classification

- Introduce one backend classifier returning `REGULAR`, `WEEKLY_OFF`, or `HOLIDAY`.
- Replace scattered checks in `backend/payroll_system/api/managers.py` and the earned-salary service.
- Add `EmployeeAttendanceOvertimeDetail` as the source of categorized daily OT, rather than storing only one `ot_day_type` on attendance. One row represents one continuous OT interval.
- Keep `EmployeeAttendance.ot_min` as a compatibility aggregate synchronized from its overtime details.
- Backfill existing OT attendance using the best available holiday and employee-off configuration, reporting ambiguous rows.

The detail fields have these meanings:

- `attendance` links every segment to the attendance/shift that produced it. Multiple overnight segments can link to the same attendance record.
- `work_date` is the local payroll date used to classify the segment and select its policy rule.
- `day_type` stores the historical classification so later holiday or weekly-off changes do not reclassify old OT.
- `start_datetime` and `end_datetime` are timezone-aware boundaries of the exact continuous interval considered for OT. They describe OT time, not the complete punch or normal shift interval.
- `start_datetime` and `end_datetime` must either both be present or both be null. They can be null for duration-only manual entries.
- `gross_minutes` is the duration between the datetimes, or the manually entered duration when exact times are unavailable.
- `excluded_minutes` records lunch, unpaid breaks, or other ineligible time inside the interval.
- `eligible_minutes` must equal `gross_minutes - excluded_minutes`. It is stored before OT rounding and monthly late deduction.

Add database and service validation for:

- Both datetimes being null or both being set.
- `end_datetime > start_datetime`.
- `gross_minutes > 0` and matching the datetime duration when datetimes are present.
- `excluded_minutes <= gross_minutes`.
- `eligible_minutes = gross_minutes - excluded_minutes` and `eligible_minutes > 0`.
- Non-overlapping exact intervals for the same attendance.
- A segment not crossing a local payroll-date boundary, except that it may end exactly at the following midnight and still belong to the preceding `work_date`.

Use this day-type precedence when classifications overlap:

```text
HOLIDAY > WEEKLY_OFF > REGULAR
```

Employee extra-off days are classified as `WEEKLY_OFF`. `WO` and `WO*` share that category; `HD` and `HD*` share `HOLIDAY`. Compensation off remains excluded until explicitly introduced as another policy day type.

Split overnight OT at every midnight in the company payroll timezone before classifying and saving it. For example:

```text
Original OT interval:
Saturday 23:00 -> Sunday 01:30

Detail 1:
attendance       = Saturday shift attendance
start_datetime   = Saturday 23:00
end_datetime     = Sunday 00:00
work_date        = Saturday
day_type         = REGULAR
gross_minutes    = 60
excluded_minutes = 0
eligible_minutes = 60

Detail 2:
attendance       = Saturday shift attendance
start_datetime   = Sunday 00:00
end_datetime     = Sunday 01:30
work_date        = Sunday
day_type         = WEEKLY_OFF
gross_minutes    = 90
excluded_minutes = 0
eligible_minutes = 90
```

Both details belong to the attendance that produced the overnight shift. `work_date`, rather than `attendance.date`, controls each segment's day classification and policy rule.

For a manual duration-only entry, save both datetimes as null and persist the selected date, category, and minutes:

```text
work_date        = Sunday
day_type         = WEEKLY_OFF
source           = MANUAL
start_datetime   = null
end_datetime     = null
gross_minutes    = 120
excluded_minutes = 0
eligible_minutes = 120
```

Do not store multipliers, late-deducted minutes, salary rates, divisors, or monetary amounts on attendance OT details. Those values belong to the prepared-salary overtime snapshot because they depend on the effective payroll policy.

### 4. Centralize monetary calculation

Create a backend overtime calculator that accepts:

- Effective employee policy
- Categorized OT minutes
- Late minutes
- Salary mode
- Effective earning-head rates
- Company divisor
- Authenticated account role

Resolve late deductions in ascending `late_deduction_priority`.

For each `(attendance, work_date, day_type)` group, sum `eligible_minutes` and then apply OT rounding. This preserves the current behavior where early-arrival and late-departure minutes in the same category are combined before 30-minute rounding. If an overnight interval contains multiple payroll dates or day types, round each group separately because each can have a different multiplier.

Calculate each category independently:

```text
daily salary:
eligible rate / 8 * net category hours * category multiplier

monthly salary:
eligible rate / divisor / 8 * net category hours * category multiplier
```

- Preserve the existing `REGULAR` rule: multiplier `2`, divisor `26`.
- Preserve owner divisor behavior from `Calculations.ot_calculation`.
- Round category amounts consistently with `Decimal` and `ROUND_HALF_UP`.
- Sum category amounts into the existing monthly OT amount.

### 5. Store an auditable salary breakdown

Add a prepared-salary overtime detail model containing:

```text
salary_prepared
day_type
gross_minutes
deducted_late_minutes
net_minutes
multiplier
eligible_salary_rate
divisor
amount
```

- Keep existing aggregate OT minute and amount fields for reports and totals.
- Snapshot resolved values so changing a policy later does not rewrite the meaning of prepared historical payroll.
- Treat attendance overtime details as the record of when and under which calendar category OT occurred. Treat prepared-salary overtime details as the record of how that OT was rounded, deducted, rated, and paid.

### 6. Update every backend calculation path

Replace duplicated formulas in:

- `backend/payroll_system/api/managers.py`
- `backend/payroll_system/api/services/calculate_ot_attendance_using_earned_salary.py`
- `backend/payroll_system/api/reports/generate_overtime_sheet_daily.py`

Additional changes:

- Make monthly reports consume the saved breakdown rather than recalculate with current policy.
- For earned-salary reverse calculation, use only eligible day categories. If the policy has no regular-day rule and no eligible off-day attendance can accept OT, return a clear validation error.
- Preserve daily versus monthly formulas; the earned-salary service currently mishandles daily salaries and should be aligned.
- Add explicit authentication to the earned-salary endpoint.

### 7. Add policy APIs

- Add owner-only create/update/deactivate endpoints scoped through the authenticated owner's companies.
- Permit regular accounts to read the effective policies required for attendance and salary preparation.
- Prevent cross-company policy and earning-head assignments.
- Return both the selected policy and resolved effective policy for employee forms.

### 8. Build the company policy UI

Add a dedicated "Overtime Policies" setup screen rather than extending the date-specific "OverTime Settings" subuser-cap screen.

Support:

- Named policies
- Default-policy selection
- Regular/WO/HD rows
- Decimal multiplier per row
- Drag/reorder or numeric late-deduction priority
- All Earnings versus Selected Heads
- Multi-select earning heads
- Active/inactive status

Provide UI shortcuts such as "WO only," "HD only," "WO + HD," and "All days," but persist normalized day rows rather than those combinations.

### 9. Update employee configuration

- Replace the S/D and overtime-type controls in `EmployeeSalaryDetail.jsx`.
- Provide "Use company default," a company-policy selector, and a resolved-policy summary showing eligible days, multipliers, and earning heads.
- Existing migrated employees display their explicitly assigned legacy policy.
- Validate that inactive policies cannot be newly assigned, while retaining them for existing historical assignments.

### 10. Update manual salary preparation

- Change `frontend/src/components/menu/Transaction/forms/SalaryPreparationForm/EditSalary.jsx` to show Regular, WO, and HD OT breakdowns.
- Display gross minutes, deducted late minutes, net minutes, multiplier, and category amount.
- Prefer a backend preview endpoint so the browser does not duplicate payroll policy resolution.
- Recalculate and validate again on save; never trust a submitted OT amount.
- Keep all ordinary earning heads in salary earnings. Filter heads only when determining the OT salary base.
- Update the earned-salary modal's hard-coded documentation to describe the resolved policy.

### 11. Regression coverage

- Test all S/D and overtime-type migration combinations.
- Test arbitrary multipliers such as `1.2`, `1.25`, `1.5`, and `2`.
- Test WO-only, HD-only, WO+HD, and all-day policies.
- Test holiday-over-weekly-off precedence and employee extra-off mapping.
- Test Basic-only and multi-head OT bases.
- Test default inheritance and explicit employee policy selection.
- Test late deduction priority across different multipliers.
- Test daily and monthly salary formulas.
- Test owner divisors `26`, `30`, and calendar days.
- Test preserved REGULAR `2x`/`26` behavior.
- Test frontend preview, bulk preparation, earned-salary calculation, and reports produce matching amounts.
- Test cross-company assignments and policy deactivation.
- Run backend tests and the frontend production build.

## Outcome

This structure covers Pahwa's Basic-only Sunday/holiday rules while supporting future company policies without adding columns for every new WO/HD combination.
