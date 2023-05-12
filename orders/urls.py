from django.urls import path
from .import views

urlpatterns = [

  path('placeorder/', views.place_order, name='placeorder'),
  path("cashondelivery/<int:id>/",views.cash_on_delivery,name='cashondelivery'),

  path('myOrders/', views.myOrders, name='myOrders'),
  path('orderDetails/<int:order_id>/', views.orderDetails, name='orderDetails'),
  path("cancel_order/<int:id>/",views.cancel_order,name='cancel_order'),
   

  path('payments/', views.payments, name='payments'),
  path('payments_completed/',views.payments_completed,name = 'payments_completed'),

  path('razorpay/', views.razorpay, name='razorpay'),
  
  path("coupon/",views.coupon,name='coupon'),
  # path("order_cancel/<int:order_id>/",views.order_cancel,name='ordercancel'),
  
     
     
]