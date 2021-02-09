from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Test_Index_View(TestCase):
    #fixtures = [settings.PROJECT_PATH / 'fixtures' / 'groups.json']
    """
        python3 manage.py test --keepdb apps
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="admin@example.com",
            email="admin@example.com",
            password="1QAZ2wsx", is_active=True, is_staff=True
        )
        # self.user.user_permissions.set(list(Permission.objects.filter(
        #     codename__in=[
        #         'can_see_deals',
        #     ]
        # ).values_list('id', flat=True)))

    def test_index_view(self):
        url = "/"
        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
