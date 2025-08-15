from django import forms


class loginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),

    )

from django.contrib.auth.models import User

class registerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تایید رمز عبور'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
        }
# nafahmidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "رمزها یکسان نیستند.")
