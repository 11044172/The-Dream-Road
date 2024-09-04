from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.shortcuts import render
from .models import Product, ProductAttribute, AttributeValue
from cart.models import Cart

from django.shortcuts import get_object_or_404, render
from .models import Product, ProductAttribute,ColorImage

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductAttribute
from cart.models import Cart

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart

@login_required  # Ensure that only logged-in users can access the account page
def account_view(request):
    user = request.user

    # Get the user's cart
    cart = Cart.objects.filter(user=user).first()
    cart_items = cart.cartitem_set.all() if cart else []

    # Get order history (if you have an Order model)
    # orders = Order.objects.filter(user=user).order_by('-created_at')  # Assuming you have an 'Order' model

    context = {
        'user': user,
        'cart_items': cart_items,
        # 'orders': orders,  # Pass orders to the template for display
    }

    return render(request, 'shop/account.html', context)




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
    else:
        cart_items = []

    # 色のリストを取得
    colors = ProductAttribute.objects.filter(product=product, attribute__name="Color").distinct()

    # 色ごとのサイズを取得するための辞書
    color_size_map = {}
    for color in colors:
        sizes = ProductAttribute.objects.filter(
            product=product,
            attribute__name="Size",
            product__attributes__attribute__name="Color",
            product__attributes__value=color.value
        ).distinct()

        size_values = {size.value.id: size.value.value for size in sizes}
        color_size_map[color.value] = size_values

    # カラー画像を直接取得
    color_images = ColorImage.objects.filter(product=product)
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()  # 'cartitem_set' を使って関連アイテムを取得
        except Cart.DoesNotExist:
            cart_items = []
    else:
        cart_items = []

    context = {
        'product': product,
        'colors': colors,
        'color_images': color_images,  # 画像URLをテンプレートに渡す
        'color_size_map': color_size_map,
        'cart_items': cart_items,
    }
    return render(request, 'shop/product_detail.html', context)






def index1(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        category = None
        products = Product.objects.all()
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()  # 'cartitem_set' を使って関連アイテムを取得
        except Cart.DoesNotExist:
            cart_items = []
    else:
        cart_items = []
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'cart_items': cart_items,  # カート内のアイテムを含む
    }
    
    return render(request, 'shop/index.html', context)


import re
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Product, Attribute, AttributeValue, ProductAttribute, ColorImage

# ヘルパー関数
def get_or_create_attribute(name):
    attribute, created = Attribute.objects.get_or_create(name=name)
    return attribute

def get_or_create_attribute_value(attribute, value):
    attr_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=value)
    return attr_value

# 商品データを取得する関数
def get_product_data(url, category):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 商品のタイトル、画像、価格、説明文を抽出
    product_title_tag = soup.find('h1', class_='ttl-name')
    product_title = product_title_tag.text.strip() if product_title_tag else 'タイトルなし'
    
    product_image_tag = soup.find('img', {'onerror': "this.src='https://cdn.grail.bz/images/goods/noimage_692_934.jpg';this.onerror=null;"})
    product_image = product_image_tag['src'] if product_image_tag else 'Image not found'
    
    product_price_tag = soup.find('p', class_='txt-price')
    if product_price_tag:
        product_price_text = product_price_tag.text.strip()
        match = re.search(r'¥([\d,]+)', product_price_text)
        if match:
            product_price = match.group(1).replace(',', '')
            product_price = float(product_price)
            tw_price = int(round(product_price * 0.34, -1))
        else:
            tw_price = 'Price not found'
    else:
        tw_price = 'Price not found'
    
    product_description_tag = soup.find('div', class_='tab-content is-visible')
    product_description = product_description_tag.text.strip() if product_description_tag else 'Description not found'
    
    # Productモデルにデータを保存
    product = Product(
        title=product_title,
        price=tw_price,
        image=product_image,
        description=product_description,
        category=category,
        url=url
    )
    product.save()
    
    # 色やサイズの属性を作成
    color_attribute = get_or_create_attribute('Color')
    size_attribute = get_or_create_attribute('Size')
    
    # 商品の色とサイズの情報を抽出
    color_sections = soup.find_all('div', class_='card-item-addcart')
    
    for section in color_sections:
        # カラー名を抽出
        color_name_tag = section.find('p', class_='txt-info')
        color_name = color_name_tag.text.strip() if color_name_tag else 'カラーなし'
        color_value = get_or_create_attribute_value(color_attribute, color_name)
        
        # カラー画像URLを抽出
        image_tag = section.find('img')
        color_image_url = image_tag['src'] if image_tag else 'Image not found'
        
        # カラー属性を保存
        ProductAttribute.objects.create(product=product, attribute=color_attribute, value=color_value)
        
        # カラー画像を保存
        ColorImage.objects.create(product=product, color=color_value, image_url=color_image_url)
        
        # サイズオプションを抽出
        size_select = section.find('select', class_='size-select')
        if size_select:
            size_options = size_select.find_all('option')
            for option in size_options:
                size_text = option.text.split('/')[0].strip()  # サイズ名を抽出 (例: 'S')
                size_value = get_or_create_attribute_value(size_attribute, size_text)
                
                # サイズ属性を保存
                ProductAttribute.objects.create(product=product, attribute=size_attribute, value=size_value)
        else:
            print(f"サイズセレクトが見つかりませんでした: {color_name}")
    
    return product


from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, ColorImage, ProductAttribute

from django.shortcuts import render
from .models import Product, ColorImage, ProductAttribute, Attribute, AttributeValue

from django.shortcuts import render, get_object_or_404

def scrape_product_view(request, category_id=None):
    categories = Category.objects.all()

    if request.method == 'POST':
        url = request.POST.get('url')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)

        # 商品データを取得
        product = get_product_data(url, category)

        # 色のリストを取得
        colors = ProductAttribute.objects.filter(product=product, attribute__name="Color").distinct()

        # 色ごとのサイズを取得するための辞書
        color_size_map = {}
        for color in colors:
            sizes = ProductAttribute.objects.filter(
                product=product,
                attribute__name="Size",
                product__attributes__attribute__name="Color",
                product__attributes__value=color.value
            ).distinct()

            # サイズのリストを色に対応付ける
            size_values = {size.value.id: size.value.value for size in sizes}
            color_size_map[color.value] = size_values
            color_images = ColorImage.objects.filter(product=product)

    
    

        context = {
            'product': product,
            'colors': colors,
            'color_size_map': color_size_map,
            'categories': categories,
            'color_images': color_images, 
        }
        return render(request, 'shop/product_preview.html', context)

    context = {
        'categories': categories,
    }
    return render(request, 'shop/scrape_form.html', context)







from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Product, Category, Attribute, AttributeValue, ProductAttribute, ColorImage

def save_product_view(request, product_id):
    # product_id を使ってデータベースから Product オブジェクトを取得
    product = get_object_or_404(Product, id=product_id)
    old_colors = ProductAttribute.objects.filter(product=product, attribute__name="Color").distinct()
    
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        image = request.POST.get('image')
        price = request.POST.get('price')
        colors = request.POST.getlist('colors')  # カラーリスト
        sizes = request.POST.getlist('sizes')    # サイズリスト
        shipping_size = request.POST.get('shipping_size')

        # 変更点があるかどうかを確認して、必要に応じて更新
        if title and title != product.title:
            product.title = title
        
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            product.category = category.name  # カテゴリ名を保存

        if description and description != product.description:
            product.description = description
        
        if image and image != product.image:
            product.image = image
        
        if price and price != product.price:
            product.price = price
        
        if shipping_size and shipping_size != product.shipping_size:
            product.shipping_size = shipping_size
        
        if colors:
    # 既存のカラー名を取得
            old_colors = list(product.attributes.filter(attribute__name="Color").values_list('value__value', flat=True))
            
            # 既存のカラーデータをクリアしてから再追加
            product.attributes.filter(attribute__name="Color").delete()  # 既存のカラーを削除
            color_attribute = Attribute.objects.get(name="Color")  # Color属性を取得
            
            for i, color_name in enumerate(colors):
                # 新しいカラー名を作成または取得
                color_value, created = AttributeValue.objects.get_or_create(attribute=color_attribute, value=color_name)
                ProductAttribute.objects.create(product=product, attribute=color_attribute, value=color_value)
                
                # 古いカラー名が存在する場合はColorImageを更新する
                if i < len(old_colors):
                    old_color_name = old_colors[i]
                    try:
                        # 古いカラー名に対応するColorImageを取得
                        old_color_image = ColorImage.objects.get(product=product, color__value=old_color_name)
                        
                        # 新しいカラー名に更新
                        old_color_image.color = color_value
                        old_color_image.save()
                    except ColorImage.DoesNotExist:
                        # 対応するColorImageが存在しない場合はスキップ
                        continue


        # Sizesの更新
        if sizes:
            # 既存のサイズデータをクリアしてから再追加
            product.attributes.filter(attribute__name="Size").delete()  # 既存のサイズを削除
            size_attribute = Attribute.objects.get(name="Size")  # Size属性を取得
            
            for size_name in sizes:
                size_value, created = AttributeValue.objects.get_or_create(attribute=size_attribute, value=size_name)
                ProductAttribute.objects.create(product=product, attribute=size_attribute, value=size_value)

        # 変更を保存
        product.save()

        return redirect('product_detail', product_id=product_id)

    return render(request, 'product_preview.html', {
        'product': product,
        'categories': Category.objects.all(),
    })
