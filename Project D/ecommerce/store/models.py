from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='customer',null=True,blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    p_name = models.CharField(max_length=200)
    price = models.FloatField()
    catagory = models.CharField(max_length=100)
    img = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.p_name
    
    @property
    def imgURL(self):
        try:
            url = self.img.url
        except:
            url = ""
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL,related_name='orderItems', null=True)
    date = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default = False, null=True, blank=False)
    trans_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.trans_id
    
    @property
    def total(self):
        orderitem = self.orderitem_set.all()
        total = sum([i.p_total for i in orderitem])
        return total
    def all_total(self):
        orderitem = self.oerderitem_set.all()
        total = sum([i.quantity for i in orderitem])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.p_name
    
    @property
    def p_total(self):
        ptotal = self.quantity * self.product.price
        return ptotal
    
    
    
class ShippingAdd(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class ForgetPass(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username