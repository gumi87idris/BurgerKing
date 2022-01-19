from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    # print(categories)
    return render(request, 'index.html',
                  {'categories': categories})

def products_list(request, slug):
    products = Product.objects.filter(category__slug=slug)       #-> это только внутри queryset
    return render(request, 'list.html',
                  {'products': products})

def product_detail(request, product_id):
    # product = Product.objects.get(pk=product_id)        # pk = primary key, можно id использовать
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'detail.html', locals())     # locals() все что находится на локальной
