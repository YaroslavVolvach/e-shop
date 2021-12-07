from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from account.models import CustomUser
from account.views import remove_image, UserList, blacklist, permissions
from django.urls import reverse
from django.shortcuts import get_object_or_404


class CreateUserForTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@gmail.com',
            user_name='User',
            password='*qwerty#',
            gender='Male'
        )

        self.banned = CustomUser.objects.create_user(
            email='banned@gmail.com',
            user_name='Banned',
            password='*qwerty#',
            gender='Femail',
            is_active=False
        )

        self.staff = CustomUser.objects.create_staff(
            email='stafftest@gmail.com',
            user_name='Staff',
            password='*qwerty#',
        )


class CustomUserViewTest(CreateUserForTests):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_change_image_view(self):
        response = self.client.post(reverse('account:change_image'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/profile/', 302, 200)

    def test_remove_image_view(self):
        request = self.factory.post(reverse('account:change_image'))
        old_image = self.user.main_image
        request.user = self.user
        response = remove_image(request)
        response.client = self.client
        self.assertNotEqual(request.user.main_image, old_image)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/profile/', 302, 200)

    def test_remove_image_view_redirect(self):
        response = self.client.post(reverse('account:change_image'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/profile/', 302, 200)

    def user_list(self, category):
        instance = UserList()
        instance.kwargs = {'category': category}
        return instance.get_queryset()

    def test_user_list_staff_view(self):
        self.assertEqual(self.user_list('Staff').first(), self.staff)

    def test_user_list_user_view(self):
        self.assertEqual(self.user_list('Customers').first(), self.user)

    def test_user_list_blocked_user_view(self):
        self.assertEqual(self.user_list('Blocked users').first(), self.banned)

    def test_user_list_all_user_view(self):
        self.assertQuerysetEqual(self.user_list('All users').order_by('id'), CustomUser.objects.all().order_by('id'))


class CustomUserViewForPermissionTest(CreateUserForTests):
    def test_blacklist_for_anonymous(self):

        response = self.client.post(reverse('account:blacklist', args=(self.user.id, 'Customers')))
        self.assertEqual(response.status_code, 302)
       # self.assertRedirects(response, '/admin/login/?next=%2Faccount%2Fblacklist%2F1%2FCustomers%2F', 302, 200)

    def test_blacklist_for_user(self):
        self.client.force_login(self.user)
        url = reverse('account:blacklist', args=(self.user.id, 'Customers'))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
       # self.assertRedirects(response, url, 302, 200)

    def test_blacklist_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('account:blacklist', args=(self.user.id, 'Customers')))
       # self.assertEqual(response.status_code, 302)
       # self.assertRedirects(response, '/account/users/Customers/', 302, 200)

    def blacklist_for_blocke(self, request_user):
        user = self.user
        banned = self.banned
        self.client.force_login(request_user)
        request = RequestFactory().post(reverse('account:blacklist', args=(0, 'Customers')))
        request.user = request_user
        blacklist(request, user.id, 'Customers')
        blacklist(request, banned.id, 'Customers')
        user = get_object_or_404(CustomUser, id=user.id)
        banned = get_object_or_404(CustomUser, id=banned.id)
        return (user, banned)

    def test_blacklist_for_anonymous_blocke(self):
        user, banned = self.blacklist_for_blocke(self.user)
        self.assertTrue(user.is_active)
        self.assertFalse(banned.is_active)

    def test_blacklist_for_user_blocke(self):
        user, banned = self.blacklist_for_blocke(self.user)
        self.assertTrue(user.is_active)
        self.assertFalse(banned.is_active)

    def test_blacklist_for_staff_blocke(self):
        user, banned = self.blacklist_for_blocke(self.staff)
        self.assertFalse(user.is_active)
        self.assertTrue(banned.is_active)

    def test_permissions_for_anonymous(self):
        response = self.client.post(reverse('account:permissions', args=(self.user.id, 'Customers')))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/account/login/?next=%2Faccount%2Fpermissions%2F29%2FCustomers%2F', 302, 200)

    def test_permissions_for_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account:permissions', args=(self.user.id, 'Customers')))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('account:login'), 302, 200)

    def test_permissions_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('account:permissions', args=(self.user.id, 'Customers')))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/account/users/Customers/', 302, 200)

    def permissions_for_blocke(self, request_user):
        user = self.user
        staff = self.staff
        if request_user.__class__ != AnonymousUser:
            self.client.force_login(request_user)
        request = RequestFactory().post(reverse('account:blacklist', args=(0, 'Customers')))
        request.user = request_user
        permissions(request, user.id, 'Customers')
        permissions(request, staff.id, 'Customers')
        user = get_object_or_404(CustomUser, id=user.id)
        staff = get_object_or_404(CustomUser, id=staff.id)
        return (user, staff)

    def test_change_permissions_by_anonymous(self):
        user, staff = self.permissions_for_blocke(AnonymousUser())
        self.assertFalse(user.is_staff)
        self.assertTrue(staff.is_staff)

    def test_change_permissions_by_user(self):
        user, staff = self.permissions_for_blocke(self.user)
        self.assertFalse(user.is_staff)
        self.assertTrue(staff.is_staff)

    def test_change_permissions_by_staff(self):
        user, staff = self.permissions_for_blocke(self.staff)
        self.assertTrue(user.is_staff)
        self.assertTrue(staff.is_staff)

    def test_change_permissions_by_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='superuser@gmail.com',
            password='*qwerty#',
            user_name='SuperUser'
        )
        user, staff = self.permissions_for_blocke(superuser)
        self.assertTrue(user.is_staff)
        self.assertFalse(staff.is_staff)
