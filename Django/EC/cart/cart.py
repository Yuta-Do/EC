# cart/cart.py

from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # セッションにカートがない場合は空のカートを作成
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(Product.objects.get(id=product_id).price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        self.session.modified = True
    
    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        for product in products:
            cart_items.append({
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity'],
                'price': self.cart[str(product.id)]['price'],
                'total_price': Decimal(self.cart[str(product.id)]['price']) * self.cart[str(product.id)]['quantity']
            })
        return cart_items
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
