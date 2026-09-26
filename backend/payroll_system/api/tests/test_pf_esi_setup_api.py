from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Company, EarningsHead
from api.tests.base import AttendanceTestDataMixin


class PfEsiSetupApiTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.setup = self.company.pf_esi_setup_details

    def setup_payload(self, **overrides):
        payload = {
            'company': self.company.pk,
            'ac_1_epf_employee_percentage': '12.00',
            'ac_1_epf_employee_limit': 15000,
            'ac_1_epf_employer_percentage': '3.67',
            'ac_1_epf_employer_limit': 15000,
            'ac_10_eps_employer_percentage': '8.33',
            'ac_10_eps_employer_limit': 15000,
            'ac_2_employer_percentage': '0.50',
            'ac_21_employer_percentage': '0.50',
            'ac_22_employer_percentage': '0.00',
            'employer_pf_code': '',
            'esi_employee_percentage': '0.75',
            'esi_employee_limit': 21000,
            'esi_employer_percentage': '3.25',
            'esi_employer_limit': 21000,
            'employer_esi_code': '',
            'esi_earnings_heads': list(
                self.setup.esi_earnings_heads.values_list('pk', flat=True)
            ),
            'enable_labour_welfare_fund': False,
            'labour_wellfare_fund_employer_code': '',
            'labour_welfare_fund_percentage': '0.20',
            'labour_welfare_fund_limit': 31,
        }
        payload.update(overrides)
        return payload

    def test_existing_company_defaults_all_earnings_heads_for_esi(self):
        self.assertSetEqual(
            set(self.setup.esi_earnings_heads.values_list('pk', flat=True)),
            set(EarningsHead.objects.filter(company=self.company).values_list('pk', flat=True)),
        )

    def test_update_replaces_esi_earnings_heads(self):
        basic = EarningsHead.objects.get(company=self.company, name='Basic')
        response = self.client.put(
            f'/api/pf-esi-setup/{self.company.pk}',
            self.setup_payload(esi_earnings_heads=[basic.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['esi_earnings_heads'], [basic.pk])
        self.assertSetEqual(
            set(self.setup.esi_earnings_heads.values_list('pk', flat=True)),
            {basic.pk},
        )

    def test_update_requires_at_least_one_esi_earnings_head(self):
        response = self.client.put(
            f'/api/pf-esi-setup/{self.company.pk}',
            self.setup_payload(esi_earnings_heads=[]),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('esi_earnings_heads', response.data)

    def test_update_rejects_another_company_earning_head(self):
        other_company = Company.objects.create(user=self.user, name='Other')
        other_head = EarningsHead.objects.get(company=other_company, name='Basic')
        response = self.client.put(
            f'/api/pf-esi-setup/{self.company.pk}',
            self.setup_payload(esi_earnings_heads=[other_head.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('esi_earnings_heads', response.data)
