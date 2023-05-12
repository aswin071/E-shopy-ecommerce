from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from shop.models import Category, Product, Sub_Category
from carts.models import Cart, CartItem

from carts.views import _cart_id
from django.core import serializers

# Create your views here.


def shop(request, category_slug=None, sub_category_slug=None):
  categories_shop= None
  subCategories_shop = None
  products = None
    
  if sub_category_slug != None:
    subCategories_shop = get_object_or_404(Sub_Category, slug=sub_category_slug)
    products = Product.objects.all().filter(sub_category=subCategories_shop, is_available=True)
    product_count = products.count()
    
  elif category_slug != None:
    categories_shop = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.all().filter(category=categories_shop, is_available=True)
    product_count = products.count()
        
  else:
    categories_shop = Category.objects.all()
    subCategories_shop = Sub_Category.objects.all()
    products = Product.objects.all().filter(is_available=True).order_by('product_name')
    product_count = products.count()
    
  if request.method == 'POST':
    min = request.POST['minamount']
    max = request.POST['maxamount']
    min_price = min.split('₹')[1]
    max_price = max.split('₹')[1]
    products = Product.objects.all().filter(Q(price__gte=min_price),Q(price__lte=max_price),is_available=True).order_by('price')
    product_count = products.count()
    
  
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
    
  context = {
    'categories_shop':categories_shop,
    'subCategories_shop':subCategories_shop,
    'products':page_obj,
    'product_count':product_count
  }
  return render(request, 'mainapp/shop.html', context)

def sub_category(request):
  cat_id = request.GET['category_id']
  sub_categories = Sub_Category.objects.filter(category=cat_id).values()
  
  return JsonResponse(
          {'success': True,
           'sub_categories':list(sub_categories),
           },
          safe=False
        )

def get_product_names(request):
  if 'term' in request.GET:
     qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
     product_names = list()
     for product in qs:
        product_names.append(product.product_name)
     return JsonResponse(product_names,safe=False)
  return render(request, 'mainapp/shop.html')


# def get_product_names(request):
#   if 'term' in request.GET:
#      qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
#      products = [{'id': product.id, 'name': product.product_name, 'image': product.image_1.url, 'price': product.price} for product in qs]
#      return JsonResponse(products, safe=False)
#   return render(request, 'mainapp/shop.html')




# def get_product_names(request):
#     if 'term' in request.GET:
#         qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
#         products = []
#         for product in qs:
#             products.append({
#                 'name': product.product_name,
#                 'object': serializers.serialize('json', [product])[1:-1]
#             })
#         return JsonResponse(products, safe=False)
#     return render(request, 'mainapp/shop.html')


def search(request):
  if request.method == 'GET':
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
      product_count = products.count()
      
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
      
  context = {
    'products':page_obj,
    'product_count':product_count,
  }
  return render(request, 'mainapp/shop.html', context)