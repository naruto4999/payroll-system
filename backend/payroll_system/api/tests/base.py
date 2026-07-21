from datetime import date, time

from api.models import (
    Company,
    EmployeePersonalDetail,
    EmployeeProfessionalDetail,
    EmployeeSalaryDetail,
    EmployeeShifts,
    Holiday,
    LeaveGrade,
    Shift,
    User,
    WeeklyOffHolidayOff,
)


class AttendanceTestDataMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password",
            phone_no=9999999999,
        )
        cls.company = Company.objects.create(user=cls.user, name="Acme")

        cls.leave_present = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="P")
        cls.leave_absent = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="A")
        cls.leave_miss_punch = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="MS")
        cls.leave_weekly_off = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="WO")
        cls.leave_weekly_off_skip = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="WO*")
        cls.leave_holiday_off = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="HD")
        cls.leave_holiday_off_skip = LeaveGrade.objects.get(user=cls.user, company=cls.company, name="HD*")

        weekly_off_config = WeeklyOffHolidayOff.objects.get(user=cls.user, company=cls.company)
        weekly_off_config.min_days_for_weekly_off = 0
        weekly_off_config.min_days_for_holiday_off = 0
        weekly_off_config.save(update_fields=["min_days_for_weekly_off", "min_days_for_holiday_off"])

        cls.shift = Shift.objects.create(
            user=cls.user,
            company=cls.company,
            name="General",
            beginning_time=time(9, 0),
            end_time=time(17, 0),
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

    def create_employee(
        self,
        *,
        paycode="E001",
        attendance_card_no=101,
        salary_mode="monthly",
        overtime_type="all_days",
        weekly_off="sun",
        extra_off="no_off",
        date_of_joining=date(2024, 1, 1),
    ):
        employee = EmployeePersonalDetail.objects.create(
            user=self.user,
            company=self.company,
            name=f"Employee {paycode}",
            paycode=paycode,
            attendance_card_no=attendance_card_no,
            gender="M",
        )
        EmployeeProfessionalDetail.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date_of_joining=date_of_joining,
            date_of_confirm=date_of_joining,
            weekly_off=weekly_off,
            extra_off=extra_off,
            resigned=False,
        )
        EmployeeSalaryDetail.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            salary_mode=salary_mode,
            overtime_type=overtime_type,
            overtime_rate="S" if overtime_type != "no_overtime" else None,
        )
        EmployeeShifts.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            shift=self.shift,
            from_date=date_of_joining,
            to_date=date(2099, 12, 31),
        )
        return employee

    def set_weekly_off_thresholds(self, *, weekly_days, holiday_days):
        weekly_off_config = WeeklyOffHolidayOff.objects.get(user=self.user, company=self.company)
        weekly_off_config.min_days_for_weekly_off = weekly_days
        weekly_off_config.min_days_for_holiday_off = holiday_days
        weekly_off_config.save(update_fields=["min_days_for_weekly_off", "min_days_for_holiday_off"])

    def create_holiday(self, *, holiday_date, name):
        return Holiday.objects.create(
            user=self.user,
            company=self.company,
            name=name,
            date=holiday_date,
            mandatory_holiday=False,
        )

