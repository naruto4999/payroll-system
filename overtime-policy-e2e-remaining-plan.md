# Overtime Policy End-to-End Remaining Plan

The current implementation is a policy/schema foundation with partial salary integration. The following work remains for true end-to-end configurable overtime support.

## Backend Blockers

1. Fix effective-policy resolution.
   - `overtime_policy = null` must resolve to the active company default.
   - Current behavior falls back to legacy `overtime_type` / `overtime_rate`.
   - File: `backend/payroll_system/api/services/overtime_policy.py`

2. Make attendance OT details operational.
   - Create/update `EmployeeAttendanceOvertimeDetail` for manual, machine, imported, off-day, and earned-salary OT.
   - Split overnight intervals at midnight.
   - Apply `HOLIDAY > WEEKLY_OFF > REGULAR`.
   - Synchronize `EmployeeAttendance.ot_min` from details.
   - Add interval overlap, date boundary, timezone, and eligible-minute validation.
   - Currently the table exists but nothing writes or reads it.

3. Rewrite the central calculator to consume OT details.
   - Group and round by `(attendance, work_date, day_type)`.
   - Apply late deductions by category priority.
   - Return validation errors for invalid selected-head configurations instead of silently paying zero.

4. Update every attendance writer.
   - Manual attendance create/update.
   - Machine attendance.
   - MDB/direct imports.
   - Bulk autofill/default attendance.
   - Owner-to-regular transfer.
   - Earned-salary attendance generation.
   - Remove legacy `overtime_type` gating from `backend/payroll_system/api/managers.py`.

5. Harden policy APIs.
   - Bind company from the URL and authenticated owner.
   - Prevent cross-company create/update.
   - Make default switching transactional.
   - Prevent leaving a company without an active default.
   - Make system-policy behavior immutable.
   - Validate `SELECTED_HEADS` has at least one head.
   - Return clean validation errors for duplicate day types/priorities.

6. Add salary OT preview API.
   - Both preview and save must call the same calculator.
   - Return effective policy and Regular/WO/HD breakdown.
   - Recalculate before persistence.
   - Wrap salary aggregate, breakdown, earnings, ESI, and repayments atomically.

7. Rewrite earned-salary reverse calculation.
   - Add authentication and company/employee authorization.
   - Support policy eligibility, selected heads, arbitrary multipliers, and daily salaries.
   - Create categorized attendance OT details.
   - Return a clear error when no eligible date can receive OT.
   - File: `backend/payroll_system/api/services/calculate_ot_attendance_using_earned_salary.py`

8. Update reports.
   - Daily OT report must use categorized OT and shared calculations.
   - Monthly OT report must use saved prepared-salary breakdown snapshots.
   - Files:
     - `backend/payroll_system/api/reports/generate_overtime_sheet_daily.py`
     - `backend/payroll_system/api/reports/generate_overtime_sheet.py`

9. Add follow-up migrations/backfills.
   - Backfill existing attendance `ot_min` into categorized details where classification is unambiguous.
   - Report ambiguous records.
   - Decide how existing prepared salaries with amounts but no breakdown should be represented.
   - Do not rewrite migration `0050` if it has been applied anywhere.

## Policy UI And Menu

Add an owner-only setup screen with:

- Policy list and create/edit modal.
- Name, default, active status.
- Regular/WO/HD eligibility rows.
- Decimal multipliers.
- Late-deduction priorities.
- All Earnings/Selected Heads.
- Earnings-head multi-select.
- WO-only, HD-only, WO+HD, and All-days shortcuts.
- System-policy restrictions and inactive status.

Recommended files:

- `frontend/src/components/authentication/api/overtimePolicyApiSlice.js`
- `frontend/src/components/menu/MasterEntry/forms/OvertimePoliciesForm/OvertimePoliciesForm.jsx`
- `frontend/src/components/menu/MasterEntry/forms/OvertimePoliciesForm/OvertimePolicyModal.jsx`
- `frontend/src/components/menu/MasterEntry/forms/OvertimePoliciesForm/OvertimePolicySchema.js`

Add:

- Menu item under **Setup Entry**, beside `Calculations`.
- Route: `/home/master-entry/overtime-policies`
- Update:
  - `frontend/src/components/menu/SidebarData.js`
  - `frontend/src/components/App.tsx`
  - `frontend/src/components/authentication/api/apiSlice.js` tag types
- Add an owner-only route guard; hiding the menu alone is insufficient.

## Employee Configuration

The existing selector is incomplete:

- Remove visible legacy S/D and overtime-type controls.
- Resolve the summary from the currently selected policy or company default.
- Show eligible categories, multipliers, late priority, earnings basis, and selected heads.
- Handle policy loading/error states.
- Preserve an existing inactive assignment while preventing new inactive selections.

Files:

- `frontend/src/components/menu/MasterEntry/forms/EmployeeEntryForm/EmployeeSalaryDetail.jsx`
- `frontend/src/components/menu/MasterEntry/forms/EmployeeEntryForm/EmployeeEntryForm.jsx`
- `frontend/src/components/menu/MasterEntry/forms/EmployeeEntryForm/EmployeeEntrySchema.js`

## Time Updation

1. `TimeUpdationForm.jsx`
   - Submit categorized OT details, not only `otMin`.
   - Normalize manual duration-only entries.

2. `EditAttendance.jsx`
   - Remove hard-coded `no_overtime`, `all_days`, and `holiday_weekly_off` branches.
   - Use the resolved policy or preferably a backend preview.
   - Exclude compensation off.
   - Stop excluding daily employees from off-day eligibility.
   - Handle overnight splitting.

3. `AttendanceMonthDays.jsx`
   - Display/edit category and manual OT details.

4. `AttendanceHeader.jsx`
   - Add category/detail headings.

5. `AttendanceFooter.jsx`
   - Display Regular/WO/HD gross, late deduction, and net totals.

6. `TimeUpdationSchema.js`
   - Validate detail payloads.

7. `timeUpdationApiSlice.js`
   - Read and write OT details.

Backend-generated machine/import attendance must use the same detail service, otherwise manual and imported attendance will still disagree.

## Salary Preparation

1. `EditSalary.jsx`
   - Remove the legacy browser S/D formula.
   - Fetch backend OT preview.
   - Display Regular/WO/HD breakdown:
     - Gross minutes
     - Deducted late minutes
     - Net minutes
     - Multiplier
     - Eligible salary rate
     - Divisor
     - Amount

2. `salaryPreparationApiSlice.js`
   - Add preview endpoint.
   - Return prepared overtime breakdown.

3. `CalculateOtAttendanceusingEarnedSalary.jsx`
   - Preserve and display `overtimeBreakdown`.
   - Show the effective policy.

4. `InsertTotalEarnedModal.jsx`
   - Replace hard-coded OT documentation with resolved-policy information.

5. Verify aggregate consumers:
   - `Deductions.jsx`
   - `NetSalary.jsx`
   - `DeductionsForCalculateOtAttendanceUsingEarnedSalary.jsx`
   - `NetSalaryForCalculateOtAttendanceUsingEarnedSalary.jsx`

Ordinary salary earnings must remain unchanged; selected heads only affect the OT rate base.

## Testing And Rollout

Missing tests include:

- Legacy migration combinations.
- Default inheritance and explicit overrides.
- Arbitrary multipliers.
- Selected earnings heads.
- Holiday precedence and extra-off classification.
- Overnight splitting.
- Late-deduction priority.
- Daily/monthly formulas.
- Owner divisors and `REGULAR` `2x/26`.
- Cross-company API protection.
- Manual, machine, bulk, earned-salary, preview, and report parity.
- Historical salary snapshots remaining unchanged after policy edits.

## Recommended Order

1. Fix default resolution and policy API integrity.
2. Implement attendance OT detail service and backfill.
3. Rewrite the calculator around categorized details.
4. Migrate every attendance writer.
5. Add salary preview and atomic save.
6. Rewrite earned-salary and reports.
7. Build policy UI/menu.
8. Complete employee, Time Updation, and Salary Preparation UI.
9. Add regression tests and run one parallel payroll reconciliation.

## Rollout Decisions Needed

1. Confirm whether migration `0050` has been applied outside local development.
2. Decide what timezone defines payroll midnight, since the project currently uses UTC and has no company payroll-timezone field.
