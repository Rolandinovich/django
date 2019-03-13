from django.test import TestCase
from mainapp.models import Product, Category


class ProductsTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(title="стулья")
        self.product_1 = Product.objects.create(title="стул 1",
                                                category=category,
                                                cost=1999.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(title="стул 2",
                                                category=category,
                                                cost=2998.1,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(title="стул 3",
                                                category=category,
                                                cost=998.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(title="стул 1")
        product_2 = Product.objects.get(title="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(title="стул 1")
        product_2 = Product.objects.get(title="стул 2")
        self.assertEqual(str(product_1), 'стул 1')
        self.assertEqual(str(product_2), 'стул 2')

    def test_product_get_items(self):
        product_1 = Product.objects.get(title="стул 1")
        product_3 = Product.objects.get(title="стул 3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
