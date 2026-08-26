from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient

from api.models import Company, EarningsHead, OvertimePolicy, OwnerToRegular, Regular, User
from api.tests.base import AttendanceTestDataMixin
from api.services.overtime_policy import update_overtime_policy


class OvertimePolicyApiTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.list_url = f'/api/overtime-policy/{self.company.pk}'
        self.default = OvertimePolicy.objects.get(company=self.company, is_default=True)
        self.system = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')

    def policy_payload(self, **overrides):
        payload = {
            'name': 'Night shift policy',
            'is_default': False,
            'is_active': True,
            'earnings_basis': 'ALL_EARNINGS',
            'day_rules': [
                {'day_type': 'REGULAR', 'multiplier': '1.500', 'late_deduction_priority': 1},
                {'day_type': 'HOLIDAY', 'multiplier': '2.000', 'late_deduction_priority': 2},
            ],
        }
        payload.update(overrides)
        return payload

    def test_owner_can_list_retrieve_create_update_and_delete(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(f'{self.list_url}/{self.system.pk}').status_code, 200)

        response = self.client.post(self.list_url, self.policy_payload(), format='json')
        self.assertEqual(response.status_code, 201, response.data)
        policy = OvertimePolicy.objects.get(pk=response.data['id'])
        self.assertEqual(policy.company, self.company)
        self.assertRegex(policy.code, r'^CUSTOM_[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

        detail_url = f'{self.list_url}/{policy.pk}'
        response = self.client.patch(detail_url, {'name': 'Updated policy'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['name'], 'Updated policy')
        self.assertEqual(self.client.delete(detail_url).status_code, 204)
        self.assertFalse(OvertimePolicy.objects.filter(pk=policy.pk).exists())

    def test_regular_is_rejected_from_every_management_method(self):
        regular = Regular.objects.create_user(
            username='regular-api', email='regular-api@example.com', password='password', phone_no=9999999998
        )
        OwnerToRegular.objects.create(user=regular, owner=self.user)
        custom = self.create_overtime_policy(code='REGULAR_DENIED')
        self.client.force_authenticate(regular)

        requests = (
            self.client.get(self.list_url),
            self.client.get(f'{self.list_url}/{custom.pk}'),
            self.client.post(self.list_url, self.policy_payload(), format='json'),
            self.client.patch(f'{self.list_url}/{custom.pk}', {'name': 'No'}, format='json'),
            self.client.patch(f'{self.list_url}/{custom.pk}', {'is_default': True}, format='json'),
            self.client.patch(f'{self.list_url}/{custom.pk}', {'is_active': False}, format='json'),
            self.client.delete(f'{self.list_url}/{custom.pk}'),
        )

        self.assertEqual([response.status_code for response in requests], [403] * len(requests))

    def test_unowned_company_is_hidden_and_body_cannot_move_policy(self):
        other_owner = User.objects.create_user(
            username='other-api', email='other-api@example.com', password='password', phone_no=9999999997
        )
        other_company = Company.objects.create(user=other_owner, name='Other')
        self.assertEqual(self.client.get(f'/api/overtime-policy/{other_company.pk}').status_code, 404)

        response = self.client.post(
            self.list_url,
            self.policy_payload(company=other_company.pk),
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('company', response.data)

        response = self.client.patch(
            f'{self.list_url}/{self.system.pk}',
            {'company': other_company.pk},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.system.refresh_from_db()
        self.assertEqual(self.system.company, self.company)

    def test_default_switch_is_atomic_and_only_default_cannot_be_removed(self):
        custom = self.create_overtime_policy(code='NEW_DEFAULT')
        response = self.client.patch(f'{self.list_url}/{custom.pk}', {'is_default': True}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            list(OvertimePolicy.objects.filter(company=self.company, is_default=True).values_list('pk', flat=True)),
            [custom.pk],
        )

        for payload in ({'is_default': False}, {'is_active': False}):
            response = self.client.patch(f'{self.list_url}/{custom.pk}', payload, format='json')
            self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.delete(f'{self.list_url}/{custom.pk}').status_code, 400)
        custom.refresh_from_db()
        self.assertTrue(custom.is_default)
        self.assertTrue(custom.is_active)

    def test_nested_validation_failure_does_not_change_default_or_rules(self):
        custom = self.create_overtime_policy(code='ROLLBACK')
        original_rules = list(custom.day_rules.values_list('day_type', 'late_deduction_priority'))
        response = self.client.patch(
            f'{self.list_url}/{custom.pk}',
            {
                'is_default': True,
                'day_rules': [
                    {'day_type': 'REGULAR', 'multiplier': '1.000', 'late_deduction_priority': 1},
                    {'day_type': 'REGULAR', 'multiplier': '2.000', 'late_deduction_priority': 2},
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.default.refresh_from_db()
        custom.refresh_from_db()
        self.assertTrue(self.default.is_default)
        self.assertFalse(custom.is_default)
        self.assertEqual(list(custom.day_rules.values_list('day_type', 'late_deduction_priority')), original_rules)

    def test_duplicate_priorities_and_selected_heads_are_rejected(self):
        duplicate_priorities = self.policy_payload(day_rules=[
            {'day_type': 'REGULAR', 'multiplier': '1.000', 'late_deduction_priority': 1},
            {'day_type': 'HOLIDAY', 'multiplier': '2.000', 'late_deduction_priority': 1},
        ])
        self.assertEqual(self.client.post(self.list_url, duplicate_priorities, format='json').status_code, 400)

        head = EarningsHead.objects.filter(company=self.company).first()
        selected = self.policy_payload(
            earnings_basis='SELECTED_HEADS',
            selected_earning_head_ids=[head.pk, head.pk],
        )
        self.assertEqual(self.client.post(self.list_url, selected, format='json').status_code, 400)

    def test_selected_head_state_transitions_are_validated(self):
        response = self.client.post(
            self.list_url,
            self.policy_payload(earnings_basis='SELECTED_HEADS'),
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        head = EarningsHead.objects.filter(company=self.company).first()
        response = self.client.post(
            self.list_url,
            self.policy_payload(earnings_basis='SELECTED_HEADS', selected_earning_head_ids=[head.pk]),
            format='json',
        )
        self.assertEqual(response.status_code, 201, response.data)
        policy = OvertimePolicy.objects.get(pk=response.data['id'])

        response = self.client.patch(f'{self.list_url}/{policy.pk}', {'name': 'Preserved'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(policy.selected_earning_heads.count(), 1)

        response = self.client.patch(
            f'{self.list_url}/{policy.pk}', {'earnings_basis': 'ALL_EARNINGS'}, format='json'
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertFalse(policy.selected_earning_heads.exists())

    def test_cross_company_selected_head_is_rejected(self):
        other_owner = User.objects.create_user(
            username='heads-owner', email='heads@example.com', password='password', phone_no=9999999996
        )
        other_company = Company.objects.create(user=other_owner, name='Heads')
        head = EarningsHead.objects.filter(company=other_company).first()

        response = self.client.post(
            self.list_url,
            self.policy_payload(earnings_basis='SELECTED_HEADS', selected_earning_head_ids=[head.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('selected_earning_head_ids', response.data)

    def test_system_definition_and_deletion_are_protected(self):
        detail_url = f'{self.list_url}/{self.system.pk}'
        for payload in (
            {'name': 'Changed'},
            {'code': 'CHANGED'},
            {'is_system': False},
            {'is_active': False},
            {'earnings_basis': 'SELECTED_HEADS', 'selected_earning_head_ids': []},
            {'day_rules': []},
        ):
            response = self.client.patch(detail_url, payload, format='json')
            self.assertEqual(response.status_code, 400, response.data)

        self.assertEqual(self.client.delete(detail_url).status_code, 400)

    def test_rounding_defaults_are_exposed_and_valid_updates_are_persisted(self):
        response = self.client.post(self.list_url, self.policy_payload(), format='json')
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['rounding_increment_minutes'], 30)
        self.assertEqual(response.data['round_up_from_minutes'], 16)

        detail_url = f"{self.list_url}/{response.data['id']}"
        response = self.client.patch(
            detail_url,
            {'rounding_increment_minutes': 30, 'round_up_from_minutes': 16},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['rounding_increment_minutes'], 30)
        self.assertEqual(response.data['round_up_from_minutes'], 16)
        self.assertIn('rounding_increment_minutes', self.client.get(self.list_url).data[0])

    def test_rounding_pair_validation_uses_merged_patch_state(self):
        custom = self.create_overtime_policy(code='ROUNDING_PATCH')
        detail_url = f'{self.list_url}/{custom.pk}'

        for payload in (
            self.policy_payload(rounding_increment_minutes=0),
            self.policy_payload(rounding_increment_minutes=30, round_up_from_minutes=31),
        ):
            response = self.client.post(self.list_url, payload, format='json')
            self.assertEqual(response.status_code, 400, response.data)

        for payload in (
            {'rounding_increment_minutes': 0},
            {'round_up_from_minutes': 0},
            {'rounding_increment_minutes': 15},
            {'round_up_from_minutes': 31},
        ):
            response = self.client.patch(detail_url, payload, format='json')
            self.assertEqual(response.status_code, 400, response.data)

        custom.refresh_from_db()
        self.assertEqual((custom.rounding_increment_minutes, custom.round_up_from_minutes), (30, 16))
        response = self.client.patch(detail_url, {'round_up_from_minutes': 16}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['rounding_increment_minutes'], 30)

    def test_system_policy_allows_only_valid_rounding_definition_changes(self):
        response = self.client.patch(
            f'{self.list_url}/{self.system.pk}',
            {'rounding_increment_minutes': 45, 'round_up_from_minutes': 25},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.system.refresh_from_db()
        self.assertEqual((self.system.rounding_increment_minutes, self.system.round_up_from_minutes), (45, 25))


class OvertimePolicyConcurrencyTests(AttendanceTestDataMixin, TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.setUpTestData()

    def test_concurrent_default_switches_leave_exactly_one_active_default(self):
        first = self.create_overtime_policy(code='CONCURRENT_FIRST')
        second = self.create_overtime_policy(code='CONCURRENT_SECOND')
        barrier = Barrier(2)

        def switch_default(policy_id):
            close_old_connections()
            actor = User.objects.get(pk=self.user.pk)
            company = Company.objects.get(pk=self.company.pk)
            policy = OvertimePolicy.objects.get(pk=policy_id)
            barrier.wait()
            update_overtime_policy(
                actor=actor,
                company=company,
                policy=policy,
                validated_data={'is_default': True},
                day_rules=None,
                selected_heads=None,
            )
            close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(switch_default, policy.pk) for policy in (first, second)]
            for future in futures:
                future.result()

        defaults = OvertimePolicy.objects.filter(company=self.company, is_default=True, is_active=True)
        self.assertEqual(defaults.count(), 1)
        self.assertIn(defaults.get().pk, {first.pk, second.pk})
