from datetime import date
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient

from api.models import (
    EarnedAmount,
    EarningsHead,
    EmployeeAdvanceEmiRepayment,
    EmployeeAdvancePayment,
    EmployeeMonthlyAttendanceDetails,
    EmployeePfEsiDetail,
    EmployeeSalaryPrepared,
    EmployeeSalaryPreparedOvertimeDetail,
    OvertimePolicy,
)
from api.services.salary_preparation import prepare_employee_salary
from api.tests.base import AttendanceTestDataMixin


class PhaseSixSalaryPreparationTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee()
        self.earning = self.create_salary_earning(self.employee)
        self.employee_pf_esi = EmployeePfEsiDetail.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            esi_allow=True,
            esi_on_ot=True,
            vpf_amount=150,
            tds_amount=200,
        )
        self.monthly = EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 1),
            paid_days_count=62,
        )
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')
        self.assign_overtime_policy(self.employee, policy)
        attendance = self.create_attendance(self.employee, work_date=date(2024, 1, 2))
        self.create_overtime_detail(attendance, minutes=60)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def preview_payload(self):
        return {
            'company': self.company.pk,
            'employee': self.employee.pk,
            'year': 2024,
            'month': 1,
        }

    def salary_preview_payload(self, **overrides):
        payload = {
            **self.preview_payload(),
            'incentive_amount': 0,
            'advance_deducted': 0,
            'others_deducted': 0,
            'arrears': [],
        }
        payload.update(overrides)
        return payload

    def salary_payload(self, **parent_overrides):
        parent = {
            'company': self.company.pk,
            'employee': self.employee.pk,
            'date': '2024-01-01',
            'incentive_amount': 0,
            'advance_deducted': 0,
            'others_deducted': 0,
        }
        parent.update(parent_overrides)
        return {
            'employee_salary_prepared': parent,
            'all_earned_amounts': [{
                'earnings_head': {'id': self.earning.earnings_head_id},
                'rate': self.earning.value,
                'earned_amount': self.earning.value,
                'arear_amount': 0,
            }],
        }

    def test_preview_is_authenticated_scoped_and_no_write(self):
        anonymous = APIClient().post('/api/salary-overtime/preview', self.preview_payload(), format='json')
        self.assertEqual(anonymous.status_code, 401)

        before = (
            EmployeeSalaryPrepared.objects.count(),
            EarnedAmount.objects.count(),
            EmployeeSalaryPreparedOvertimeDetail.objects.count(),
            EmployeeAdvanceEmiRepayment.objects.count(),
        )
        response = self.client.post('/api/salary-overtime/preview', self.preview_payload(), format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data['breakdown']), 3)
        self.assertEqual(response.data['totals']['amount'], '200')
        self.assertIsInstance(response.data['breakdown'][0]['multiplier'], str)
        self.assertEqual(before, (
            EmployeeSalaryPrepared.objects.count(),
            EarnedAmount.objects.count(),
            EmployeeSalaryPreparedOvertimeDetail.objects.count(),
            EmployeeAdvanceEmiRepayment.objects.count(),
        ))

    def test_preview_and_save_match_and_esi_uses_server_overtime(self):
        preview = self.client.post('/api/salary-overtime/preview', self.preview_payload(), format='json')
        response = self.client.post('/api/employee-salary-prepared', self.salary_payload(), format='json')
        self.assertEqual(response.status_code, 200, response.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee, date=date(2024, 1, 1))
        self.assertEqual(salary.net_ot_minutes_monthly, preview.data['totals']['net_minutes'])
        self.assertEqual(str(salary.net_ot_amount_monthly), preview.data['totals']['amount'])
        self.assertEqual(salary.esi_deducted, 158)
        self.assertEqual(
            salary.net_ot_minutes_monthly,
            sum(salary.overtime_breakdown.values_list('net_minutes', flat=True)),
        )
        self.assertEqual(
            salary.net_ot_amount_monthly,
            sum(salary.overtime_breakdown.values_list('amount', flat=True)),
        )
        self.assertIn('salary', response.data)
        self.assertIn('overtime', response.data)

    def test_full_salary_preview_has_no_writes(self):
        EmployeeAdvancePayment.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            principal=100,
            emi=25,
            date=date(2023, 12, 1),
            tenure_months_left=4,
        )
        before = (
            EmployeeSalaryPrepared.objects.count(),
            EarnedAmount.objects.count(),
            EmployeeSalaryPreparedOvertimeDetail.objects.count(),
            EmployeeAdvanceEmiRepayment.objects.count(),
        )
        response = self.client.post(
            '/api/salary-preparation/preview',
            self.salary_preview_payload(
                incentive_amount=500,
                advance_deducted=None,
                others_deducted=100,
                arrears=[{'earnings_head': self.earning.earnings_head_id, 'arear_amount': 250}],
            ),
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['salary']['earned_amounts'][0]['earned_amount'], self.earning.value + 250)
        self.assertEqual(response.data['salary']['earned_amounts'][0]['arear_amount'], 250)
        self.assertEqual(response.data['salary']['advance_deducted'], 25)
        self.assertIn('net_salary', response.data['salary'])
        self.assertEqual(before, (
            EmployeeSalaryPrepared.objects.count(),
            EarnedAmount.objects.count(),
            EmployeeSalaryPreparedOvertimeDetail.objects.count(),
            EmployeeAdvanceEmiRepayment.objects.count(),
        ))

    def test_full_salary_preview_matches_saved_salary(self):
        preview = self.client.post(
            '/api/salary-preparation/preview',
            self.salary_preview_payload(
                incentive_amount=500,
                others_deducted=100,
                arrears=[{'earnings_head': self.earning.earnings_head_id, 'arear_amount': 250}],
            ),
            format='json',
        )
        self.assertEqual(preview.status_code, 200, preview.data)
        preview_salary = preview.data['salary']
        payload = self.salary_payload(incentive_amount=500, others_deducted=100)
        payload['all_earned_amounts'] = [{
            'earnings_head': {'id': row['earnings_head']['id']},
            'rate': row['rate'],
            'earned_amount': row['earned_amount'],
            'arear_amount': row['arear_amount'],
        } for row in preview_salary['earned_amounts']]
        saved = self.client.post('/api/employee-salary-prepared', payload, format='json')
        self.assertEqual(saved.status_code, 200, saved.data)
        self.assertEqual(str(saved.data['salary']['net_salary']), str(preview_salary['net_salary']))
        for field in (
            'incentive_amount',
            'pf_deducted',
            'esi_deducted',
            'vpf_deducted',
            'advance_deducted',
            'tds_deducted',
            'labour_welfare_fund_deducted',
            'others_deducted',
            'net_ot_minutes_monthly',
            'net_ot_amount_monthly',
        ):
            self.assertEqual(str(saved.data['salary'][field]), str(preview_salary[field]))

    def test_manual_vpf_and_tds_override_configuration_defaults(self):
        default_preview = self.client.post(
            '/api/salary-preparation/preview',
            self.salary_preview_payload(vpf_deducted=None, tds_deducted=None),
            format='json',
        )
        self.assertEqual(default_preview.status_code, 200, default_preview.data)
        self.assertEqual(default_preview.data['salary']['vpf_deducted'], 150)
        self.assertEqual(default_preview.data['salary']['tds_deducted'], 200)

        override_preview = self.client.post(
            '/api/salary-preparation/preview',
            self.salary_preview_payload(vpf_deducted=325, tds_deducted=475),
            format='json',
        )
        self.assertEqual(override_preview.status_code, 200, override_preview.data)
        preview_salary = override_preview.data['salary']
        self.assertEqual(preview_salary['vpf_deducted'], 325)
        self.assertEqual(preview_salary['tds_deducted'], 475)

        payload = self.salary_payload(vpf_deducted=325, tds_deducted=475)
        payload['all_earned_amounts'] = [{
            'earnings_head': {'id': row['earnings_head']['id']},
            'rate': row['rate'],
            'earned_amount': row['earned_amount'],
            'arear_amount': row['arear_amount'],
        } for row in preview_salary['earned_amounts']]
        saved = self.client.post('/api/employee-salary-prepared', payload, format='json')
        self.assertEqual(saved.status_code, 200, saved.data)
        self.assertEqual(saved.data['salary']['vpf_deducted'], 325)
        self.assertEqual(saved.data['salary']['tds_deducted'], 475)
        self.assertEqual(str(saved.data['salary']['net_salary']), str(preview_salary['net_salary']))

    def test_bulk_replaces_manual_vpf_and_tds_with_configuration_defaults(self):
        manual = self.client.post(
            '/api/employee-salary-prepared',
            self.salary_payload(vpf_deducted=325, tds_deducted=475),
            format='json',
        )
        self.assertEqual(manual.status_code, 200, manual.data)

        bulk = self.client.post('/api/employee-bulk-salary-prepared', {
            'company': self.company.pk,
            'year': 2024,
            'month': 1,
            'employee_ids': [self.employee.pk],
        }, format='json')
        self.assertEqual(bulk.status_code, 200, bulk.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee)
        self.assertEqual(salary.vpf_deducted, 150)
        self.assertEqual(salary.tds_deducted, 200)

    def test_client_overtime_totals_are_rejected_without_writes(self):
        payload = self.salary_payload(net_ot_minutes_monthly=999, net_ot_amount_monthly=999)
        response = self.client.post('/api/employee-salary-prepared', payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(EmployeeSalaryPrepared.objects.count(), 0)

    def test_complete_earned_array_is_validated_before_writes(self):
        payload = self.salary_payload()
        payload['all_earned_amounts'][0]['earned_amount'] = -1
        response = self.client.post('/api/employee-salary-prepared', payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(EmployeeSalaryPrepared.objects.count(), 0)

    def test_excessive_advance_repayment_rolls_back_existing_graph(self):
        advance = EmployeeAdvancePayment.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            principal=100,
            emi=25,
            date=date(2023, 12, 1),
            tenure_months_left=4,
        )
        initial = self.client.post(
            '/api/employee-salary-prepared', self.salary_payload(advance_deducted=25), format='json',
        )
        self.assertEqual(initial.status_code, 200, initial.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee)
        old_breakdown = list(salary.overtime_breakdown.values())
        old_earned = list(salary.current_salary_earned_amounts.values())

        response = self.client.post(
            '/api/employee-salary-prepared', self.salary_payload(advance_deducted=101), format='json',
        )
        self.assertEqual(response.status_code, 400)
        salary.refresh_from_db()
        self.assertEqual(salary.advance_deducted, 25)
        self.assertEqual(list(salary.overtime_breakdown.values()), old_breakdown)
        self.assertEqual(list(salary.current_salary_earned_amounts.values()), old_earned)
        self.assertEqual(advance.all_emis_of_advance.get().amount, 25)

    def test_failure_after_child_replacements_rolls_back(self):
        response = self.client.post('/api/employee-salary-prepared', self.salary_payload(), format='json')
        self.assertEqual(response.status_code, 200, response.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee)
        old_amount = salary.net_ot_amount_monthly
        old_rows = list(salary.overtime_breakdown.values())
        self.earning.value = 26000
        self.earning.save()
        payload = self.salary_payload()
        payload['all_earned_amounts'][0].update(rate=26000, earned_amount=26000)

        with patch(
            'api.services.salary_preparation._replace_repayments',
            side_effect=RuntimeError('repayment stage failed'),
        ):
            with self.assertRaisesRegex(RuntimeError, 'repayment stage failed'):
                prepare_employee_salary(
                    actor=self.user,
                    company_id=self.company.pk,
                    employee_id=self.employee.pk,
                    year=2024,
                    month=1,
                    parent_inputs=payload['employee_salary_prepared'],
                    earned_inputs=payload['all_earned_amounts'],
                )
        salary.refresh_from_db()
        self.assertEqual(salary.net_ot_amount_monthly, old_amount)
        self.assertEqual(list(salary.overtime_breakdown.values()), old_rows)
        self.assertEqual(salary.current_salary_earned_amounts.get().rate, 20800)

    def test_rerun_replaces_stale_children_and_policy_edits_do_not_mutate_snapshot(self):
        response = self.client.post('/api/employee-salary-prepared', self.salary_payload(), format='json')
        self.assertEqual(response.status_code, 200, response.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee)
        old_amount = salary.net_ot_amount_monthly
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')
        policy.rounding_increment_minutes = 45
        policy.round_up_from_minutes = 25
        policy.save()
        salary.refresh_from_db()
        self.assertEqual(salary.net_ot_amount_monthly, old_amount)
        self.assertEqual(salary.ot_rounding_increment_minutes, 30)

        stale_head = EarningsHead.objects.create(
            user=self.user, company=self.company, name='Stale', mandatory_earning=False,
        )
        EarnedAmount.objects.create(
            user=self.user,
            salary_prepared=salary,
            earnings_head=stale_head,
            rate=1,
            earned_amount=1,
        )
        EmployeeSalaryPreparedOvertimeDetail.objects.create(
            salary_prepared=salary,
            day_type='HOLIDAY',
            gross_minutes=1,
            net_minutes=1,
            multiplier=1,
            eligible_salary_rate=1,
            divisor=1,
            amount=1,
        )
        rerun = self.client.post('/api/employee-salary-prepared', self.salary_payload(), format='json')
        self.assertEqual(rerun.status_code, 200, rerun.data)
        salary.refresh_from_db()
        self.assertEqual(salary.current_salary_earned_amounts.count(), 1)
        self.assertEqual(list(salary.overtime_breakdown.values_list('day_type', flat=True)), ['REGULAR'])
        self.assertEqual(salary.ot_rounding_increment_minutes, 45)

    def test_bulk_preflight_is_all_or_nothing_and_uses_shared_service(self):
        second = self.create_employee(paycode='E002', attendance_card_no=102)
        self.create_salary_earning(second)
        response = self.client.post('/api/employee-bulk-salary-prepared', {
            'company': self.company.pk,
            'year': 2024,
            'month': 1,
            'employee_ids': [self.employee.pk, second.pk],
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(EmployeeSalaryPrepared.objects.count(), 0)

        EmployeePfEsiDetail.objects.create(user=self.user, company=self.company, employee=second)
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=second,
            date=date(2024, 1, 1),
            paid_days_count=62,
        )
        response = self.client.post('/api/employee-bulk-salary-prepared', {
            'company': self.company.pk,
            'year': 2024,
            'month': 1,
            'employee_ids': [self.employee.pk, second.pk],
        }, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['prepared_count'], 2)
        self.assertEqual(EmployeeSalaryPrepared.objects.count(), 2)

    def test_manual_and_bulk_persist_identical_server_owned_values(self):
        manual = self.client.post('/api/employee-salary-prepared', self.salary_payload(), format='json')
        self.assertEqual(manual.status_code, 200, manual.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee)
        manual_parent = (
            salary.pf_deducted,
            salary.esi_deducted,
            salary.vpf_deducted,
            salary.tds_deducted,
            salary.labour_welfare_fund_deducted,
            salary.net_ot_minutes_monthly,
            salary.net_ot_amount_monthly,
            salary.ot_rounding_increment_minutes,
            salary.ot_round_up_from_minutes,
        )
        manual_earned = list(salary.current_salary_earned_amounts.values_list(
            'earnings_head_id', 'rate', 'earned_amount', 'arear_amount',
        ))
        manual_overtime = list(salary.overtime_breakdown.values_list(
            'day_type', 'gross_minutes', 'deducted_late_minutes', 'net_minutes',
            'multiplier', 'eligible_salary_rate', 'divisor', 'amount',
        ))

        bulk = self.client.post('/api/employee-bulk-salary-prepared', {
            'company': self.company.pk,
            'year': 2024,
            'month': 1,
            'employee_ids': [self.employee.pk],
        }, format='json')
        self.assertEqual(bulk.status_code, 200, bulk.data)
        salary.refresh_from_db()
        self.assertEqual(manual_parent, (
            salary.pf_deducted,
            salary.esi_deducted,
            salary.vpf_deducted,
            salary.tds_deducted,
            salary.labour_welfare_fund_deducted,
            salary.net_ot_minutes_monthly,
            salary.net_ot_amount_monthly,
            salary.ot_rounding_increment_minutes,
            salary.ot_round_up_from_minutes,
        ))
        self.assertEqual(manual_earned, list(salary.current_salary_earned_amounts.values_list(
            'earnings_head_id', 'rate', 'earned_amount', 'arear_amount',
        )))
        self.assertEqual(manual_overtime, list(salary.overtime_breakdown.values_list(
            'day_type', 'gross_minutes', 'deducted_late_minutes', 'net_minutes',
            'multiplier', 'eligible_salary_rate', 'divisor', 'amount',
        )))


class PhaseSixSalaryPreparationConcurrencyTests(AttendanceTestDataMixin, TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        AttendanceTestDataMixin.setUpTestData.__func__(self.__class__)
        self.employee = self.create_employee()
        self.earning = self.create_salary_earning(self.employee)
        EmployeePfEsiDetail.objects.create(
            user=self.user, company=self.company, employee=self.employee,
        )
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 1),
            paid_days_count=62,
        )
        EmployeeAdvancePayment.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            principal=100,
            emi=100,
            date=date(2023, 12, 1),
            tenure_months_left=1,
        )

    def test_concurrent_saves_cannot_over_repay_an_advance(self):
        barrier = Barrier(2)

        def save_salary():
            close_old_connections()
            try:
                user = type(self.user).objects.get(pk=self.user.pk)
                barrier.wait()
                prepare_employee_salary(
                    actor=user,
                    company_id=self.company.pk,
                    employee_id=self.employee.pk,
                    year=2024,
                    month=1,
                    parent_inputs={'advance_deducted': 100},
                    earned_inputs=[{
                        'earnings_head': {'id': self.earning.earnings_head_id},
                        'rate': 20800,
                        'earned_amount': 20800,
                        'arear_amount': 0,
                    }],
                )
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(save_salary) for _ in range(2)]
            for future in futures:
                future.result()

        self.assertEqual(EmployeeSalaryPrepared.objects.count(), 1)
        self.assertEqual(
            sum(EmployeeAdvanceEmiRepayment.objects.values_list('amount', flat=True)),
            100,
        )
