######-- We made changes for daily wage employee transfer attendance logic after creating this file

### Overall Purpose

The function's primary role is to synchronize attendance data from an `OWNER` user account to a linked `REGULAR` user account for a specific company, month, and year. It doesn't just copy the data; it processes and transforms it based on a set of rules defined for the sub-user. The main goals of the transformation are to remove or cap overtime, handle special rules for female employees, and ensure the sub-user's attendance data is consistent with their specific settings, while preserving manual overrides.

### Key Models Involved

- **`EmployeeAttendance`**: The central model storing daily attendance records.
- **`OwnerToRegular`**: Defines the one-to-one link between an `OWNER` and a `REGULAR` user.
- **`SubUserOvertimeSettings`**: Stores rules that define the maximum overtime hours (`max_ot_hrs`) a sub-user can have on a specific date.
- **`SubUserMiscSettings`**: Contains miscellaneous settings, most notably `enable_female_max_punch_out` and `max_female_punch_out` time.
- **`EmployeeShifts`**: Provides the shift timings (start, end, lunch) for an employee on any given date.
- **`EmployeeProfessionalDetail`**: Used to identify an employee's weekly and extra off days.
- **`Holiday`**: Contains the list of company holidays.

---

### Processing Logic and Edge Cases

The function iterates through each attendance record of the `OWNER` user for the specified month and processes it to generate the corresponding record for the `REGULAR` user.

Here is a breakdown of the logic, structured by input scenarios and their outcomes.

#### 1. Initial State: No Attendance for REGULAR User

This is the simplest path where the function creates new records for the REGULAR user.

| Input Scenario (from OWNER's record)     | Output (for REGULAR user's new record)                                                                              | Explanation                                                                                                                         |
| :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Normal Workday, No OT**                | `machine_in`/`out` times are randomized within a small buffer around the shift start/end times. `ot_min` is `None`. | The function "naturalizes" the punch times, removing minor deviations but keeping the core attendance status.                       |
| **Normal Workday, with OT**              | `ot_min` is set to `None`. `machine_out` is adjusted to be near the shift's end time.                               | By default, all overtime is removed for the sub-user.                                                                               |
| **Attendance on a Weekly Off / Holiday** | `machine_in` and `machine_out` are set to `None`. `ot_min` is `None`.                                               | The function nullifies any work done on a day off, effectively preventing the sub-user from getting paid for it or accumulating OT. |
| **OWNER's `machine_in` is very early**   | The REGULAR user's `machine_in` is adjusted to be within a predefined buffer of the shift start time.               | This prevents the sub-user from getting credit for arriving excessively early.                                                      |

#### 2. Overtime Handling with `SubUserOvertimeSettings`

This logic applies when a `SubUserOvertimeSettings` record exists for the attendance date, allowing for controlled overtime.

| Input Scenario                   | Output (for REGULAR user)                                                                                                                            | Explanation                                                                                                                  |
| :------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **OWNER's OT > `max_ot_hrs`**    | `ot_min` is capped at `max_ot_hrs`. `machine_out` is recalculated and adjusted to reflect this capped overtime duration.                             | The sub-user is only credited with the maximum allowed overtime. The punch-out time is modified to match this cap.           |
| **OWNER's OT <= `max_ot_hrs`**   | `ot_min` is the same as the OWNER's. `machine_out` is mostly unchanged (unless other rules apply).                                                   | The sub-user gets full credit for their overtime since it's within the allowed limit.                                        |
| **OT on a Weekly Off / Holiday** | `ot_min` is capped at `max_ot_hrs`. The shift's `lunch_duration` is deducted from the calculated OT if the employee worked through the lunch period. | Overtime on days off is allowed but capped, and the system intelligently deducts the lunch break from the total OT duration. |

#### 3. Miscellaneous Settings (`SubUserMiscSettings`)

These are special rules that can override other calculations.

| Input Scenario                                                      | Output (for REGULAR user)                                                                      | Explanation                                                                                                                                                                         |
| :------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Employee is **Female** and `enable_female_max_punch_out` is `True`. | The `machine_out` time is capped at the `max_female_punch_out` time specified in the settings. | This is a compliance or safety feature to ensure female employees' punch-out times do not exceed a certain time of day. This cap is applied even if it reduces calculated overtime. |

#### 4. Handling of Existing & Manual Attendance Data

This is the most complex logic, dealing with cases where the REGULAR user already has attendance records, some of which might have been manually entered. The function aims to respect manual data while applying the transformation rules.

| Input Scenario                                                         | Output (for REGULAR user)                                                                                                                                                                                                                                                                                           | Explanation                                                                                                                                                                                                                       |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Existing record, no manual data**                                    | The record is updated with the newly calculated `machine_in`, `machine_out`, and `ot_min` based on the rules above.                                                                                                                                                                                                 | This is a standard update/synchronization.                                                                                                                                                                                        |
| **OWNER's record has `manual_mode = True`**                            | The `first_half` and `second_half` status (e.g., 'Present', 'Absent') and `manual_mode` flag are copied directly. `machine_in`/`out` and `ot_min` are still calculated and stored but do not influence the attendance status.                                                                                       | This preserves the exact attendance status (like 'On-Duty' or a specific leave type) that was manually set for the owner, treating it as an explicit override.                                                                    |
| **REGULAR user's existing record has `manual_in` or `manual_out` set** | The function recalculates the `first_half` and `second_half` status from scratch. It uses the manual time if present, otherwise falls back to the newly calculated machine time. The final status (`Present`, `Absent`, `Half-day`) is determined based on the total worked duration derived from this combination. | This logic respects the sub-user's manual entries. For instance, if a `manual_out` was entered, the system uses that time to determine if the employee completed a full or half day, ignoring the owner's original `machine_out`. |
| **REGULAR user's existing record has `manual_mode = True`**            | The record is left untouched. The `ot_min` and `late_min` are copied from the owner's record, but the core attendance data is not modified.                                                                                                                                                                         | The system assumes that a record in full `manual_mode` for the sub-user is a deliberate entry that should not be overwritten by the synchronization process.                                                                      |

#### 5. Final Step: Record Updates

After iterating through all attendance records, the function performs `bulk_create` and `bulk_update` operations for efficiency. Finally, it calls `generate_update_monthly_record` for each affected employee to ensure their monthly summary reports are accurate.
