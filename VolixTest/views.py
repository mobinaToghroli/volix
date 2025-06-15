from django.shortcuts import render
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

def products_page(request):
    context = {}
    return render(request, 'products.html', context)