
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Developer(models.Model):
    name=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    title=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return str(self.title)

class Product(models.Model):
    name=models.CharField(max_length=50,unique=True)
    icon=models.URLField()
    description=models.CharField(max_length=50)
    category=models.ManyToManyField(Category)
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #def __str__(self):
    #    return str(self.name) + ", " + str(self.category)

class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')#Isto e a FK para a classe User zé. N Mexas xD
    favorites=models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    def __str__(self):
        return str(self.user.username) + ", " + str( self.user.email)



class Purchase(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    available_until= models.DateField(null=True, blank=True)
    def set_paid_until(self,date):
        self.available_until=date
        self.save()
    def has_paid_until(self,current_date=datetime.date.today()):
        # if this parameter is None, then pricing plan is free... for now
        if self.available_until is None : return  True
        if self.available_until > current_date:
            return False

class Prod_Benefits(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating=models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    date=models.DateField()
    body=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Product_Pricing_Plan(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    plans = (
        ('FREE', 'Free Plan'),
        ('MONTHLY', 'Monthly Basic'),
        ('ANNUAL', 'Annual Pro'),
    )
    plan_type=models.CharField(max_length=25, choices=plans, default='FREE')
    price=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    feature=models.CharField(max_length=100)