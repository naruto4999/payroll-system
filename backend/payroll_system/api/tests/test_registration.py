from django.core import mail
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import OTP, User


class RegistrationTests(TestCase):
    register_url = '/api/auth/register/'
    verify_url = '/api/auth/register/otp'

    def setUp(self):
        self.client = APIClient()
        self.existing_user = User.objects.create_user(
            username='existing-user',
            email='existing@example.com',
            password='password123',
            phone_no=9999999999,
        )

    def registration_payload(self, **overrides):
        payload = {
            'username': 'new-user',
            'email': 'new@example.com',
            'password': 'password123',
            'phone_no': 9999999998,
        }
        payload.update(overrides)
        return payload

    def test_existing_email_is_rejected_before_otp_is_sent(self):
        response = self.client.post(
            self.register_url,
            self.registration_payload(email=self.existing_user.email),
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('email', response.data)
        self.assertEqual(str(response.data['email'][0]), 'A user with this email already exists.')
        self.assertEqual(OTP.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_users_can_register_with_the_same_phone_number(self):
        payload = self.registration_payload(phone_no=self.existing_user.phone_no)
        response = self.client.post(self.register_url, payload, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        otp = OTP.objects.get(email=payload['email'])

        response = self.client.post(
            self.verify_url,
            {**payload, 'otp': otp.otp},
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(User.objects.filter(phone_no=self.existing_user.phone_no).count(), 2)

    def test_email_conflict_after_otp_delivery_returns_email_error(self):
        payload = self.registration_payload()
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        otp = OTP.objects.get(email=payload['email'])

        User.objects.create_user(
            username='another-user',
            email=payload['email'],
            password='password123',
            phone_no=9999999997,
        )
        response = self.client.post(
            self.verify_url,
            {**payload, 'otp': otp.otp},
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('email', response.data)
        self.assertFalse(User.objects.filter(username=payload['username']).exists())
