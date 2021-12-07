from django.test import TestCase
from django.utils import timezone
from account.models import CustomUser
from django.urls import reverse
from datetime import datetime


class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@gmail.com',
            user_name='User',
            password='*qwerty#',
            birth_date=datetime.strptime('2000-01-01', "%Y-%m-%d")

        )

    def test_method__str__(self):
        self.assertEqual(self.user.user_name, 'User')

    def test_user_get_absolute_url(self):
        self.assertEquals(self.user.get_absolute_url(), reverse('account:profile_for_staff', args=[self.user.id]))

    def test_user_age_method(self):
        today = timezone.now()
        birth_date = datetime.strptime('2000-01-01', "%Y-%m-%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.assertEqual(self.user.age, age)
