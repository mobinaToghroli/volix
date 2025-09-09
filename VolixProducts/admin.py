from django.contrib import admin
from VolixProducts.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'title' , 'price' , 'active']


    class Meta :
        model = Product

admin.site.register(Product , ProductAdmin)