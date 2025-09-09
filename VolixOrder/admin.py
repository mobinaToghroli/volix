from django.contrib import admin
from .models import Order , OrderDetail
import VolixOrder

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)