from django.shortcuts import render,redirect
from .models import Account
from .forms import RegistrationForm,UserForm
from orders.models import Address
from orders.forms import AddressForm
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import random
from twilio.rest import Client
from django.views.decorators.cache import never_cache

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
import pyotp
import random

# Create your views here.


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
     form = RegistrationForm(request.POST)
     if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        password = form.cleaned_data['password']
      

        if Account.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'account/signup.html', {'form': form})

        if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Phone number already exists")
                return render(request, 'account/signup.html', {'form': form})
           
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
        user.save()

        if user.is_active:
            messages.success(request, 'Phone verified')
            return redirect('login')
        else:

            totp = pyotp.TOTP(settings.OTP_SECRET)
            otp = totp.now()
            msg_html = render_to_string(
                'account/email.html', {'otp': otp})

            send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
                email], html_message=msg_html, fail_silently=False)

            request.session['otp'] = otp
            request.session['email'] = email
            return redirect('verify_otp')
    else:    
        form = RegistrationForm()
    context = {
        'form': form
    }
  
    return render(request, 'account/signup.html', context)

# def send_otp(request, phone_number):


#     TWILIO_AUTH_TOKEN = '79dfb241e4152af47f82091d378a54a5'
#     TWILIO_ACCOUNT_SID = 'AC6f14efef14bd2c27c86e85e8e2da10e1'
#     TWILIO_PHONE_NUMBER = '+16073669882'
#     otp = random.randint(1000, 9999)
#     request.session['otp'] = otp
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=f"Your OTP is {otp}",
#         from_=TWILIO_PHONE_NUMBER,
#         to=('+91{}'.format(phone_number))
#     )
#     print(message)

def resend_otp(request, phone_number):
    email = request.POST['email']
      
  
    if User.objects.filter(email=email).exists():
        
        totp = pyotp.TOTP(settings.OTP_SECRET)
        otp = totp.now()
        msg_html = render_to_string(
            'userapp/email.html', {'otp': otp})

        send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
            email], html_message=msg_html, fail_silently=False)

        request.session['otp'] = otp
        request.session['email'] = email
        return redirect('verify_otp')


@never_cache
def verify_otp(request):
    if 'otp' not in request.session:
        return redirect('home')
    error = ''
    if request.method == 'POST':
        otp = request.session['otp']
        print(f'otp is{otp}')
        user_otp = request.POST['otp']

        if user_otp != '':
            email = request.session['email']

            if 'otp' in request.session and int(user_otp) == int(request.session['otp']):
                print(f'user otp is{user_otp}')

                user = Account.objects.get(email=email)
                user.is_active = True
                user.save()
                del request.session['otp']
                del request.session['email']
                messages.success(
                    request, 'Email verified, please login to continue')
                return redirect('userlogin')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'account/otp.html', {'error': 'Invalid OTP'})
    return render(request, 'account/otp.html', {'error': error})


#userlogin
@never_cache
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
         
            login(request, user)
            request.session['email'] = email            
            return redirect('home')
        
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('userlogin')
    else:
        return render(request, 'account/login.html') 


@login_required(login_url = 'userlogin')
@never_cache
def logout_user(request):
    if 'email' in request.session:
        request.session.flush()
        return redirect('userlogin') 
    return render (request, 'account/login.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = Account.objects.filter(Q(email=data))
                        
			if associated_users.exists():
                               
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "account/main/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'http://eshopy.store',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                                     
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'dezusajame@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="account/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required(login_url='userlogin')
def profile(request):
    
    return render(request,'user/profile.html')


@login_required(login_url='userlogin')
def editProfile(request):
  if request.method =='POST':
    form = UserForm(request.POST,instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request,'Your Profile Updated Successfully ')
      return redirect ('editprofile')

  else:
    form = UserForm(instance=request.user)

    context = {
        'form':form
         } 

    return render(request, 'user/editprofile.html', context)


@login_required(login_url='userlogin')
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  
  context = {
    'address':address,
  }
  return render(request, 'user/myAddress.html', context)

@login_required(login_url='userlogin')
@never_cache
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.district =  form.cleaned_data['district']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.pincode =  form.cleaned_data['pincode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('useraddress')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('useraddress')
    else:
        form = AddressForm()
        context={
            'form':form
        }    
    return render(request,'user/add-address.html',context)

@login_required(login_url='userlogin')
def edit_address(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('useraddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('useraddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request , 'user/edit-address.html' , context)

@login_required(login_url='userlogin')
def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('useraddress')
    
@login_required(login_url='userlogin')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,"Password Changed")  # Important!
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})


    

