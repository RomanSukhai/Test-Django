from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, User
from django.contrib.auth import get_user_model

User = get_user_model()


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
        data = {'name': 'New Product', 'description':'wdwddwwddwdwwd', 'price': 50.00, 'stock': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='romansukhai@gmail.com', first_name='roman', last_name='sukhai')
        self.product = Product.objects.create(name="Test Product",description='wdwddwwddwdwwd', price=100.00, stock=10)
        self.client.force_authenticate(user=self.user)

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
    def setUp(self):
        self.user_data = {'email': 'romansukhai@gmial.com','first_name': 'roman', 'last_name': 'sukhai' }

    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 0)


class APIRootViewTestCase(APITestCase):
    def test_api_root_get_request(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('orders', response.data)
        self.assertIn('users', response.data)

