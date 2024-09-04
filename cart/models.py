from django.db import models
from django.db import models
from django.conf import settings
from shop.models import Product  # shopアプリで定義されているProductモデルをインポート
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cartitem_set.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitem_set', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # カラーとサイズの追加
    color = models.CharField(max_length=50)  # カラーの情報を保存するフィールド
    size = models.CharField(max_length=50)   # サイズの情報を保存するフィールド
    
    def __str__(self):
        return f"{self.product.title} ({self.color}, {self.size}) x{self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
