from django.urls import path
from .views import ProductsList , product_detail , SearchProducts , ProductsListByCategory

app_name = 'Volix_Products'

urlpatterns = [

    path('productss', ProductsList.as_view(), name='products_list'),
    path('productss/<product_id>/<title>',product_detail ),
    path('productss/search',SearchProducts.as_view() ),
    path('productss/<category_name>', ProductsListByCategory.as_view()),


]