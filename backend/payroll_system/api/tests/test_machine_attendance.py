from datetime import date, datetime, time
from io import BytesIO
from unittest.mock import patch

import pandas as pd
from django.test import TestCase

from api.models import EmployeeAttendance, EmployeeShifts, Shift
from api.tests.base import AttendanceTestDataMixin


class MachineAttendanceManagerTests(AttendanceTestDataMixin, TestCase):
    def build_mdb_side_effect(self, checkinout_rows, userinfo_rows):
        checkinout_df = pd.DataFrame(checkinout_rows, columns=["USERID", "CHECKTIME"])
        userinfo_df = pd.DataFrame(userinfo_rows, columns=["USERID", "Badgenumber"])

        def side_effect(_path, table_name):
            if table_name == "CHECKINOUT":
                return checkinout_df.copy()
            if table_name == "USERINFO":
                return userinfo_df.copy()
            raise AssertionError(f"Unexpected table requested: {table_name}")

        return side_effect

    def run_machine_attendance(self, *, from_date, to_date, employee, checkinout_rows, userinfo_rows):
        fake_mdb = BytesIO(b"fake-mdb")
        with patch("api.managers.mdb.read_table", side_effect=self.build_mdb_side_effect(checkinout_rows, userinfo_rows)):
            with patch("api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record"):
                return EmployeeAttendance.objects.machine_attendance(
                    from_date=from_date,
                    to_date=to_date,
                    company_id=self.company.id,
                    user=self.user,
                    all_employees_machine_attendance=False,
                    mdb_database=fake_mdb,
                    employee=employee.id,
                )

    def test_machine_attendance_marks_full_day_present_and_computes_late_minutes(self):
        employee = self.create_employee()
        target_date = datetime(2024, 1, 3)

        success, message = self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5001, "01/03/24 09:20:00"],
                [5001, "01/03/24 17:40:00"],
            ],
            userinfo_rows=[
                [5001, str(employee.attendance_card_no)],
            ],
        )

        self.assertTrue(success)
        self.assertEqual(message, "Operation successful")

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.machine_in, time(9, 20))
        self.assertEqual(attendance.machine_out, time(17, 40))
        self.assertEqual(attendance.first_half, self.leave_present)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertEqual(attendance.late_min, 20)
        self.assertEqual(attendance.ot_min, 30)
        self.assertEqual(float(attendance.pay_multiplier), 1.0)

    def test_machine_attendance_marks_miss_punch_when_only_one_punch_exists(self):
        employee = self.create_employee(paycode="E002", attendance_card_no=102)
        target_date = datetime(2024, 1, 4)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[[5002, "01/04/24 09:10:00"]],
            userinfo_rows=[[5002, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.machine_in, time(9, 10))
        self.assertIsNone(attendance.machine_out)
        self.assertEqual(attendance.first_half, self.leave_miss_punch)
        self.assertEqual(attendance.second_half, self.leave_miss_punch)
        self.assertEqual(float(attendance.pay_multiplier), 0.0)

    def test_machine_attendance_preserves_manual_mode_records(self):
        employee = self.create_employee(paycode="E003", attendance_card_no=103)
        target_date = date(2024, 1, 5)

        attendance = EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=target_date,
            manual_in=time(10, 0),
            manual_out=time(18, 0),
            first_half=self.leave_absent,
            second_half=self.leave_present,
            manual_mode=True,
        )

        self.run_machine_attendance(
            from_date=datetime.combine(target_date, time.min),
            to_date=datetime.combine(target_date, time.min),
            employee=employee,
            checkinout_rows=[
                [5003, "01/05/24 09:00:00"],
                [5003, "01/05/24 17:00:00"],
            ],
            userinfo_rows=[[5003, str(employee.attendance_card_no)]],
        )

        attendance.refresh_from_db()
        self.assertEqual(attendance.manual_in, time(10, 0))
        self.assertEqual(attendance.manual_out, time(18, 0))
        self.assertEqual(attendance.first_half, self.leave_absent)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertTrue(attendance.manual_mode)

    def test_machine_attendance_marks_half_day_when_work_minutes_cross_half_day_threshold(self):
        employee = self.create_employee(paycode="E006", attendance_card_no=106, overtime_type="no_overtime")
        target_date = datetime(2024, 1, 8)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5006, "01/08/24 09:20:00"],
                [5006, "01/08/24 13:50:00"],
            ],
            userinfo_rows=[[5006, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_present)
        self.assertEqual(attendance.second_half, self.leave_absent)
        self.assertEqual(attendance.late_min, 20)
        self.assertIsNone(attendance.ot_min)
        self.assertEqual(float(attendance.pay_multiplier), 0.5)

    def test_machine_attendance_marks_absent_present_when_late_exceeds_max_allowed(self):
        employee = self.create_employee(paycode="E007", attendance_card_no=107, overtime_type="no_overtime")
        target_date = datetime(2024, 1, 9)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5007, "01/09/24 10:10:00"],
                [5007, "01/09/24 18:30:00"],
            ],
            userinfo_rows=[[5007, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_absent)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertIsNone(attendance.late_min)
        self.assertEqual(float(attendance.pay_multiplier), 0.5)

    def test_machine_attendance_ignores_regular_day_overtime_for_holiday_weekly_off_mode(self):
        employee = self.create_employee(
            paycode="E008",
            attendance_card_no=108,
            overtime_type="holiday_weekly_off",
        )
        target_date = datetime(2024, 1, 10)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5008, "01/10/24 08:00:00"],
                [5008, "01/10/24 18:30:00"],
            ],
            userinfo_rows=[[5008, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_present)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertIsNone(attendance.ot_min)

    def test_machine_attendance_marks_paid_weekly_off_when_threshold_is_met(self):
        employee = self.create_employee(
            paycode="E009",
            attendance_card_no=109,
            overtime_type="holiday_weekly_off",
            weekly_off="sun",
        )
        target_date = datetime(2024, 1, 7)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5009, "01/07/24 09:00:00"],
                [5009, "01/07/24 18:00:00"],
            ],
            userinfo_rows=[[5009, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_weekly_off)
        self.assertEqual(attendance.second_half, self.leave_weekly_off)
        self.assertEqual(attendance.ot_min, 510)
        self.assertEqual(float(attendance.pay_multiplier), 1.0)

    def test_machine_attendance_marks_unpaid_weekly_off_when_threshold_is_not_met(self):
        employee = self.create_employee(
            paycode="E010",
            attendance_card_no=110,
            overtime_type="no_overtime",
            weekly_off="sun",
        )
        self.set_weekly_off_thresholds(weekly_days=3, holiday_days=3)
        target_date = datetime(2024, 1, 7)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[],
            userinfo_rows=[[5010, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_weekly_off_skip)
        self.assertEqual(attendance.second_half, self.leave_weekly_off_skip)
        self.assertEqual(float(attendance.pay_multiplier), 0.0)

    def test_machine_attendance_marks_paid_holiday_and_keeps_holiday_overtime(self):
        employee = self.create_employee(
            paycode="E011",
            attendance_card_no=111,
            overtime_type="holiday_weekly_off",
        )
        target_date = datetime(2024, 1, 11)
        self.create_holiday(holiday_date=target_date.date(), name="Founders Day")

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5011, "01/11/24 09:00:00"],
                [5011, "01/11/24 18:00:00"],
            ],
            userinfo_rows=[[5011, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_holiday_off)
        self.assertEqual(attendance.second_half, self.leave_holiday_off)
        self.assertEqual(attendance.ot_min, 510)
        self.assertEqual(float(attendance.pay_multiplier), 1.0)

    def test_machine_attendance_keeps_daily_wage_employee_absent_without_punches_on_weekly_off(self):
        employee = self.create_employee(
            paycode="E012",
            attendance_card_no=112,
            salary_mode="daily",
            overtime_type="holiday_weekly_off",
            weekly_off="sun",
        )
        target_date = datetime(2024, 1, 7)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[],
            userinfo_rows=[[5012, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.first_half, self.leave_absent)
        self.assertEqual(attendance.second_half, self.leave_absent)
        self.assertEqual(float(attendance.pay_multiplier), 0.0)

    def test_machine_attendance_updates_existing_non_manual_record(self):
        employee = self.create_employee(paycode="E013", attendance_card_no=113, overtime_type="no_overtime")
        target_date = date(2024, 1, 12)
        attendance = EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=target_date,
            first_half=self.leave_absent,
            second_half=self.leave_absent,
            machine_in=None,
            machine_out=None,
        )

        self.run_machine_attendance(
            from_date=datetime.combine(target_date, time.min),
            to_date=datetime.combine(target_date, time.min),
            employee=employee,
            checkinout_rows=[
                [5013, "01/12/24 09:00:00"],
                [5013, "01/12/24 17:00:00"],
            ],
            userinfo_rows=[[5013, str(employee.attendance_card_no)]],
        )

        attendance.refresh_from_db()
        self.assertEqual(attendance.machine_in, time(9, 0))
        self.assertEqual(attendance.machine_out, time(17, 0))
        self.assertEqual(attendance.first_half, self.leave_present)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertEqual(float(attendance.pay_multiplier), 1.0)

    def test_machine_attendance_skips_days_before_joining_date(self):
        employee = self.create_employee(
            paycode="E014",
            attendance_card_no=114,
            overtime_type="no_overtime",
            date_of_joining=date(2024, 1, 15),
        )

        self.run_machine_attendance(
            from_date=datetime(2024, 1, 14),
            to_date=datetime(2024, 1, 16),
            employee=employee,
            checkinout_rows=[
                [5014, "01/14/24 09:00:00"],
                [5014, "01/14/24 17:00:00"],
                [5014, "01/15/24 09:00:00"],
                [5014, "01/15/24 17:00:00"],
                [5014, "01/16/24 09:00:00"],
                [5014, "01/16/24 17:00:00"],
            ],
            userinfo_rows=[[5014, str(employee.attendance_card_no)]],
        )

        self.assertFalse(EmployeeAttendance.objects.filter(employee=employee, date=date(2024, 1, 14), user=self.user).exists())
        self.assertTrue(EmployeeAttendance.objects.filter(employee=employee, date=date(2024, 1, 15), user=self.user).exists())
        self.assertTrue(EmployeeAttendance.objects.filter(employee=employee, date=date(2024, 1, 16), user=self.user).exists())

    def test_machine_attendance_marks_miss_punch_when_punch_in_is_after_half_day_cutoff(self):
        employee = self.create_employee(paycode="E015", attendance_card_no=115, overtime_type="no_overtime")
        target_date = datetime(2024, 1, 13)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5015, "01/13/24 14:00:00"],
                [5015, "01/13/24 17:00:00"],
            ],
            userinfo_rows=[[5015, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertIsNone(attendance.machine_in)
        self.assertEqual(attendance.machine_out, time(17, 0))
        self.assertEqual(attendance.first_half, self.leave_miss_punch)
        self.assertEqual(attendance.second_half, self.leave_miss_punch)

    def test_machine_attendance_currently_keeps_weekly_off_status_for_overnight_shift_with_next_day_punch_out(self):
        overnight_shift = Shift.objects.create(
            user=self.user,
            company=self.company,
            name="Night",
            beginning_time=time(22, 0),
            end_time=time(6, 0),
            lunch_duration=30,
            lunch_beginning_time=time(2, 0),
            tea_time=0,
            late_grace=15,
            ot_begin_after=30,
            next_shift_delay=0,
            max_late_allowed_min=60,
            accidental_punch_buffer=0,
            half_day_minimum_minutes=240,
            full_day_minimum_minutes=480,
            short_leaves=0,
        )
        employee = self.create_employee(paycode="E016", attendance_card_no=116, overtime_type="no_overtime")
        EmployeeShifts.objects.filter(employee=employee).delete()
        EmployeeShifts.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            shift=overnight_shift,
            from_date=date(2024, 1, 1),
            to_date=date(2099, 12, 31),
        )
        target_date = datetime(2024, 1, 14)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5016, "01/14/24 21:30:00"],
                [5016, "01/15/24 06:30:00"],
            ],
            userinfo_rows=[[5016, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.machine_in, time(21, 30))
        self.assertEqual(attendance.machine_out, time(6, 30))
        self.assertEqual(attendance.first_half, self.leave_weekly_off)
        self.assertEqual(attendance.second_half, self.leave_weekly_off)

    def test_machine_attendance_keeps_month_end_punch_out_after_midnight_for_normal_shift(self):
        late_shift = Shift.objects.create(
            user=self.user,
            company=self.company,
            name="Late Day",
            beginning_time=time(9, 30),
            end_time=time(18, 0),
            lunch_duration=30,
            lunch_beginning_time=time(13, 0),
            tea_time=0,
            late_grace=15,
            ot_begin_after=30,
            next_shift_delay=0,
            max_late_allowed_min=60,
            accidental_punch_buffer=0,
            half_day_minimum_minutes=240,
            full_day_minimum_minutes=480,
            short_leaves=0,
        )
        employee = self.create_employee(paycode="E017", attendance_card_no=117, overtime_type="all_days")
        EmployeeShifts.objects.filter(employee=employee).delete()
        EmployeeShifts.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            shift=late_shift,
            from_date=date(2024, 1, 1),
            to_date=date(2099, 12, 31),
        )
        target_date = datetime(2024, 1, 31)

        self.run_machine_attendance(
            from_date=target_date,
            to_date=target_date,
            employee=employee,
            checkinout_rows=[
                [5017, "01/31/24 09:30:00"],
                [5017, "02/01/24 00:30:00"],
            ],
            userinfo_rows=[[5017, str(employee.attendance_card_no)]],
        )

        attendance = EmployeeAttendance.objects.get(employee=employee, date=target_date.date(), user=self.user)
        self.assertEqual(attendance.machine_in, time(9, 30))
        self.assertEqual(attendance.machine_out, time(0, 30))
        self.assertEqual(attendance.first_half, self.leave_present)
        self.assertEqual(attendance.second_half, self.leave_present)
        self.assertEqual(attendance.ot_min, 390)
        self.assertEqual(float(attendance.pay_multiplier), 1.0)

