from rest_framework.test import APITestCase
from rest_framework import status
from account.models import CustomUser


class UserAPITest(APITestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(
            email='email@gmail.com',
            user_name='User',
            password='*qwerty#',
            country='UK'
        )

        self.staff = CustomUser.objects.create_staff(
            email='stafftest@gmail.com',
            user_name='Staff',
            password='*qwerty#',
            country='UK'
        )

        self.data = {
            'email': 'new_email@gmail.com',
            'user_name': 'New Name',
            'password': '*qwerty#',
            'country': 'USA'
        }

    def test_user_update_by_anonymous_response(self):
        user = self.user
        response = self.client.put('/account/api/user-update/{}'.format(user.id), data=self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_user_update_by_yourself_response(self):
        user = self.user
        self.client.force_authenticate(user)
        response = self.client.put('/account/api/user-update/{}'.format(user.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_user_update_by_another_user_response(self):
        self.client.force_authenticate(self.staff)
        response = self.client.put('/account/api/user-update/{}'.format(self.user.id), data=self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_user_ban_or_unban_by_anonymous_response(self):
        response = self.client.put('/account/api/user-ban/{}'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_user_ban_or_unban_by_user_response(self):
        user = self.user
        self.client.force_authenticate(user)
        response = self.client.put('/account/api/user-ban/{}'.format(user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_user_ban_or_unban_by_staff_response(self):
        self.client.force_authenticate(self.staff)
        response = self.client.put('/account/api/user-ban/{}'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_user_change_permission_by_anonymous_response(self):
        response = self.client.put('/account/api/user-permission/{}'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_user_change_permission_by_user_response(self):
        user = self.user
        self.client.force_authenticate(user)
        response = self.client.put('/account/api/user-permission/{}'.format(user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_user_change_permission_by_staff_response(self):
        self.client.force_authenticate(self.staff)
        response = self.client.put('/account/api/user-permission/{}'.format(self.user.id),)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
