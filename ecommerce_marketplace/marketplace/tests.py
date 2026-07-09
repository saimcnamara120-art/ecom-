"""Tests for the marketplace application."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Product
from .models import Store
from .models import UserProfile


class MarketplaceModelTests(TestCase):
    """Test the main database models."""

    def test_store_and_product_creation(self):
        """Confirm that a vendor can own a store and product."""
        vendor = User.objects.create_user(
            username='vendor1',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=vendor,
            role=UserProfile.VENDOR
        )
        store = Store.objects.create(
            vendor=vendor,
            name='Tech Store',
            description='Technology products.'
        )
        product = Product.objects.create(
            store=store,
            name='Phone',
            description='Smart phone.',
            price=499.99,
            quantity=10
        )

        self.assertEqual(store.name, 'Tech Store')
        self.assertEqual(product.name, 'Phone')


class MarketplaceViewTests(TestCase):
    """Test that public pages load correctly."""

    def setUp(self):
        """Create sample data for view tests."""
        self.vendor = User.objects.create_user(
            username='vendor1',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.vendor,
            role=UserProfile.VENDOR
        )
        self.store = Store.objects.create(
            vendor=self.vendor,
            name='Tech Store',
            description='Technology products.'
        )
        Product.objects.create(
            store=self.store,
            name='Phone',
            description='Smart phone.',
            price=499.99,
            quantity=10
        )

    def test_home_page_loads(self):
        """Confirm the home page returns HTTP 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_page_loads(self):
        """Confirm products appear on the product list."""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Phone')

    def test_store_list_page_loads(self):
        """Confirm stores appear on the store list."""
        response = self.client.get(reverse('store_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tech Store')
