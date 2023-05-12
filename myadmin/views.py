from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from datetime import datetime,timedelta,date
from category.models import Category, Sub_Category
from .forms import  CategoryForm, SubCategoryForm
from django.core.paginator import Paginator
from accounts.models import Account
from shop.models import Product,Variation
from orders.models import Order,Coupon,Payment
from datetime import datetime,timedelta,date
from django.db.models import Sum, Q, FloatField

from django.http import HttpResponse
from .forms import ProductForm,VariationForm, CouponForm


# Create your views here.




def adminlogin(request):
    if 'email' in request.session:
        return redirect('adminhome')
    #checking if user is superuser or not   
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_superadmin:
            login(request, user)
            request.session['email'] = email 
            return redirect('adminhome')
           
            
        else:
            messages.info(request, 'Invalid username or password. Please try again.')
            return redirect('adminlogin')
            
    else:
        error_message = ""

    return render(request, 'myadmin/adminlogin.html')


#rendering admin html

@staff_member_required(login_url = 'adminlogin')
def admin_home(request):
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    order_count_in_day =Order.objects.filter(created_at__date = today, is_ordered=True).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week, is_ordered=True).count()
    number_of_users  = Account.objects.filter(is_admin = False).count()
    paypal_orders = Payment.objects.filter(payment_method="PayPal",status = True).count()
    razorpay_orders = Payment.objects.filter(payment_method="RazerPay",status = True).count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash On Delivery",status = True).count()

    total_payment_count = paypal_orders + razorpay_orders + cash_on_delivery_count
    try:
        total_payment_amount = Payment.objects.filter(status = True).annotate(total_amount=Cast('amount_paid', FloatField())).aggregate(Sum('total_amount'))
        
    except:
        total_payment_amount=0
        
    if isinstance(total_payment_amount, dict) and 'total_amount__sum' in total_payment_amount:
      revenue = total_payment_amount['total_amount__sum']
      revenue = format(revenue, '.2f')
    
    else:
      revenue = 0
           
    blocked_user = Account.objects.filter(is_active = False,is_superadmin = False).count()
    unblocked_user = Account.objects.filter(is_active = True,is_superadmin = False).count()

    today_sale = Order.objects.filter(created_at__date = today_date,payment__status = True, is_ordered=True).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_5_name = new_date.strftime("%A")
    #status
    ordered = Order.objects.filter(status = 'Order Confirmed', is_ordered=True).count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()
    returned = Order.objects.filter(status = "Returned").count()
    cancelled = Order.objects.filter(status = "Cancelled").count()

    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'razorpay_orders':razorpay_orders,
        'total_payment_count':total_payment_count,
        'revenue':revenue,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'returned':returned,
        'cancelled':cancelled,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request, 'myadmin/adminhome.html', context)

@staff_member_required(login_url = 'adminlogin')
def userview(request):
    user_list= Account.objects.all()
    return render(request,'myadmin/userview.html',{'user_list':user_list})


#Block user
@staff_member_required(login_url = 'adminlogin')
def block_user(request, id):
    users = Account.objects.get(id=id)
    if users.is_active:
        users.is_active = False
        users.save()
        messages.success(request,'User Blocked')

    else:
         users.is_active = True
         users.save()
         messages.success(request,'User Unblocked')

    return redirect('userview')
 

    
@staff_member_required(login_url = 'adminlogin')
def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
        return redirect('adminlogin') 
    return render(request,'myadmin/adminlogin.html')


@staff_member_required(login_url = 'adminlogin')
def Categories(request):
  categories = Category.objects.all().order_by('id')
  
  paginator = Paginator(categories, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'categories':page_obj
  }
  return render(request, 'myadmin/categories.html', context)
  

@staff_member_required(login_url = 'adminlogin')
def addCategory(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Category added successfully.')
      return redirect('categories')
    else:
        print(form.errors)
        messages.error(request, 'Invalid input!!!')
        return redirect('addcategory')
  else:
    form = CategoryForm()
    context = {
      'form':form,
    }
    return render(request, 'myadmin/addcategory.html', context)


@staff_member_required(login_url = 'adminlogin')
def editCategory(request, slug):
  category = Category.objects.get(slug=slug)
  
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES, instance=category)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input')
      return redirect('editcategory', slug)
      
  form =   CategoryForm(instance=category)
  context = {
    'form':form,
    'category':category,
  }
  return render(request, 'myadmin/editcategory.html', context)


@staff_member_required(login_url = 'adminlogin')
def deleteCategory(request, slug):
  category = Category.objects.get(slug=slug)
  category.delete()
  messages.success(request, 'Category deleted successfully.')
  return redirect('categories')


@staff_member_required(login_url = 'adminlogin')
def Subcategories(request, category_slug):
  subCategories = Sub_Category.objects.all().filter(category__slug=category_slug)
  context = {
    'subCategories':subCategories,
    'category_slug':category_slug,
  }
  return render(request, 'myadmin/subcategory.html', context)


@staff_member_required(login_url = 'adminlogin')
def addSubCategory(request, category_slug):
  category = Category.objects.get(slug=category_slug)
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Sub Category added successfully.')
      return redirect('subcategory', category_slug)
    else:
      print(form.errors)
      messages.error(request, 'Invalid input!!!')
      return redirect('addsubcategory', category_slug)
  else:
    form = SubCategoryForm()
    context = {
      'form':form,
      'category':category
    }
    return render(request, 'myadmin/addsubcategory.html', context)

@staff_member_required(login_url = 'adminlogin')
def editSubCategory(request, slug):
  subCategory = Sub_Category.objects.get(slug=slug)
  cat_slug = subCategory.category.slug
  
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES, instance=subCategory)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('subcategory', cat_slug)
    else:
      messages.error(request, 'Invalid input')
      return redirect('editsubcategory')
      
  form =   SubCategoryForm(instance=subCategory)
  context = {
    'form':form,
    'subCategory':subCategory,
  }
  return render(request, 'myadmin/editsubcategory.html', context)

@staff_member_required(login_url = 'adminlogin')
def deleteSubCategory(request, slug):
  sub_category = Sub_Category.objects.get(slug=slug)
  cat_slug = sub_category.category.slug
  sub_category.delete()
  messages.success(request, 'Sub Category deleted successfully.')
  return redirect('subcategory', cat_slug)
 


@staff_member_required(login_url = 'adminlogin')
def Products(request):
  products = Product.objects.all().order_by('-id')
  
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'products': page_obj
  }
  return render(request, 'myadmin/product.html', context)

@staff_member_required(login_url = 'adminlogin')
def addProduct(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('products')
    else:
      print(form.errors)
      messages.error(request, 'Invalid input!!!')
      return redirect('addproduct')
  else:
    form = ProductForm()
    context = {
      'form':form,
    }
    return render(request, 'myadmin/addproduct.html', context)


@staff_member_required(login_url = 'adminlogin')
def editProduct(request, id):
  product = Product.objects.get(id=id)
  
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Product edited successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input')
      
  form =   ProductForm(instance=product)
  context = {
    'form':form,
    'product':product,
  }
  return render(request, 'myadmin/editproduct.html', context)


@staff_member_required(login_url = 'adminlogin')
def deleteProduct(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  messages.success(request, 'Product deleted successfully.')
  return redirect('products')


@staff_member_required(login_url = 'adminlogin')
def orders(request):
  orders=Order.objects.filter(is_ordered=True).order_by('-id')

  paginator=Paginator(orders,10)
  page_number=request.GET.get('page')
  page_obj=paginator.get_page(page_number)

  context ={
    'orders':page_obj,
  }
  return render(request,'myadmin/orders.html',context)

@staff_member_required(login_url = 'adminlogin')
def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash On Delivery':
              payment.status = True
              payment.save()
      except:
          pass
    order.save()
    
  return redirect('orders')

@staff_member_required(login_url = 'adminlogin')
def product_variations(request):
  variations= Variation.objects.all().order_by('product')

  paginator= Paginator(variations, 10)
  page_number = request.GET.get('page')
  page_obj=paginator.get_page(page_number)

  context ={
    'variations':page_obj
  }
  return render(request,'myadmin/product_variation.html',context)

@staff_member_required(login_url = 'adminlogin')
def add_product_variation(request):

  if request.method == 'POST':
    form = VariationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Variation added successfully.')
      return redirect('productvariation')
    else:
      messages.error(request,'Invalid input!!')
      return redirect('addvariations')

  form=VariationForm()
  context= {
        'form':form
      }
  return render(request, 'myadmin/addVariation.html',context)

@staff_member_required(login_url = 'adminlogin')
def edit_variation(request,id):

  variation = Variation.objects.get(id=id)
  
  if request.method == 'POST':
    form = VariationForm(request.POST, instance=variation)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Variation edited successfully.')
      return redirect('productvariation')
    else:
      messages.error(request, 'Invalid input')
      return redirect('editvariation')
      
  form =   VariationForm(instance=variation)
  context = {
    'form':form,
    'variation':variation,
  }
  return render(request, 'myadmin/editVariations.html', context)

@staff_member_required(login_url = 'adminlogin')
def delete_variation(request,id):
  variation=variation = Variation.objects.get(id=id)
  variation.delete()
  messages.success(request, 'Variation deleted successfully!!!')
  return redirect('productvariation')

@staff_member_required(login_url = 'adminlogin')
def coupons(request):
  coupons= Coupon.objects.all()

  context = {
    'coupons':coupons
  }
  return render(request,'myadmin/coupons.html',context)

@staff_member_required(login_url = 'adminlogin')
def add_coupons(request):
  if request.method == 'POST':
    form = CouponForm(request.POST , request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon Added successfully')
      return redirect('coupons')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addcoupons')
  form = CouponForm()
  context = {
    'form':form,
  }
  return render(request, 'myadmin/addcoupon.html', context)

@staff_member_required(login_url = 'adminlogin')
def edit_coupon(request, id):
  coupon = Coupon.objects.get(id = id)
  if request.method == 'POST':
    form = CouponForm(request.POST , request.FILES, instance=coupon)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon updated successfully')
      return redirect('coupons')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('editcoupon', coupon.id)
  form = CouponForm(instance=coupon)
  context = {
    'coupon':coupon,
    'form':form,
  }
  return render(request, 'myadmin/editcoupon.html', context)

@staff_member_required(login_url = 'adminlogin')
def delete_coupon(request,id):
  coupon = Coupon.objects.get(id = id)
  coupon.delete()
  messages.success(request,'Coupon deleted successfully')
  return redirect('coupons')


@staff_member_required(login_url = 'adminlogin')
def sales_report(request):
  year=datetime.now().year
  today= datetime.today()
  month = today.month
  years = []
  today_date = str(date.today())
  start_date= today_date
  end_date= today_date

  if request.method == 'POST':
      start_date = request.POST.get('start_date')
      end_date = request.POST.get('end_date')
      val = datetime.strptime(end_date, '%Y-%m-%d')
      end_date = val+timedelta(days=1)
      orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')

  else:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')

  year = today.year
  for i in range (3):
        val = year-i
        years.append(val)
  
  context = {
        'orders':orders,
        'today_date':today_date,
        'years':years,
        'start_date':start_date,
        'end_date':end_date,
    }
  return render(request, 'myadmin/sales_report.html', context)


@staff_member_required(login_url = 'adminlogin')
def sales_report_month(request,id):
    orders = Order.objects.filter(created_at__month = id,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'myadmin/sales_report_table.html',context)

  
@staff_member_required(login_url = 'adminlogin')
def pdf_report(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
      orders = Order .objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    
    template_path = 'adminapp/sales-report-pdf.html'
    context = {'orders': orders,}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@staff_member_required(login_url = 'adminlogin')
def excel_report(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
    else:
      orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
      
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales_report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Item Name', 'Item sold', 'In stock', 'Amount Received']
    
    for col_num in range(len(columns)):
      ws.write(row_num, col_num, columns[col_num], font_style)
      
    font_style = xlwt.XFStyle()
    
    rows = orders
    
    for row in rows:
      row_num += 1

      for col_num in range(len(row)):
        ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response
