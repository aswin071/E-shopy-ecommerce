from django.urls import path
from .import views

urlpatterns = [
     path('signup/',views.register,name='signup'),
     path('userlogin/',views.userLogin,name='userlogin'),
     path('userlogout',views.logout_user,name='userlogout'),
     path('verify_otp/',views.verify_otp, name='verify_otp'),
     path("passwordreset",views.password_reset_request, name="password_reset"),
     
     path('profile/',views.profile,name='profile'),
     path('editprofile/',views.editProfile,name="editprofile"),
     path('useraddress/',views.myAddress,name="useraddress"),
     path('addaddress/',views.add_address,name="addaddress"),
     path('editaddress/<int:id>/',views.edit_address,name="editaddress"),
     path('deleteaddress/<int:id>/',views.delete_address,name="deleteaddress"),

     path('changepassword/',views.change_password,name="changepassword"),

   
  
     
]