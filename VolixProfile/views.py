from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required(login_url='/login')
def profile_main_page(request):

    context = {}
    return render(request,'profile_main_page.html',context)
@login_required(login_url='/login')
def profile_user_order(request):
    # user_id = request.user.id
    context = {}
    return render(request,'profile_user_orders.html',context)
@login_required(login_url='/login')
def profile_sidebar(request):
    context = {}
    return render(request,'profile_sidebar.html',context)