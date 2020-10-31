from django.db import models
from django.db.models import Avg

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField()

class Client(models.Model):
    user=models.ForeignKey(User)
    email=models.EmailField()
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)

class Developer(models.Model):
    name=models.CharField(max_length=50)
    num_apps=models.IntegerField()
    user=models.ForeignKey(User)
    '''
    @property
    def average_rating(self):
        return self.rates.all().aggregate(Avg('rating')).get('rating__avg', 0.00)
    '''
class Category(models.Model):
    title=models.CharField(max_length=50)


class Product(models.Model):
    name=models.CharField(max_length=50)

    icon=models.URLField()
    rating=models.DecimalField(max_digits=2, decimal_places=1)
    description=models.CharField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

class Purchase(models.Model):
    client=models.ForeignKey(Client)
    product=models.ForeignKey(Product)
    
class Prod_Benefits(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField()
    product=models.ForeignKey(Product)

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2, decimal_places=1)
    date=models.DateField()
    body=models.CharField()

class Product_Pricing_Plan(models.Model):
    product=models.ForeignKey(Product)
    plan_type=models.CharField(max_length=35)
    price=models.CharField(max_length=30)
    feature=models.CharField(max_length=100)
