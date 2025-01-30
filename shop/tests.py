from django.test import TestCase
from django.urls import reverse
from .models import Type, Product

class ShopModelsTestCase(TestCase):
    def setUp(self):
        self.type = Type.objects.create(name="Test Type", description="Test description")
        self.product = Product.objects.create(name="Test Product", description="Test description", type=self.type, price=10.00, stock=100)

    def test_type_str(self):
        self.assertEqual(str(self.type), "Test Type")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_type_absolute_url(self):
        url = reverse('shop:products_by_type', args=[self.type.id])
        self.assertEqual(self.type.get_absolute_url(), url)

    def test_product_absolute_url(self):
        url = reverse('shop:product_detail', args=[self.type.id, self.product.id])
        self.assertEqual(self.product.get_absolute_url(), url)


