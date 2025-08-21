from django import forms
from django.contrib.auth import get_user_model
from django.core import validators


class loginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),

    )


User = get_user_model()


class registerForm(forms.Form):
    username = forms.CharField(

        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        validators=[validators.MaxLengthValidator(limit_value=20, message='نام کاربری نباید بیشتر از 20 کاراکتر باشد !')],
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        validators=[validators.EmailValidator('ایمیل نامعتبر است!')],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),

    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' confirm password'}),

    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        query = User.objects.filter(username=username)

        if query.exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email=email)

        if query.exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords doesn't match")
        return data
