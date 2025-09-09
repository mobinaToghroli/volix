from django.shortcuts import render
from .models import ContactUs

from .forms import ContactUsForm
# Create your views here.

def contact_us_page(request):

    contact_form = ContactUsForm(request.POST or None)
    if contact_form.is_valid():
        fullname = contact_form.cleaned_data.get('fullname')
        email = contact_form.cleaned_data.get('email')
        message = contact_form.cleaned_data.get('message')
        new_contact = ContactUs.objects.create(fullname=fullname, email=email, message=message)
        print(new_contact)

    context = {
        'contact_form': contact_form,
    }


    return render(request,'contact_us_page.html',context)