from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView

from VolixProductsCategory.models import ProductCategory
from VolixTag.models import Tag
from .models import Product
from VolixOrder.forms import UserNewOrderForm


# Create your views here.

class ProductsList(ListView):
    template_name = 'products_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.get_active_products()


class ProductsListByCategory(ListView):
    template_name = 'products_list.html'
    paginate_by = 1

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        print(category_name)
        categories = ProductCategory.objects.filter(name__iexact=category_name)
        if categories is None:
            raise Http404('صفحه مورد نظر یافت نشد!')

        return Product.objects.get_product_by_category(category_name)


def products_categories_partial(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'categories_view_partial.html', context)


def product_detail(request, *args, **kwargs):
    product_id = kwargs['product_id']
    title = kwargs['title']
    new_order_form = UserNewOrderForm(request.POST or None, initial=({'product_id':product_id}))

    # Debug: Print form data
    print(f"Product detail - Product ID: {product_id}")
    print(f"Product detail - Request method: {request.method}")
    if request.method == 'POST':
        print(f"Product detail - POST data: {request.POST}")
        print(f"Product detail - Form is valid: {new_order_form.is_valid()}")
        if not new_order_form.is_valid():
            print(f"Product detail - Form errors: {new_order_form.errors}")

    product = Product.objects.get_product_by_id(product_id)
    if product is None:
        raise Http404('محصول یافت نشد')

    related_products = Product.objects.get_queryset().filter(categories__product=product).distinct()
    print(related_products)

    context = {
        'product': product,
        'related_products':related_products,
        'new_order_form':new_order_form
    }

    tag = Tag.objects.first()
    #print(tag)
    # print(tag.products.all())
    # print(product)
    print(product.tag_set.all())

    return render(request, 'product_detail.html', context)


class SearchProducts(ListView):
    template_name = 'products_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            return Product.objects.search_products(query)

        return Product.objects.get_active_products()
