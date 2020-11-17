from django.contrib.auth.models import User
from django import forms
from .models import Products,Order
from django.contrib.auth.forms import UserCreationForm



class ProductsForm(forms.ModelForm):
    

    class Meta:
        model = Products
        fields=[
            'pname','pstock','pdesc','prod_price','document'
        ]
    

        
        

    def __init__(self, *args, **kwargs):
         super(ProductsForm, self).__init__(*args, **kwargs)
         self.fields['pname'].label = "product name"
         self.fields['pstock'].label = "product stock"
         self.fields['pdesc'].label="product description"
         self.fields['prod_price'].label="product price"
         self.fields['document'].label="product image"

         #self.fields['pname'].widget.attrs['name'] = 'new_name'
          # Call to ModelForm constructor
    #     self.fields['pname'].widget.attrs['style'] = 'width:400px; height:40px;'
    #     self.fields['pstock'].widget.attrs['style']  = 'width:401px; height:40px;'
    #     self.fields['pdesc'].widget.attrs['style']  = 'width:405px; height:80px;'
    #     self.fields['prod_price'].widget.attrs['style']  = 'width:375px; height:40px;'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class customerform(forms.ModelForm):
    class Meta:
        model=Order
        fields=['name','email','address','city','state','phone','pincode']
