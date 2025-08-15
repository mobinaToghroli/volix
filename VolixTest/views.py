from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import loginForm
#partial render fb
def header(request):
    context = {}
    return render(request,'base/header.html',context)

def footer(request):
    context = {}
    return render(request,'base/footer.html',context)

def home_page(request):
    context = {}

    return render(request,'home_page.html',context)

def contact_us_page(request):
    context = {}
    return render(request,'contact_us.html',context)

#AUTH section
def login_page(request):

    login_form = loginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')

        password = login_form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Login failed')

    context = {
        'login_form': login_form
    }
    return render(request,'login_page.html',context)

#AUTH section


def products_page(request):
    context = {}
    return render(request, 'products.html', context)


from .forms import registerForm
from django.contrib.auth import login as auth_login


def register_page(request):
    form = registerForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        auth_login(request, user)
        return redirect('/')

    return render(request, 'register_page.html', {'form': form})
