from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User


class TestAccounts(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user = User.objects.create(
            username='admin@admin.ru',
            first_name='Админ',
            middle_name='А',
            last_name='Админов',
            phone='+79109200101',
            email='admin@admin.ru',
            password="1QAZ2wsx",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

    def setUp(self):
        self.client.force_login(user=self.user, backend='django.contrib.auth.backends.ModelBackend')

    def test_accounts_list(self):
        url = reverse('api-root:accounts-list')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_accounts_me(self):
        url = reverse('api-root:accounts-me')
        self.client.force_login(self.user)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 16)

    def test_send_activation_email(self):
        send = self.user.send_verify_email()
        self.assertEqual(send.status, "PENDING")

    def test_send_restore_password_email(self):
        send = self.user.send_change_password_email()
        self.assertEqual(send.status, "PENDING")

    def test_api_registry_account(self):
        url = reverse('api-root:accounts-registration')
        data = {
            "username": "test@example.com",
            "first_name": "Иван",
            "middle_name": "Иванович",
            "last_name": "Иванов",
            "email": "test@example.com",
            "phone": "+79109200102",
            "password": "1Initial",
            "passworddup": "1Initial"
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 201)

        url = reverse('api-root:accounts-list')
        self.client.force_login(self.user)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.data['count'], 3)

    def test_api_restore_password(self):
        url = reverse('api-root:accounts-restore-password')
        data = {'username': 'admin@admin.ru'}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')

    def test_api_headers(self):
        url = reverse('api-root:accounts-headers')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
