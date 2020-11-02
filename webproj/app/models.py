from django.db import models
from django.db.models import Avg

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField()

class Client(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField()
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)

class Developer(models.Model):
    name=models.CharField(max_length=50)
    #num_apps=models.IntegerField() isto e uma query tb n adianta meter, ia nos foder dps
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    '''
    @property
    def average_rating(self):
        return self.rates.all().aggregate(Avg('rating')).get('rating__avg', 0.00)
    '''
class Category(models.Model):
    title=models.CharField(max_length=50,unique=True)


class Product(models.Model):
    name=models.CharField(max_length=50,unique=True)

    icon=models.URLField()
    rating=models.DecimalField(max_digits=2, decimal_places=1)
    description=models.CharField()
    category=models.ManyToManyField(Category)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

class Purchase(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
class Prod_Benefits(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2, decimal_places=1)
    date=models.DateField()
    body=models.CharField()

class Product_Pricing_Plan(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    plan_type=models.CharField(max_length=35)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    feature=models.CharField(max_length=100)
