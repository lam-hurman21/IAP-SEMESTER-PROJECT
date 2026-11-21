from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Product


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember me for 14 days')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'image', 'image_alt', 'is_active')
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
