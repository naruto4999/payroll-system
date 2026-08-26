from datetime import date, time
from decimal import Decimal

from api.models import (
    Company,
    EarningsHead,
    EmployeeAttendance,
    EmployeeAttendanceOvertimeDetail,
    EmployeePersonalDetail,
    EmployeeProfessionalDetail,
    EmployeeSalaryEarning,
    EmployeeSalaryDetail,
    EmployeeSalaryPrepared,
    EmployeeSalaryPreparedOvertimeDetail,
    EmployeeShifts,
    Holiday,
    LeaveGrade,
    OvertimePolicy,
    OvertimePolicyDayRule,
    OvertimePolicyEarningsHead,
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
        overtime_rate=None,
        overtime_policy=None,
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
            overtime_rate=overtime_rate or ("S" if overtime_type != "no_overtime" else None),
            overtime_policy=overtime_policy,
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

    def create_overtime_policy(
        self,
        *,
        code="CUSTOM_POLICY",
        name="Custom policy",
        rules=(("REGULAR", "1"),),
        earnings_basis=OvertimePolicy.EARNINGS_BASIS_ALL,
        selected_heads=(),
        is_default=False,
        is_active=True,
        rounding_increment_minutes=30,
        round_up_from_minutes=16,
    ):
        policy = OvertimePolicy.objects.create(
            company=self.company,
            code=code,
            name=name,
            earnings_basis=earnings_basis,
            is_default=is_default,
            is_active=is_active,
            rounding_increment_minutes=rounding_increment_minutes,
            round_up_from_minutes=round_up_from_minutes,
        )
        for priority, (day_type, multiplier) in enumerate(rules, start=1):
            OvertimePolicyDayRule.objects.create(
                policy=policy,
                day_type=day_type,
                multiplier=Decimal(multiplier),
                late_deduction_priority=priority,
            )
        for earnings_head in selected_heads:
            OvertimePolicyEarningsHead.objects.create(policy=policy, earnings_head=earnings_head)
        return policy

    def assign_overtime_policy(self, employee, policy):
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.overtime_policy = policy
        salary_detail.save(update_fields=["overtime_policy"])
        return salary_detail

    def create_salary_earning(self, employee, *, name="Basic", value=20800):
        earnings_head, _ = EarningsHead.objects.get_or_create(
            user=self.user,
            company=self.company,
            name=name,
            defaults={"mandatory_earning": False},
        )
        return EmployeeSalaryEarning.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            earnings_head=earnings_head,
            value=value,
            from_date=date(2024, 1, 1),
            to_date=date(2099, 1, 1),
        )

    def create_attendance(self, employee, *, work_date=date(2024, 1, 2), ot_min=None, late_min=None):
        return EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=work_date,
            first_half=self.leave_present,
            second_half=self.leave_present,
            ot_min=ot_min,
            late_min=late_min,
        )

    def create_overtime_detail(
        self,
        attendance,
        *,
        minutes=30,
        day_type="REGULAR",
        source="MANUAL",
        work_date=None,
        excluded_minutes=0,
        exclusion_reason="NONE",
        exclusion_note="",
    ):
        return EmployeeAttendanceOvertimeDetail.objects.create(
            attendance=attendance,
            work_date=work_date or attendance.date,
            day_type=day_type,
            source=source,
            gross_minutes=minutes,
            excluded_minutes=excluded_minutes,
            eligible_minutes=minutes - excluded_minutes,
            exclusion_reason=exclusion_reason,
            exclusion_note=exclusion_note,
        )

    def create_prepared_salary(
        self,
        employee,
        *,
        period=date(2024, 1, 1),
        net_minutes=0,
        amount=0,
    ):
        return EmployeeSalaryPrepared.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=period,
            net_ot_minutes_monthly=net_minutes,
            net_ot_amount_monthly=amount,
        )

    def create_prepared_overtime_detail(
        self,
        salary,
        *,
        day_type="REGULAR",
        gross_minutes=30,
        deducted_late_minutes=0,
        net_minutes=30,
        multiplier="1",
        eligible_salary_rate="20800",
        divisor="26",
        amount=50,
    ):
        return EmployeeSalaryPreparedOvertimeDetail.objects.create(
            salary_prepared=salary,
            day_type=day_type,
            gross_minutes=gross_minutes,
            deducted_late_minutes=deducted_late_minutes,
            net_minutes=net_minutes,
            multiplier=Decimal(multiplier),
            eligible_salary_rate=Decimal(eligible_salary_rate),
            divisor=Decimal(divisor),
            amount=amount,
        )

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
