from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
# Create your models here.


class Developer(models.Model):
    name=models.CharField(max_length=50)

class Category(models.Model):
    title=models.CharField(max_length=50,unique=True)

class Product(models.Model):
    name=models.CharField(max_length=50,unique=True)
    icon=models.URLField()
    description=models.CharField(max_length=50)
    category=models.ManyToManyField(Category)
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)

class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')#Que é isto MANO?
    favorites=models.ManyToManyField(Product,default=None)
    def __str__(self):
        return str(self.user.username) + ", " + str( self.user.email)

class Purchase(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Prod_Benefits(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2, decimal_places=1)
    date=models.DateField()
    body=models.CharField(max_length=50)

class Product_Pricing_Plan(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    plan_type=models.CharField(max_length=35)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    feature=models.CharField(max_length=100)