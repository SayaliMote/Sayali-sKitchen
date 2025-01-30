from django.test import TestCase, RequestFactory
from shop.models import Product
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView
from unittest.mock import patch

class SearchResultsListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product1 = Product.objects.create(name="Test Product 1", description="Test description 1", price=10.00, stock=100)
        self.product2 = Product.objects.create(name="Test Product 2", description="Test description 2", price=20.00, stock=200)

    def test_search_results_list_view(self):
        url = reverse('search_results')
        request = self.factory.get(url, {'q': 'test'})
        response = SearchResultsListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_get_queryset(self):
        view = SearchResultsListView()
        view.request = RequestFactory().get('/search?q=test')
        view.request.GET['q'] = 'test'
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.product1 in queryset)
        self.assertTrue(self.product2 in queryset)

    def test_get_context_data(self):
        view = SearchResultsListView()
        context = view.get_context_data(query='test')
        self.assertIn('query', context)
        self.assertEqual(context['query'], 'test')
