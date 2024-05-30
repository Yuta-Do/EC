# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.all().filter(cart=cart)
    total_price = sum(item.total for item in cart_items)  # カート内の合計金額を計算
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    # 対象の商品を取得
    product = get_object_or_404(Product, id=product_id)
    
    # カートに商品を追加する処理
    if request.method == 'POST':
        # POST リクエストから数量を取得
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
            except CartItem.DoesNotExist:
                cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            
            # カート内の合計金額を計算
            cart_item.total = cart_item.product.price * cart_item.quantity
            
            # 保存
            cart_item.save()
        
        return redirect('cart:cart')
    return redirect('cart:cart')

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart:cart')
