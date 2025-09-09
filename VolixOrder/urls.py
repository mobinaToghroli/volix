from django.urls import path
from . import views
from .views import add_new_order, cart, send_request, verify

app_name = 'VolixOrder'

urlpatterns = [
    path('add_new_order/', add_new_order, name='add_new_order'),
    path('cart/', cart, name='cart'),
    path('request/', send_request, name='send_request'),
    path('verify/', verify, name='verify'),
]