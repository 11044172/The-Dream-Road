import os
import sys
import django
import re
from bs4 import BeautifulSoup
import requests

# Djangoプロジェクトのパスを設定
sys.path.append('/Users/eusyoicloud.com/myshop_project/myshop')
sys.path.append('/Users/eusyoicloud.com/myshop_project')

# Django設定の読み込み
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

# モデルのインポート
from shop.models import Product, Attribute, AttributeValue, ProductAttribute, ColorImage

def get_or_create_attribute(name):
    attribute, created = Attribute.objects.get_or_create(name=name)
    return attribute

def get_or_create_attribute_value(attribute, value):
    attr_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=value)
    return attr_value

def get_product_data(url):
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
        category="bottoms",
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

# テスト用URL
url = 'https://www.grail.bz/item/ai1091119/'
product = get_product_data(url)
print(f"{product}の登録が完了しました。")

# 最後に追加された色とサイズの情報を表示
print(f"Product: {product.title}")
print("Colors and Sizes:")
for pa in ProductAttribute.objects.filter(product=product):
    print(f" - {pa.attribute.name}: {pa.value.value}")

# 追加されたカラー画像の情報を表示
print("Color Images:")
for ci in ColorImage.objects.filter(product=product):
    print(f" - {ci.color.value}: {ci.image_url}")
