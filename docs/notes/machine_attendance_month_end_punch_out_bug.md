# Machine Attendance Bug: Month-End Punch-Out After Midnight Was Dropped

## Summary

`machine_attendance` was dropping a valid punch-out if:

- the employee is processed for the last day of a date range or month,
- the shift is a normal same-day shift such as `09:30` to `18:00`,
- the employee punches out after `12:00 AM` on the next calendar day.

In the reproduced case, the employee was marked as `MS` / miss punch even though the next-day punch-out existed in the machine data.

## Reproduced Case

- Shift: `09:30` to `18:00`
- Attendance date: `2024-01-31`
- Machine in: `2024-01-31 09:30:00`
- Machine out: `2024-02-01 00:30:00`
- `from_date = 2024-01-31 00:00:00`
- `to_date = 2024-01-31 00:00:00`

## Original Broken Output

Original `EmployeeAttendance` result before the fix:

- `machine_in = 09:30`
- `machine_out = None`
- `first_half = MS`
- `second_half = MS`
- `late_min = None`
- `pay_multiplier = 0.0`

Observed manager debug output during the test:

```text
From Date: 2024-01-31 00:00:00 End Date: 2024-01-31 00:00:00
Current Employee ACN: 117
The USERID for Badgenumber is: 5017
Current Date of loop 2024-01-31 00:00:00
Machine Out: None Machine In: 2024-01-31 09:30:00 Punch In: 2024-01-31 09:30:00 Punch Out: None
Punch in time : 2024-01-31 09:30:00 Punch out time : None, Employee: Employee E017
date: 2024-01-31 00:00:00 Late Minutes Integer: 0 Late Min: 0:00:00
```

## Expected Behavior

The next-day punch-out should still be considered for the previous day's attendance when it falls within the allowed punch window for that shift. In this reproduced case, `00:30` should not be silently discarded before attendance calculation.

## Root Cause

The bug starts in the MDB row filtering in:

- [backend/payroll_system/api/managers.py](/home/naruto/kaushal/payper/payroll-system/backend/payroll_system/api/managers.py:374)

Original filter:

```python
filtered_rows = df[
    (df['CHECKTIME'] >= (from_date - relativedelta(days=1))) &
    (df['CHECKTIME'] <= (to_date + relativedelta(days=1)))
]
```

If `to_date` is `2024-01-31 00:00:00`, then the upper bound becomes `2024-02-01 00:00:00`.

That means:

- `2024-02-01 00:00:00` is included
- `2024-02-01 00:30:00` is excluded

So the punch-out is lost before shift resolution and punch pairing logic run.

## Impact

- Late exits after midnight on the last processed day are undercounted.
- Employees can be incorrectly marked as `MS`.
- OT can be lost because there is no punch-out left to evaluate.
- Month-end attendance can be wrong even when the machine data is correct.

## Solution Options

### Option 1: Widen The Coarse Import Window

Keep the current structure, but widen the initial MDB dataframe filter so it includes the full extra next day instead of stopping at midnight.

Implementation shape:

- use `< to_date + 2 days` instead of `<= to_date + 1 day`

Pros:

- minimal code change
- fixes the reproduced bug
- works with the existing shift-window logic later in the method

Cons:

- still relies on a coarse global prefilter
- less robust than a fully shift-window-driven design

### Option 2: Make Shift Windows The Source Of Truth

Do not use a midnight datetime as the upper bound for next-day punch capture.

Keep only a broad raw import range, then assign punches using the per-attendance shift boundaries already computed later in the method.

Pros:

- more domain-correct
- better for overnight shifts and edge windows
- reduces hidden date-boundary assumptions

Cons:

- larger refactor
- higher regression risk

## Chosen Fix

We implemented **Option 1**.

Updated code:

- [backend/payroll_system/api/managers.py](/home/naruto/kaushal/payper/payroll-system/backend/payroll_system/api/managers.py:374)

New filter:

```python
filtered_rows = df[
    (df['CHECKTIME'] >= (from_date - relativedelta(days=1))) &
    (df['CHECKTIME'] < (to_date + relativedelta(days=2)))
]
```

This preserves `2024-02-01 00:30:00` for the `2024-01-31` attendance run while still leaving the later per-shift punch-window logic in control of which punch is used.

## Output After Fix

Updated `EmployeeAttendance` result for the same reproduced case:

- `machine_in = 09:30`
- `machine_out = 00:30`
- `first_half = P`
- `second_half = P`
- `ot_min = 360`
- `late_min = None`
- `pay_multiplier = 1.0`

## Regression Test

Regression test in:

- [backend/payroll_system/api/tests.py](/home/naruto/kaushal/payper/payroll-system/backend/payroll_system/api/tests.py:561)

Test name:

- `test_machine_attendance_keeps_month_end_punch_out_after_midnight_for_normal_shift`

The test now asserts the corrected behavior under Option 1.

## Status

- Bug documented
- Both solution options recorded
- Fix implemented with Option 1
- Regression test updated and passing
- Option 2 remains the stronger long-term design
