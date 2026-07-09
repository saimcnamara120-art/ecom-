"""Admin registrations for marketplace models."""

from django.contrib import admin

from .models import Cart
from .models import CartItem
from .models import Order
from .models import OrderItem
from .models import Product
from .models import Review
from .models import Store
from .models import UserProfile

admin.site.register(UserProfile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
