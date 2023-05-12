from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from category.models import Category,Sub_Category
from shop.models import Product
from carts.models import Cart, CartItem


from django.shortcuts import get_object_or_404
from carts.views import _cart_id

# Create your views here.


def error_404(request,exception):
  return render(request,'404.html')
def home(request):
    
    featured_products = Product.objects.all().filter(is_featured=True)[:3]
    featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:3]
   
    context = {
    'featured_categories': featured_categories,
    'featured_products': featured_products,

    }
   
    

    return render(request,'mainapp/home.html',context)

def contact(request):
  return render(request,'mainapp/contact.html')



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



def product_list(request):
    products = Product.objects.all()
    categories = {}
    for product in products:
        if product.category not in categories:
            categories[product.category] = [product]
        else:
            categories[product.category].append(product)
    context = {'categories': categories}
    return render(request, 'product_list.html', context)

def product_details(request, category_slug, sub_category_slug, product_slug):
  categories = Category.objects.all()
  
  try:
    product = Product.objects.get(category__slug=category_slug, sub_category__slug=sub_category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()    
    related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[:4]
    
  except Exception as e:
    raise e

  context = {
    'categories':categories,
    'product':product,
    "related_products":related_products,
    "in_cart":in_cart,
  }
  return render(request, 'mainapp/singleproduct.html', context)