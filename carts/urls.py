from django.urls import path
from .import views

urlpatterns = [

    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('checkout/', views.checkout, name='checkout'),

    path('decqnty/', views.decqnty, name='decqnty'),
    path('incqnty/', views.incqnty, name='incqnty'),

    path('increment_cart_item/<int:cart_item_id>/',views.increment_cart_item, name='increment_cart_item'),
        
    path('decrement_cart_item/<int:cart_item_id>/',views.decrement_cart_item, name='decrement_cart_item'),
         
 

   
    
     
]
