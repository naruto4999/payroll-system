from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Company, CompanyReportConfiguration, Regular, User


class CompanyReportConfigurationApiTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner-config',
            email='owner-config@example.com',
            password='password',
            phone_no=9000000001,
        )
        self.company = Company.objects.create(user=self.owner, name='Configured Company')
        self.client = APIClient()
        self.client.force_authenticate(self.owner)
        self.url = f'/api/company-report-configuration/{self.company.pk}'

    def payload(self, display='weighted'):
        return {
            'report_type': 'payment_sheet',
            'output_format': 'xlsx',
            'options': {'ot_hours_display': display},
        }

    def test_owner_can_create_list_and_update_configuration(self):
        create_response = self.client.post(self.url, self.payload(), format='json')
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.data['options']['ot_hours_display'], 'weighted')

        list_response = self.client.get(self.url)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        detail_url = f"{self.url}/{create_response.data['id']}"
        update_response = self.client.patch(
            detail_url,
            {'options': {'ot_hours_display': 'actual'}},
            format='json',
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['options']['ot_hours_display'], 'actual')

    def test_configuration_is_unique_per_company_report_and_format(self):
        self.client.post(self.url, self.payload(), format='json')

        duplicate_response = self.client.post(self.url, self.payload(), format='json')

        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(CompanyReportConfiguration.objects.count(), 1)

    def test_invalid_or_unknown_options_are_rejected(self):
        invalid_value = self.client.post(self.url, self.payload('triple'), format='json')
        unknown_option = self.client.post(
            self.url,
            {
                'report_type': 'payment_sheet',
                'output_format': 'xlsx',
                'options': {'unknown': True},
            },
            format='json',
        )
        unsupported_report = self.client.post(
            self.url,
            {'report_type': 'payslip', 'output_format': 'pdf', 'options': {}},
            format='json',
        )

        self.assertEqual(invalid_value.status_code, 400)
        self.assertEqual(unknown_option.status_code, 400)
        self.assertEqual(unsupported_report.status_code, 400)

    def test_other_owner_cannot_access_company_configuration(self):
        other_owner = User.objects.create_user(
            username='other-owner-config',
            email='other-owner-config@example.com',
            password='password',
            phone_no=9000000002,
        )
        self.client.force_authenticate(other_owner)

        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_regular_user_cannot_manage_configuration(self):
        regular = Regular.objects.create_user(
            username='regular-config',
            email='regular-config@example.com',
            password='password',
            phone_no=9000000003,
        )
        self.client.force_authenticate(regular)

        self.assertEqual(self.client.get(self.url).status_code, 403)
