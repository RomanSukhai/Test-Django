from django.contrib.messages import get_messages
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, User
from django.test import TestCase, Client


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100.00, stock=10)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'New Product', 'description': 'wdwddwwddwdwwd', 'price': 50.00,
                'stock': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)


class OrderViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user@example.com', 'password')
        self.client.login(email='user@example.com', password='password')
        self.product = Product.objects.create(name='Test Product', price=34, stock=10)
        self.create_order_url = reverse('create_order')

    def test_create_order_success(self):
        response = self.client.post(self.create_order_url, {'product': self.product.id, 'quantity': 9})
        self.assertRedirects(response, reverse('home'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)

    def test_create_order_insufficient_stock(self):
        response = self.client.post(self.create_order_url, {'product': self.product.id, 'quantity': 20})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Недостатня кількість товару на складі.', messages)


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user@example.com', 'password')
        self.home_url = reverse('home')

    def test_home_view_authenticated(self):
        self.client.login(email='user@example.com', password='password')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('login'))


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_success(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, reverse('login'))

    def test_register_duplicate_email(self):

        User.objects.create_user(email='existinguser@example.com', password='password')

        response = self.client.post(self.register_url, {
            'email': 'existinguser@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertIn('User with this Email already exists.', response.content.decode())


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='romansukhai@gmail.com', password='namor2004', first_name='roman',
                                             last_name='sukhai')
        self.product = Product.objects.create(name="Test Product", description='wdwddwwddwdwwd', price=100.00, stock=10)

    def test_create_order_with_valid_data(self):
        url = reverse('order-list')
        data = {'product': self.product.id, 'user': self.user.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_with_invalid_data(self):
        url = reverse('order-list')
        data = {'product': self.product.id, 'user': self.user.id, 'quantity': 20}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomUserViewSetTestCase(APITestCase):

    def test_create_user(self):
        url = reverse('user-list')
        data = {'email': 'romansukhai@gmail.com', 'password': 'namor2004', 'first_name': 'roman', 'last_name': 'sukhai'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class APIRootViewTestCase(APITestCase):
    def test_api_root_get_request(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('orders', response.data)
        self.assertIn('users', response.data)
