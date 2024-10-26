# blog/forms.py

from django import forms
from .models import Post, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image_url']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use.')
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class DeleteUserForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Please confirm you want to delete your account')
