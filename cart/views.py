from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shop.models import Product, AttributeValue,ColorImage

from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # POSTデータからカラーとサイズを取得
    color = request.POST.get('color')
    size = request.POST.get('size')

    # 既に同じ商品、カラー、サイズのアイテムがあるか確認
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        size=size,
        defaults={'quantity': 1}
    )

    # 同じアイテムが既にあれば数量を増やす
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')




from decimal import Decimal


@login_required
def cart_detail(request):
    # 現在のユーザーのカートを取得
    cart = get_object_or_404(Cart, user=request.user)
    
    # カート内のアイテムを取得
    cart_items = CartItem.objects.filter(cart=cart)
    total_item_count = sum(item.quantity for item in cart_items)

     # トータル価格を計算
    
    extra_shipping_fee = 0
   
    cart_items_with_images = []
    for item in cart_items:
        if item.product.shipping_size == "normal":
            continue
        elif item.product.shipping_size == "large":
            extra_shipping_fee+=50
        elif item.product.shipping_size == "extra_large":
            extra_shipping_fee+=100


    for item in cart_items:
        # カートアイテムの color が AttributeValue オブジェクトであることを確認
        if isinstance(item.color, str):
            # 文字列が渡されている場合は、AttributeValue を取得
            color_value = AttributeValue.objects.filter(value=item.color).first()
        else:
            # すでに AttributeValue オブジェクトが渡されている場合
            color_value = item.color
        
        # color_value を使って ColorImage を取得
        color_image = ColorImage.objects.filter(product=item.product, color=color_value).first()
        cart_items_with_images.append({
            'item': item,
            'color_image': color_image
        })

    total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
    order_total_price = total_price + extra_shipping_fee +150
    total_shipping_fee = extra_shipping_fee +150

    context = {
        "total_shipping_fee":total_shipping_fee,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_item_count': total_item_count,  # 合計数量をコンテキストに追加
        'cart_items_with_images': cart_items_with_images,
        "extra_shipping_fee":extra_shipping_fee,
        "order_total_price":order_total_price,

    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    
    # カート内のアイテムを取得
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    
    # アイテムを削除
    cart_item.delete()
    
    # カートの詳細ページを再表示
    cart_items = cart.cartitem_set.all()
    total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)

    total_item_count = sum(item.quantity for item in cart_items)

    cart_items_with_images = []
    for item in cart_items:
        # カートアイテムの color が AttributeValue オブジェクトであることを確認
        if isinstance(item.color, str):
            # 文字列が渡されている場合は、AttributeValue を取得
            color_value = AttributeValue.objects.filter(value=item.color).first()
        else:
            # すでに AttributeValue オブジェクトが渡されている場合
            color_value = item.color

    extra_shipping_fee = 0
    for item in cart_items:
        if item.product.shipping_size == "normal":
            continue
        elif item.product.shipping_size == "large":
            extra_shipping_fee+=50
        elif item.product.shipping_size == "extra_large":
            extra_shipping_fee+=100
        
        # color_value を使って ColorImage を取得
        color_image = ColorImage.objects.filter(product=item.product, color=color_value).first()
        cart_items_with_images.append({
            'item': item,
            'color_image': color_image
        })
    order_total_price = total_price + extra_shipping_fee +150
    total_shipping_fee = extra_shipping_fee +150

    context = {
        "total_shipping_fee":total_shipping_fee,
    
        'cart_items': cart_items,
        'total_price': total_price,
        'total_item_count': total_item_count,  # 合計数量をコンテキストに追加
        'cart_items_with_images': cart_items_with_images,
        "extra_shipping_fee":extra_shipping_fee,
        "order_total_price":order_total_price,
    }
    
    return render(request, 'cart/cart_detail.html', context)