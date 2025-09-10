from django.urls import path
from . import views
from VolixProfile.views import profile_main_page , profile_user_order

app_name = 'VolixProfile'

urlpatterns = [
    path('profile',profile_main_page),
    path('profile/orders',profile_user_order , name='orders'),

]