"""Database models for the marketplace application."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Store the role assigned to a Django user account.

    A user can be registered as either a buyer or a vendor. This model
    allows the application to enforce role-based permissions.
    """

    BUYER = 'buyer'
    VENDOR = 'vendor'

    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (VENDOR, 'Vendor'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        """Return a readable username and role label."""
        return f'{self.user.username} ({self.role})'


class Store(models.Model):
    """
    Represent a vendor-owned store.

    Each store belongs to one vendor. Vendors can create, update, and
    delete their own stores only.
    """

    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stores'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the store name."""
        return self.name


class Product(models.Model):
    """
    Represent a product sold inside a vendor store.

    Products are linked to stores so that ownership can be checked before
    allowing edit or delete actions.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the product name."""
        return self.name


class Cart(models.Model):
    """Represent a buyer's saved shopping cart."""

    buyer = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the cart owner."""
        return f"{self.buyer.username}'s Cart"


class CartItem(models.Model):
    """Represent one product and quantity inside a cart."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        """Calculate the cart item subtotal."""
        return self.product.price * self.quantity

    def __str__(self):
        """Return the related product name."""
        return self.product.name


class Order(models.Model):
    """Represent an order created after checkout."""

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    def __str__(self):
        """Return a readable order number."""
        return f'Order #{self.id}'


class OrderItem(models.Model):
    """Represent a purchased product inside an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        """Calculate the order item subtotal."""
        return self.price * self.quantity

    def __str__(self):
        """Return the purchased product name."""
        return self.product.name


class Review(models.Model):
    """
    Represent a product review submitted by a buyer.

    A review is marked as verified when the buyer has previously ordered
    the reviewed product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the review author."""
        return f'Review by {self.buyer.username}'
