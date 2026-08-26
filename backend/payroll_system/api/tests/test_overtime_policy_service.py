from decimal import Decimal
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Calculations, Company, EmployeeSalaryDetail, OvertimePolicy, OwnerToRegular, Regular, User
from api.services.overtime_policy import (
    OvertimePolicyConfigurationError,
    calculate_policy_overtime,
    get_company_default_overtime_policy,
    resolve_calculation_overtime_policy,
    resolve_employee_overtime_policy,
    update_overtime_policy,
)
from api.serializers import EmployeeSalaryDetailSerializer
from api.tests.base import AttendanceTestDataMixin


class OvertimePolicyResolutionTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee()
        self.salary_detail = EmployeeSalaryDetail.objects.get(employee=self.employee)

    def test_regular_days_system_policies_only_include_regular_rule(self):
        policies = OvertimePolicy.objects.filter(
            company=self.company,
            code__in=('REGULAR_DAYS_SINGLE', 'REGULAR_DAYS_DOUBLE'),
        ).order_by('code')

        self.assertEqual(policies.count(), 2)
        self.assertTrue(all(policy.is_system and policy.is_active for policy in policies))
        self.assertEqual(
            {
                policy.code: list(policy.day_rules.values_list('day_type', 'multiplier'))
                for policy in policies
            },
            {
                'REGULAR_DAYS_DOUBLE': [('REGULAR', Decimal('2.000'))],
                'REGULAR_DAYS_SINGLE': [('REGULAR', Decimal('1.000'))],
            },
        )

    def test_null_assignment_resolves_active_company_default_without_writes(self):
        before = list(OvertimePolicy.objects.values_list('pk', 'updated_at'))

        policy = resolve_employee_overtime_policy(self.salary_detail)

        self.assertTrue(policy.is_default)
        self.assertTrue(policy.is_active)
        self.assertEqual(list(OvertimePolicy.objects.values_list('pk', 'updated_at')), before)

    def test_default_change_changes_inherited_resolution(self):
        new_default = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        OvertimePolicy.objects.filter(company=self.company, is_default=True).update(is_default=False)
        new_default.is_default = True
        new_default.save(update_fields=['is_default'])

        self.assertEqual(resolve_employee_overtime_policy(self.salary_detail), new_default)
        self.assertEqual(get_company_default_overtime_policy(company=self.company), new_default)

    def test_explicit_inactive_assignment_remains_effective(self):
        policy = self.create_overtime_policy(is_active=False)
        self.assign_overtime_policy(self.employee, policy)
        self.salary_detail.refresh_from_db()

        self.assertEqual(resolve_employee_overtime_policy(self.salary_detail), policy)

    def test_inactive_policy_cannot_be_newly_assigned_but_existing_assignment_is_preserved(self):
        policy = self.create_overtime_policy(is_active=False)
        serializer = EmployeeSalaryDetailSerializer(
            self.salary_detail,
            data={'overtime_policy': policy.pk},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('overtime_policy', serializer.errors)

        self.assign_overtime_policy(self.employee, policy)
        self.salary_detail.refresh_from_db()
        serializer = EmployeeSalaryDetailSerializer(
            self.salary_detail,
            data={'overtime_policy': policy.pk, 'salary_mode': 'daily'},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_default_raises_controlled_error(self):
        OvertimePolicy.objects.filter(company=self.company, is_default=True).update(is_default=False)

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            resolve_employee_overtime_policy(self.salary_detail)

        self.assertEqual(caught.exception.code, 'missing_active_default')

    def test_owner_calculation_uses_explicit_then_inherited_policy(self):
        explicit = self.create_overtime_policy()
        self.assign_overtime_policy(self.employee, explicit)
        self.salary_detail.refresh_from_db()

        self.assertEqual(
            resolve_calculation_overtime_policy(actor=self.user, employee_salary_detail=self.salary_detail),
            explicit,
        )
        self.salary_detail.overtime_policy = None
        self.salary_detail.save(update_fields=['overtime_policy'])
        self.assertEqual(
            resolve_calculation_overtime_policy(actor=self.user, employee_salary_detail=self.salary_detail),
            get_company_default_overtime_policy(company=self.company),
        )

    def test_regular_calculation_always_uses_all_days_double(self):
        regular = Regular.objects.create_user(
            username='regular', email='regular@example.com', password='password', phone_no=9999999998
        )
        OwnerToRegular.objects.create(user=regular, owner=self.user)
        explicit = self.create_overtime_policy()
        self.assign_overtime_policy(self.employee, explicit)
        self.salary_detail.refresh_from_db()

        policy = resolve_calculation_overtime_policy(actor=regular, employee_salary_detail=self.salary_detail)

        self.assertEqual(policy.code, 'ALL_DAYS_DOUBLE')

    def test_regular_resolution_rejects_missing_or_malformed_system_policy(self):
        regular = Regular.objects.create_user(
            username='regular-malformed',
            email='regular-malformed@example.com',
            password='password',
            phone_no=9999999952,
        )
        OwnerToRegular.objects.create(user=regular, owner=self.user)
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')
        policy.day_rules.filter(day_type='HOLIDAY').delete()

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            resolve_calculation_overtime_policy(actor=regular, employee_salary_detail=self.salary_detail)

        self.assertEqual(caught.exception.code, 'malformed_all_days_double')

    def test_resolution_rejects_cross_company_actor(self):
        other_owner = User.objects.create_user(
            username='other', email='other@example.com', password='password', phone_no=9999999997
        )
        Company.objects.create(user=other_owner, name='Other')

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            resolve_calculation_overtime_policy(actor=other_owner, employee_salary_detail=self.salary_detail)

        self.assertEqual(caught.exception.code, 'cross_company_resolution')

    def test_owner_calculation_uses_policy_multiplier_not_legacy_rate(self):
        policy = self.create_overtime_policy(code='ONE_POINT_FIVE', rules=(('REGULAR', '1.5'),))
        self.salary_detail.overtime_rate = 'D'
        self.salary_detail.overtime_policy = policy
        self.salary_detail.save(update_fields=['overtime_rate', 'overtime_policy'])
        attendance = self.create_attendance(self.employee, ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)
        earning = self.create_salary_earning(self.employee)

        result = calculate_policy_overtime(
            employee_salary_detail=self.salary_detail,
            attendance_records=[attendance],
            salary_earnings=[earning],
            company_calculations=Calculations.objects.get(company=self.company),
            user=self.user,
            days_in_month=31,
        )

        self.assertEqual(result.amount, Decimal('150'))
        self.assertEqual(result.breakdown[0]['multiplier'], Decimal('1.5'))

    def test_mutation_service_protects_system_definition(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')

        with self.assertRaises(ValidationError):
            update_overtime_policy(
                actor=self.user,
                company=self.company,
                policy=policy,
                validated_data={'name': 'Changed'},
                day_rules=None,
                selected_heads=None,
            )

        policy.refresh_from_db()
        self.assertEqual(policy.name, 'All days - double rate')

    def test_mutation_service_validates_rounding_under_lock_and_allows_system_update(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')

        with self.assertRaises(ValidationError):
            update_overtime_policy(
                actor=self.user,
                company=self.company,
                policy=policy,
                validated_data={'rounding_increment_minutes': 15},
                day_rules=None,
                selected_heads=None,
            )
        policy.refresh_from_db()
        self.assertEqual((policy.rounding_increment_minutes, policy.round_up_from_minutes), (30, 16))

        update_overtime_policy(
            actor=self.user,
            company=self.company,
            policy=policy,
            validated_data={'rounding_increment_minutes': 45, 'round_up_from_minutes': 25},
            day_rules=None,
            selected_heads=None,
        )
        policy.refresh_from_db()
        self.assertEqual((policy.rounding_increment_minutes, policy.round_up_from_minutes), (45, 25))

    def test_calculator_uses_policy_rounding_and_returns_applied_pair(self):
        employee = self.create_employee(paycode='ROUND', attendance_card_no=151)
        policy = self.create_overtime_policy(round_up_from_minutes=16)
        salary_detail = self.assign_overtime_policy(employee, policy)
        attendance = self.create_attendance(employee, ot_min=46)
        self.create_overtime_detail(attendance, minutes=46)
        earning = self.create_salary_earning(employee)

        result = calculate_policy_overtime(
            employee_salary_detail=salary_detail,
            attendance_records=[attendance],
            salary_earnings=[earning],
            company_calculations=Calculations.objects.get(company=self.company),
            user=self.user,
            days_in_month=31,
        )

        self.assertEqual(result.net_minutes, 60)
        self.assertEqual((result.rounding_increment_minutes, result.round_up_from_minutes), (30, 16))

    def test_resolved_policy_serialization_exposes_rounding_pair(self):
        data = EmployeeSalaryDetailSerializer(self.salary_detail).data

        self.assertEqual(data['resolved_overtime_policy']['rounding_increment_minutes'], 30)
        self.assertEqual(data['resolved_overtime_policy']['round_up_from_minutes'], 16)

    def test_resolved_policy_serialization_uses_regular_calculation_policy(self):
        regular = Regular.objects.create_user(
            username='regular-serializer',
            email='regular-serializer@example.com',
            password='password',
            phone_no=9999999951,
        )
        OwnerToRegular.objects.create(user=regular, owner=self.user)
        explicit = self.create_overtime_policy(rounding_increment_minutes=15, round_up_from_minutes=8)
        self.assign_overtime_policy(self.employee, explicit)
        self.salary_detail.refresh_from_db()
        system_policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')
        system_policy.rounding_increment_minutes = 45
        system_policy.round_up_from_minutes = 25
        system_policy.save(update_fields=['rounding_increment_minutes', 'round_up_from_minutes'])

        data = EmployeeSalaryDetailSerializer(
            self.salary_detail,
            context={'request': SimpleNamespace(user=regular)},
        ).data

        self.assertEqual(data['resolved_overtime_policy']['code'], 'ALL_DAYS_DOUBLE')
        self.assertEqual(data['resolved_overtime_policy']['rounding_increment_minutes'], 45)
        self.assertEqual(data['resolved_overtime_policy']['round_up_from_minutes'], 25)
