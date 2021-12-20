from django.test import TestCase
from catalog.models import Product
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from cart.views import cart_add, cart_remove
from decimal import Decimal


class CartTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title='Product', description='Nice', price=1000, quantity=10)
        self.factory = RequestFactory()
        self.session = self.client.session

    def test_path_cart_add(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'), 302, 200)

    def test_cart_add(self):
        request = self.factory.post(reverse('cart:cart_add', args=[self.product.id]))
        request.POST = {'quantity': 5, 'update': False}
        request.session = self.session
        cart_add(request, self.product.id)
        self.assertTrue(request.session.get('cart'))

    def test_path_cart_remove(self):
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'), 302, 200)

    def test_cart_remove(self):
        request = self.factory.post(reverse('cart:cart_remove', args=[self.product.id]))
        request.POST = {'quantity': 5, 'update': False}
        request.session = self.session
        request.session['cart'] = {'2': {'quantity': 5, 'price': str(Decimal('1000.00'))}}
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        cart_remove(request, self.product.id)
        self.assertFalse(request.session.get('cart'))
