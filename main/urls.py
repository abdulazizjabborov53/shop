from django.urls import path
from . import  views
urlpatterns = [
    path('',views.index,name='index'),
    path('product-detail/<str:code>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile.html', views.profile, name='profile'),
    path('category-filter/<int:category_id>/', views.category_filter, name='category_filter'),
    path('add-wishlist/<str:product_code>/', views.add_wishlist, name='add_wishlist'),
    path('delete-wishlist/<str:product_code>/', views.delete_wishlist, name='delete_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('buyurtmalarim/', views.my_orders, name='my_orders'),
    path('buyurtmani-bekor-qilish/<str:cart_code>/', views.cancel_order, name='cancel_order'),
    path('buyurtmani-ochirish/<str:cart_code>/', views.delete_order, name='delete_order'),
    path('cart/',views.cart,name='cart'),
    path('add-cart/<str:product_code>/',views.add_to_cart,name='add_cart'),
    path('cart-product-plus/<str:cart_product_code>/',views.cart_product_count_plus,name='cart_product_plus'),
    path('cart-product-minus/<str:cart_product_code>/',views.cart_product_count_minus,name='cart_product_minus'),
    path('all-products/',views.all_products,name='all_products'),
    path('cart-personal/', views.cart_personal, name='cart_personal'),
    path('order/<str:cart_code>/', views.order, name='order'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('thank-you/<str:cart_code>/', views.thank_you, name='thank_you_cart'),

]