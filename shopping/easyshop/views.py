from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductsForm,CreateUserForm,customerform
from .models import Products,User,Cart,CartItem,Order,OrderItem
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from easyshop.serializers import ProductSerializer,UserSerializer,LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, views, permissions
from django.contrib import auth
from django.db.models import Q
from django.contrib import messages


 

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'easyshop/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
        context = {}
        return render(request, 'easyshop/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store')



def store(request):
    products = Products.objects.all()
    context = { 'products': products }
    return render(request, 'easyshop/store.html', context )

@login_required(login_url='login')
def cart(request):
    cartproducts = Cart.objects.get(user=request.user)
    itemcount=cartproducts.items.count()
    if itemcount==0:
        return redirect('alert')
    else:
        context = {'products':cartproducts,'itemcount':itemcount}    
        return render(request, 'easyshop/cart.html', context)


def checkout(request):
    cartproducts = Cart.objects.get(user=request.user)
    itemcount=cartproducts.items.count()
    form=customerform()
    context = {'products':cartproducts,'itemcount':itemcount,'form':form}
    return render(request, 'easyshop/placeorder.html', context)
    
    
    
    
         

def upload(request, id=0):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = ProductsForm()
    return render(request, 'easyshop/uploadprod.html', {
        'form': form
    })

def updateOrder(request, pk):
    maintain = Products.objects.get(id=pk)
    form = ProductsForm(instance=maintain)

    if request.method == 'POST':
        form = ProductsForm(request.POST, instance=maintain)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'easyshop/uploadprod.html', context)

def maintain(request):
      products = Products.objects.all()
      context = { 'products': products }
      return render(request, 'easyshop/maintain.html', context)


def deleteOrder(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('/')

    context = {'item': product}
    return render(request, 'easyshop/delete.html', context)

def show(request, pk):
    product = Products.objects.get(id=pk)
    
    context = {'item': product}
    return render(request, 'easyshop/view.html', context) 

       
@login_required(login_url='login')
def logoutpage(request):
     
      context = {}

      return render(request, 'easyshop/logout.html', context)



@api_view(["GET",])
def show_list(request):
    if(request.method=="GET"):
        data=Products.objects.all()
        serializers=ProductSerializer(data,many=True)
        response = {
            
            'error' : False,
            'datas' : serializers.data
        }
        return Response(response)
    else:
        err={
            'error' : True
        }
        return Response(err)

 
class RegisterView(APIView):
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['error']=False
            data['message']='registration success'
            data['username']=account.username
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
            data['userid']=token.user_id
        else:
            data['error']=True
            data['message']=serializer.errors
            
        return Response(data)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        data={}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data['error']=False
            data['message']='login success'
            data['username']=user.username
            data['email']=user.email
            data['userid']=token.user_id
            data['token']=token.key
        
        return Response(data)
        
            


@login_required(login_url='login')
def addtocart(request, pk, product_qty=None):
    obj, created = Cart.objects.update_or_create(user=request.user)
    product = get_object_or_404(Products, id=pk)
    item, itemCreated = CartItem.objects.update_or_create(
        cart=obj, product=product)
    item.price = product.prod_price
    if(itemCreated == False):
        item.quantity = item.quantity+1
    # if item.quantity = request.GET['q']

    obj.items.add(item)
    item.save()
    obj.save()
    return redirect('dialog')

def dialog(request):
    context = {}
    return render(request, 'easyshop/dialog.html', context)
    
def cart_remove(request, pk):
    obj, created = Cart.objects.update_or_create(user=request.user)
    product = get_object_or_404(Products, id=pk)
    cartItems = CartItem.objects.filter(cart=obj, product=product)
    cartItems.delete()
    return redirect('cartremovedialog')




def cart_remove_alert(request):
    context={}
    return render(request,'easyshop/removedialog.html',context)      
       



def cart_add_q(request, pk, product_qty=None):
    obj, created = Cart.objects.update_or_create(user=request.user)
    product = get_object_or_404(Products, id=pk)
    item, itemCreated = CartItem.objects.update_or_create(
        cart=obj, product=product)
    # item.price = product.price

    # if item.quantity = request.GET['q']
    item.quantity = request.GET['q']
    if request.GET['q'] == "0":
        item.delete()
    else:
        obj.items.add(item)
        item.save()
        obj.save()
    return redirect('cart')
    
     
def alert(request):
    context = {}
    return render(request, 'easyshop/alert.html', context)

def placeorder(request):
    order = Order.objects.create(user=request.user)
    order.save()
    for item in cart.items.all():
        orderItem, created = OrderItem.objects.update_or_create(
            order=order, product=item.product, price=item.price, quantity=item.quantity)
        order.order_items.add(orderItem)
        form=customerform()
        if request.method=='POST':
            form = customerform(request.POST)
            if form.is_valid():
                form.save()
                return redirect('store')


    