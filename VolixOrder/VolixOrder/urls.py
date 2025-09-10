from django.urls import path
from . import views
from .views import add_new_order, cart, send_request, verify , remove_cart_item

app_name = 'VolixOrder'

urlpatterns = [
    path('add_new_order/', add_new_order, name='add_new_order'),
    path('cart/', cart, name='cart'),
    path('remove_cart_item/<detail_id>',remove_cart_item, name='remove_cart_item'),
    path('request/', send_request, name='send_request'),
    path('verify/<order_id>', verify, name='verify'),
]