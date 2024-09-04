from django.contrib import admin
from .models import Product, Attribute, AttributeValue, ProductAttribute, ColorImage,Category
from cart.models import Cart,CartItem
from registration.models import User,UserManager

# 既に登録されているか確認し、まだ登録されていなければ登録する
from django.contrib.admin.sites import AlreadyRegistered

models = [Product, Attribute, AttributeValue, ProductAttribute, ColorImage,Category,Cart,CartItem,User]

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
