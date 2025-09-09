from django import forms




class ContactUsForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control' , 'maxlenght':'150'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),
    )