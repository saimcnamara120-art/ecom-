"""Views for marketplace pages and user actions."""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import ProductForm
from .forms import RegisterForm
from .forms import ReviewForm
from .forms import StoreForm
from .models import Order
from .models import OrderItem
from .models import Product
from .models import Store
from .models import UserProfile


def get_profile(user):
    """
    Return the profile for the supplied user.

    This helper keeps repeated profile lookups in one place and prevents
    views from failing silently when a profile is missing.
    """
    return get_object_or_404(UserProfile, user=user)


def is_vendor(user):
    """Return True when the authenticated user has the vendor role."""
    if not user.is_authenticated:
        return False

    return (
        hasattr(user, 'userprofile')
        and user.userprofile.role == UserProfile.VENDOR
    )


def is_buyer(user):
    """Return True when the authenticated user has the buyer role."""
    if not user.is_authenticated:
        return False

    return (
        hasattr(user, 'userprofile')
        and user.userprofile.role == UserProfile.BUYER
    )


def require_vendor(request):
    """Redirect non-vendors away from vendor-only pages."""
    if is_vendor(request.user):
        return None

    messages.error(
        request,
        'Only vendors can access that page.'
    )
    return redirect('dashboard')


def home(request):
    """Display the public home page."""
    return render(request, 'marketplace/home.html')


def register(request):
    """Create a buyer or vendor account and matching profile."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            messages.success(
                request,
                'Account created successfully. Please log in.'
            )
            return redirect('login')
    else:
        form = RegisterForm()

    return render(
        request,
        'marketplace/register.html',
        {'form': form}
    )


def user_login(request):
    """Authenticate a user and redirect to the dashboard."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'marketplace/login.html')


def user_logout(request):
    """Log out the active user and return to the home page."""
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """Display a dashboard customised to the user's role."""
    profile = get_profile(request.user)
    context = {'profile': profile}

    if profile.role == UserProfile.VENDOR:
        context['stores'] = Store.objects.filter(
            vendor=request.user
        )
        context['products'] = Product.objects.filter(
            store__vendor=request.user
        )
    else:
        context['products'] = Product.objects.all()

    return render(
        request,
        'marketplace/dashboard.html',
        context
    )


def store_list(request):
    """Display all marketplace stores."""
    stores = Store.objects.all()

    return render(
        request,
        'marketplace/store_list.html',
        {'stores': stores}
    )


@login_required
def add_store(request):
    """Allow vendors to create a new store."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    if request.method == 'POST':
        form = StoreForm(request.POST)

        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()

            messages.success(request, 'Store created successfully.')
            return redirect('store_list')
    else:
        form = StoreForm()

    return render(
        request,
        'marketplace/store_form.html',
        {'form': form}
    )


@login_required
def edit_store(request, pk):
    """Allow vendors to edit stores they own."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    store = get_object_or_404(
        Store,
        pk=pk,
        vendor=request.user
    )

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)

        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully.')
            return redirect('store_list')
    else:
        form = StoreForm(instance=store)

    return render(
        request,
        'marketplace/store_form.html',
        {
            'form': form,
            'store': store,
        }
    )


@login_required
def delete_store(request, pk):
    """Allow vendors to delete stores they own."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    store = get_object_or_404(
        Store,
        pk=pk,
        vendor=request.user
    )

    if request.method == 'POST':
        store.delete()
        messages.success(request, 'Store deleted successfully.')
        return redirect('store_list')

    return render(
        request,
        'marketplace/delete_store.html',
        {'store': store}
    )


def product_list(request):
    """Display all products available in the marketplace."""
    products = Product.objects.all()

    return render(
        request,
        'marketplace/product_list.html',
        {'products': products}
    )


def product_detail(request, pk):
    """Display one product and its related reviews."""
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        'marketplace/product_detail.html',
        {'product': product}
    )


@login_required
def add_product(request):
    """Allow vendors to add products to their own stores."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    vendor_stores = Store.objects.filter(vendor=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.fields['store'].queryset = vendor_stores

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
        form.fields['store'].queryset = vendor_stores

    return render(
        request,
        'marketplace/product_form.html',
        {'form': form}
    )


@login_required
def edit_product(request, pk):
    """Allow vendors to edit products in their own stores."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    product = get_object_or_404(
        Product,
        pk=pk,
        store__vendor=request.user
    )
    vendor_stores = Store.objects.filter(vendor=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        form.fields['store'].queryset = vendor_stores

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        form.fields['store'].queryset = vendor_stores

    return render(
        request,
        'marketplace/product_form.html',
        {
            'form': form,
            'product': product,
        }
    )


@login_required
def delete_product(request, pk):
    """Allow vendors to delete products in their own stores."""
    redirect_response = require_vendor(request)

    if redirect_response is not None:
        return redirect_response

    product = get_object_or_404(
        Product,
        pk=pk,
        store__vendor=request.user
    )

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')

    return render(
        request,
        'marketplace/delete_product.html',
        {'product': product}
    )


@login_required
def add_to_cart(request, pk):
    """Add a product to the buyer's session cart."""
    if not is_buyer(request.user):
        messages.error(
            request,
            'Only buyers can add products to the cart.'
        )
        return redirect('dashboard')

    product = get_object_or_404(Product, pk=pk)

    if product.quantity <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_detail', pk=pk)

    cart_data = request.session.get('cart', {})
    product_id = str(product.id)
    cart_data[product_id] = cart_data.get(product_id, 0) + 1

    request.session['cart'] = cart_data
    request.session.modified = True

    messages.success(request, 'Product added to cart.')
    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    """Remove a product from the buyer's session cart."""
    cart_data = request.session.get('cart', {})
    product_id = str(pk)

    if product_id in cart_data:
        del cart_data[product_id]

    request.session['cart'] = cart_data
    request.session.modified = True

    messages.success(request, 'Product removed from cart.')
    return redirect('cart')


@login_required
def cart(request):
    """Display cart contents and total price for buyers."""
    if not is_buyer(request.user):
        messages.error(request, 'Only buyers can view the cart.')
        return redirect('dashboard')

    cart_data = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            }
        )

    return render(
        request,
        'marketplace/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


@login_required
def checkout(request):
    """Create an order from cart items and reduce stock levels."""
    if not is_buyer(request.user):
        messages.error(request, 'Only buyers can checkout.')
        return redirect('dashboard')

    cart_data = request.session.get('cart', {})

    if not cart_data:
        messages.error(request, 'Your cart is empty.')
        return redirect('product_list')

    order = Order.objects.create(buyer=request.user)
    total = Decimal('0.00')
    invoice_lines = []

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, pk=product_id)

        if product.quantity < quantity:
            messages.error(
                request,
                f'Not enough stock for {product.name}.'
            )
            order.delete()
            return redirect('cart')

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        product.quantity -= quantity
        product.save()

        subtotal = product.price * quantity
        total += subtotal
        invoice_lines.append(
            f'{product.name} x {quantity}: ${subtotal}'
        )

    order.total_price = total
    order.save()
    request.session['cart'] = {}
    request.session.modified = True

    send_mail(
        subject=f'Invoice for Order #{order.id}',
        message=(
            'Thank you for your order.\n\n'
            + '\n'.join(invoice_lines)
            + f'\n\nTotal: ${total}'
        ),
        from_email=None,
        recipient_list=[request.user.email],
        fail_silently=True
    )

    messages.success(request, 'Checkout complete.')
    return redirect('orders')


@login_required
def orders(request):
    """Display order history for buyers or vendor-related orders."""
    if is_vendor(request.user):
        user_orders = Order.objects.filter(
            items__product__store__vendor=request.user
        ).distinct().order_by('-created_at')
    else:
        user_orders = Order.objects.filter(
            buyer=request.user
        ).order_by('-created_at')

    return render(
        request,
        'marketplace/orders.html',
        {'orders': user_orders}
    )


@login_required
def add_review(request, pk):
    """Allow buyers to review a product."""
    if not is_buyer(request.user):
        messages.error(request, 'Only buyers can leave reviews.')
        return redirect('dashboard')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.buyer = request.user
            review.verified = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product
            ).exists()
            review.save()

            messages.success(request, 'Review added successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        'marketplace/review_form.html',
        {
            'form': form,
            'product': product,
        }
    )
