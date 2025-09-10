from django import forms


class UserEditProfileForm(forms.Form):
    first_name = forms.CharField(

        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد نمایید'}),

    )

    last_name = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد نمایید'}),
    )



