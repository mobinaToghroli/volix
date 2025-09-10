from django.contrib.auth import authenticate, login , get_user_model ,logout
from django.shortcuts import render, redirect
from .forms import loginForm , registerForm
from django.contrib.auth import login as auth_login
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



#AUTH section
def login_page(request):

    login_form = loginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')

        password = login_form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile')
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





User = get_user_model()
def register_page(request):
    register_form = registerForm(request.POST or None)
    if register_form.is_valid():
        userName = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')

        new_user = User.objects.create_user(username=userName, email=email, password=password)
        print(new_user)
        return redirect('home')


    context = {
        'register_form': register_form,
    }
    return render(request, 'register.html', context)

def log_out(request):
    logout(request)
    return redirect('/login')
