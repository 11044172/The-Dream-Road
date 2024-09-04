from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from registration import views as registration_views
from registration.views import ActivateView
from cart import views as cart_views
from shop.views import scrape_product_view, save_product_view,product_detail ,account_view


index_view = TemplateView.as_view(template_name="index.html")
mail_view = TemplateView.as_view(template_name="registration/mailconfirm.html")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),  # shopアプリのURL設定を含める
    path('', lambda request: HttpResponseRedirect('/shop/'), name="index"),  # ルートURLにリダイレクト
    path('', include("django.contrib.auth.urls")),
    path('signup/', registration_views.SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('mailconfirm/', mail_view, name="mailconfirm"),
    path('add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('scrape/', scrape_product_view, name='scrape_product'),
    path('save/<int:product_id>/', save_product_view, name='save_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('account/', account_view, name="account"),
]

