from django.shortcuts import render
from .models import Product, Category
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    categories = Category.objects.all()
    products_by_category = {}
    for category in categories:
        products_by_category[category] = Product.objects.filter(category=category)
    return render(request, 'products/product_list.html', {'products_by_category': products_by_category})
