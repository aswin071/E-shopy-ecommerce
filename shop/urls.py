from django.urls import path
from .import views

urlpatterns = [
   
  path('shop/', views.shop, name='shop'),
  path('shop/<slug:category_slug>/', views.shop, name='products_by_category'),
  path('shop/<slug:category_slug>/<slug:sub_category_slug>/', views.shop, name='products_by_sub_category'),
  path('shop_filter/', views.shop, name='shop_filter'),

  path('sub_category/', views.sub_category, name='sub_category'),
  path('get_product_names/', views.get_product_names, name='get_product_names'),

  path('search/', views.search, name='search'),
 
     
     
]