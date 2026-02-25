"""
URL configuration for furniture_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from store import views

# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',views.home,name='home'),

# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('dummy-payment/<int:order_id>/', views.dummy_payment, name='dummy_payment'),
    path('orders/', views.order_history, name='order_history'),
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('add-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('category/<int:id>/', views.category_products,
     name='category_products'),
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # NEW PRODUCT DETAIL URL
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('payment/<int:order_id>/', views.dummy_payment, name='dummy_payment'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
