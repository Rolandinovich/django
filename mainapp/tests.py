from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, Category
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'dbo.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/sale/')
        self.assertEqual(response.status_code, 200)

        for category in Category.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/product_details/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'accounts',
                     'ordersapp', 'cartapp')
