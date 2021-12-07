from django.test import TestCase
from account.models import CustomUser
from account.forms import ChangeProfileForm, ChangeEmailForm
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from account.forms import default_image


class ChangeProfileFormTest(TestCase):
    def setUp(self):
        self.data = {
            'email': 'test@gmail.com',
            'user_name': 'User',
            'password': '*qwerty#',
            'birth_date': datetime.strptime('2000-01-01', "%Y-%m-%d"),
            'gender': 'Male'
        }

        self.user = CustomUser.objects.create_user(**self.data)

        self.staff = CustomUser.objects.create_staff(
            email='stafftest@gmail.com',
            user_name='Staff',
            password='*qwerty#'
        )
        self.form = ChangeProfileForm(self.data)

        self.client.force_login(self.user)
        self.client.post(reverse('account:change_profile', args=[self.user.id]))

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_form_invalid(self):
        self.data['user_name'] = 'new_user_name_very_long_name'
        form = ChangeProfileForm(self.data)
        self.assertFalse(form.is_valid())

    def test_form_age_valid(self):
        self.form.is_valid()
        self.assertTrue(self.form.age_valid())

    def test_form_age_invalid(self):
        self.data['birth_date'] = timezone.now().date()
        form = ChangeProfileForm(self.data)
        form.is_valid()
        self.assertFalse(form.age_valid())

    def test_form_image_method(self):
        form = self.form
        user = self.user
        image = form.image(user.main_image, 'Male')
        self.assertIn(user.main_image, default_image.values())
        self.assertEqual(image, default_image['Male'])

    def test_form_save_method(self):
        user = self.user
        form = self.form
        form.is_valid()
        user = form.save()
        self.assertEqual(user.gender, 'Male')


class ChangeEmailFormTest(TestCase):

    def setUp(self):
        self.valid_email_data = {
            'email': 'valid_email_data@gmail.com',
            'password': '*qwerty#',
            'new_email': 'newtest@gmail.com',
            'repeat_new_email': 'newtest@gmail.com'
        }
        self.invalid_email_data = {
            'email': 'invalid_email_data@gmail.com',
            'password': '*qwerty#',
            'new_email': 'newtest@gmail.com',
            'repeat_new_email': 'new_test@gmail.com'
        }

        self.user = CustomUser.objects.create_user(
            email='test@gmail.com',
            user_name='User',
            password='*qwerty#',
            birth_date=datetime.strptime('2000-01-01', "%Y-%m-%d")
        )

        self.staff = CustomUser.objects.create_staff(
            email='stafftest@gmail.com',
            user_name='Staff',
            password='*qwerty#',
        )
        self.valid_form = ChangeEmailForm(self.valid_email_data)
        self.invalid_form = ChangeEmailForm(self.invalid_email_data)

        self.client.force_login(self.user)
        self.client.post(reverse('account:change_email', args=[self.user.id]))

    def test_form_valid(self):
        self.valid_form.is_valid()
        self.assertTrue(self.valid_form.is_valid())

    def test_form_invalid(self):
        self.assertFalse(self.invalid_form.is_valid())
