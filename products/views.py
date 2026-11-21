from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, ProductForm, RegistrationForm
from .models import Product


def index(request):
    products = Product.objects.select_related('category')
    if not (request.user.is_staff and request.user.has_perm('products.view_product')):
        products = products.filter(is_active=True)
    return render(request, 'products/index.html', {'products': products})


def about(request):
    return render(request, 'about.html')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('products:index')
    form = RegistrationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        request.session.set_expiry(0)
        messages.success(request, 'Your account has been created. Welcome to Campus Supply!')
        return redirect('products:index')
    return render(request, 'registration/register.html', {'form': form})


class CampusLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session.set_expiry(
            settings.SESSION_COOKIE_AGE if form.cleaned_data['remember_me'] else 0
        )
        return response


@login_required
def account(request):
    return render(request, 'registration/account.html')


@login_required
@require_http_methods(['GET', 'POST'])
def product_edit(request, pk=None):
    permission = 'products.add_product' if pk is None else 'products.change_product'
    if not (request.user.is_staff and request.user.has_perm(permission)):
        raise PermissionDenied
    product = get_object_or_404(Product, pk=pk) if pk is not None else None
    form = ProductForm(request.POST if request.method == 'POST' else None, instance=product)
    if request.method == 'POST' and form.is_valid():
        saved_product = form.save(commit=False)
        if product is None:
            saved_product.created_by = request.user
        saved_product.save()
        messages.success(request, 'Product saved successfully.')
        return redirect('products:index')
    return render(request, 'products/product_form.html', {'form': form, 'product': product})
