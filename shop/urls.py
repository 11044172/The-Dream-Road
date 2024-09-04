from django.urls import path
from . import views
from django.views.generic import TemplateView



app_name = 'shop'

urlpatterns = [
    path('', views.index1, name='index'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.index1, name='category_products'),
    path('/login/', TemplateView.as_view(template_name="registration/login.html"), name="login"),
]

