
from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='d_index'),
    path('create-category/',views.create_category, name='d_create_category'),
    path('list-category/',views.list_category, name='d_list_category'),
    path('edit-category/<int:id>/', views.edit_category, name='d_edit_category'),
    path('delete-category/<int:id>/', views.delete_category, name='d_delete_category'),
    path('list-orders/', views.orders, name='d_orders'),
    path('update-status/<str:code>/', views.status_update, name='d_update_status'),
    path('reject-cart/<str:code>/', views.reject_cart, name='d_reject_cart'),
    path('product-detail/<int:id>/', views.product_detail, name='d_product_detail'),
    path('category-detail/<int:id>/', views.category_detail, name='d_category_detail'),
    path('create-product/', views.create_product, name='d_create_product'),
    path('delete-product/<int:id>', views.delete_product, name='d_delete_product'),
    path('edit-product/<int:id>/', views.edit_product, name='d_edit_product'),
    path('list-product/', views.product_list, name='d_list_product'),
    path('enter-product/', views.enter_product_list, name='d_list_enter_product'),
    path('create-enter-product/', views.create_enter_product, name='d_create_enter_product'),
    path('edit-enter-product/<int:id>/', views.edit_enter_product, name='d_edit_enter_product'),
    path('detail-orders/<str:code>/', views.cart_detail, name='d_detail_orders'),
    path('yolda-orders/', views.yolda_orders, name='d_yolda_orders'),
    path('yigilmoqda-orders/', views.yigilmoqda_orders, name='d_yigilmoqda_orders'),
    path('login/', views.log_in, name='d_login'),
    path('profile/', views.profile_view, name='d_profile'),
    path('logout/', views.log_out, name='d_logout'),
    path('api/revenue-chart/', views.revenue_chart_data, name='revenue-chart'),
]