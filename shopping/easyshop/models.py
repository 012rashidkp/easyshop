from django.db import models
from django.contrib.auth.models import User
from django.db import models
import datetime









class Products(models.Model):
    pname=models.CharField(max_length=100,blank=False)
    pstock=models.CharField(max_length=5)
    pdesc=models.CharField(max_length=250)
    prod_price=models.CharField(max_length=5)
    document = models.FileField(upload_to='documents/')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):

        return self.pname

class Cart(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)
     
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'cart {}'.format(self.user.email)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

       


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
    null=True,
    on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Products,
    related_name='cart_items',
    on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return '{}'.format(self.product.pname)

    def get_cost(self):
        return self.price * self.quantity

    subtotal=property(get_cost)   
    
    def remove_item(self, itemid):
        self.items = filter(lambda x: x.itemid != itemid, self.items)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=20) 
    state = models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    pincode=models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {} {}'.format(self.user, self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
    related_name='order_items',
    on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Products,
    related_name='order_products',
    on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
