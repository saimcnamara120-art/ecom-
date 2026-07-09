"""Forms for the marketplace application."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product
from .models import Review
from .models import Store
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """Collect registration details for buyers and vendors."""

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        """Define fields used by the registration form."""

        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role',
        ]


class StoreForm(forms.ModelForm):
    """Allow vendors to create and update stores."""

    class Meta:
        """Define fields used by the store form."""

        model = Store
        fields = [
            'name',
            'description',
        ]


class ProductForm(forms.ModelForm):
    """Allow vendors to create and update products."""

    class Meta:
        """Define fields used by the product form."""

        model = Product
        fields = [
            'store',
            'name',
            'description',
            'price',
            'quantity',
        ]


class ReviewForm(forms.ModelForm):
    """Allow buyers to submit product reviews."""

    class Meta:
        """Define fields used by the review form."""

        model = Review
        fields = [
            'rating',
            'comment',
        ]
