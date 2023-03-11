from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('category/<str:id>', views.category),
    path('product/<str:slug>', views.product),
    path('api/getprodprice', views.getProductPrice),
    path('add-to-cart',views.add_to_cart),
    path('login',views.loginuser),
    path('signup',views.signup),
    path('cart', views.cart)
]
