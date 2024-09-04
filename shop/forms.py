# shop/forms.py
from django import forms

class ProductScrapeForm(forms.Form):
    url = forms.URLField(label='商品URL', max_length=500)
    category = forms.CharField(label='カテゴリー', max_length=100)
