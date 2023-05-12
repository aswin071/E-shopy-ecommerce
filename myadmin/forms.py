from django import forms
from category.models import Category, Sub_Category
from shop.models import Product, Variation
from orders.models import Coupon
import datetime

class ProductForm(forms.ModelForm):
    class Meta:
         model = Product
         fields = ['product_name', 'slug', 'description', 'price', 'image_1','image_2','image_3','stock',
                      'is_available', 'is_featured', 'category','sub_category']
        
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['min'] = 0
        self.fields['stock'].widget.attrs['min'] = 0
        self.fields['category'].widget.attrs['onchange'] = "getval(this);"

        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'price_multiplier', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super(VariationForm,self).__init__(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CategoryForm(forms.ModelForm):
    class Meta:
         model = Category
         fields = ['category_name', 'slug','description',]
        
    def __init__(self, *args, **kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class SubCategoryForm(forms.ModelForm):
    class Meta:
         model = Sub_Category
         fields = ['sub_category_name', 'slug', 'description', 'category', 'is_featured',]
        
    def __init__(self, *args, **kwargs):
        super(SubCategoryForm,self).__init__(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'price_multiplier', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super(VariationForm,self).__init__(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount','min_value','valid_at','active']
        widgets = {
                    'valid_at': DateInput(),
                    }
    def __init__(self, *args, **kwargs):
        super(CouponForm,self).__init__(*args, **kwargs)
        self.fields['valid_at'].widget.attrs['min'] = str(datetime.date.today())
        
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
                
            