# cart/context_processors.py

from .models import Cart, CartItem
from decimal import Decimal

def cart_total_price(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # カートに関連するCartItemオブジェクトを使って合計金額を計算します
            total_price = sum(Decimal(item.product.price) * item.quantity for item in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            total_price = Decimal('0.00')
    else:
        total_price = Decimal('0.00')
    
    return {'total_price': total_price}
