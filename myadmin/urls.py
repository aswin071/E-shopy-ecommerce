from django.urls import path
from .import views

urlpatterns = [
    path('adminhome/',views.admin_home,name='adminhome'),
    path('admin/',views.adminlogin,name='adminlogin'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),

    path('userview/',views.userview,name='userview'),
    path('blockuser/<int:id>/',views.block_user,name='blockuser'),
  


    path('categories/', views.Categories, name='categories'),
    path('addcategory/', views.addCategory, name='addcategory'),
    path('<str:slug>/editcategory/', views.editCategory, name='editcategory'),
    path('<str:slug>/deletecategory/', views.deleteCategory, name='deletecategory'),

    


    path('<str:category_slug>/subCategories/',views.Subcategories, name='subcategory'),
    path('<str:category_slug>/addsubcategory/',views.addSubCategory, name='addsubcategory'),
    path('<str:slug>/editSubCategory/', views.editSubCategory, name='editsubcategory'),
    path('<str:slug>/deleteSubCategory/', views.deleteSubCategory, name='deleteSubCategory'),

    path('products/',views.Products,name='products'),
    path('addproducts/',views.addProduct,name='addproduct'),
    path('<int:id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),
    path('<int:id>/editProduct/', views.editProduct, name='editProduct'),

    path('orders/', views.orders, name='orders'),
    path('update_order/<int:id>',views.update_order,name="update_order"),

    path('productvariation/',views.product_variations,name="productvariation"),
    path('products/product_variations/addvariation/',views. add_product_variation,name="addVariation"),
    path('products/product_variations/<int:id>/edit_variation',views. edit_variation,name="editvariation"),
    path('products/deletevariation/<int:id>/edit_variation',views. delete_variation,name="deletevariation"),

    path('coupons/',views.coupons,name="coupons"),
    path('addcoupons/',views.add_coupons,name="addcoupons"),
    path('editcoupon<int:id>/',views.edit_coupon,name="editcoupon"),
    path('deletecoupon<int:id>/',views.delete_coupon,name="deletecoupon"),

    path('sales_report/',views.sales_report,name="sales_report"),
    path('sales_report_month/<int:id>',views.sales_report_month,name="sales_report_month"),

    # path('sales-graph/',views.sales_graph, name='sales_graph'),
    path('pdf_report/<str:start_date>//<str:end_date>/', views.pdf_report, name='pdf_report'), 
    path('excel_report/<str:start_date>//<str:end_date>/', views.excel_report, name='excel_report'),

   
     
]
