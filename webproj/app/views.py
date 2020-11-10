from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.db.models import Min, Avg, Count
import math
from app.forms import *
from app.models import *
import random
from django.contrib.auth import authenticate, login
# Create your views here.

#foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def indexView(request):
    numBanners = random.randint(2, 6)
    productsBanner = []
    totalProds = Product.objects.count()

    for _ in range(numBanners):
        index = random.randint(0, totalProds-1)

        prod = Product.objects.all()[index]

        if prod not in productsBanner:
            productsBanner.append(prod)

    # Vai contar o nº de ocorrências noutra tabela e ordenar pelas ocorrências
    bestSellers = Product.objects.annotate(numVendasProd=Count('purchase'))

    bestSellers = list(bestSellers[:6])

    for best in bestSellers:
        best.tags = "best"

    newArrivals = Product.objects.all().order_by('-id')

    newArrivalsDistinct= []

    count=0
    for arrival in newArrivals:
        if(count==6):
            break
        if arrival not in bestSellers:
            arrival.tags = "new"
            arrival.new=True
            newArrivalsDistinct.append(arrival)
            count+=1
        else:
            index = bestSellers.index(arrival)
            bestSellers[index].new = True
            bestSellers[index].tags += " new"


    products = newArrivalsDistinct + bestSellers


    for product in products:
        product.price = round(Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'],2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate=rate
        else:
            product.rate=0
        product.nStars = range(int(product.rate))
        product.nEmptyStars = range(5-int(product.rate))


    return render(request, 'index.html',{'activelem': 'home', 'productsBanner': productsBanner, 'products': products})

def shopSearchView(request, prodName, pageNumber):
    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12
    products = Product.objects.filter(name__icontains=prodName)
    productsOffset = products[offset:offset+12]
    totalProducts=products.count()
    leftPages=totalProducts-pageNumber
    totalPages = round(totalProducts/12)

    categories = Category.objects.all()

    developers = Developer.objects.all()

    if totalPages == 0:
        totalPages=1

    if leftPages<=2:
        rangeLeftPages = range(leftPages)
    else:
        rangeLeftPages = range(2)

    for category in categories:
        category.numProd = Product.objects.filter(category__exact=category).count()

    for product in productsOffset:
        product.price = round(Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'],2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))

        product.nEmptyStars = range(5-int(product.rate))
    return render(request,'shop.html',{'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,
                                       'totalPages': totalPages,'actualPage':pageNumber,'leftPages':leftPages,
                                       'rangeLeftPages': rangeLeftPages, 'categories':categories, 'developers': developers})

def shopView(request, pageNumber=1):
    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12
    products = Product.objects.all()
    productsOffset = products[offset:offset+12]
    totalProducts=products.count()

    totalPages = math.ceil(totalProducts/12)

    categories = Category.objects.all()

    developers = Developer.objects.all()

    if totalPages == 0: totalPages=1
    leftPages = totalPages - pageNumber
    if leftPages<=2:
        rangeLeftPages = range(leftPages)
    else:
        rangeLeftPages = range(2)

    for category in categories:
        category.numProd = Product.objects.filter(category__exact=category).count()

    for product in productsOffset:
        product.price = round(Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'],2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))
        product.nEmptyStars = range(5-int(product.rate))
    return render(request,'shop.html',{'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,
                                       'totalPages': totalPages,'actualPage':pageNumber,'leftPages':leftPages,
                                       'rangeLeftPages': rangeLeftPages, 'categories':categories, 'developers': developers})

def register(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            client = Client(user=user)
            client.save()
            return render(request,'index.html',{'activelem': 'home'})
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form':form})



def prodDetails(request,idprod):
    #try:
    product=Product.objects.get(id=idprod)
    reviews=Reviews.objects.filter(product=product)
    for review in reviews:
        review.nStars=range(int(review.rating))
        review.nEmptyStars=range(5-int(review.rating))
        print(review.nStars,review.nEmptyStars)
    rate = reviews.aggregate(Avg('rating'))['rating__avg']
    if rate:
        product.rate = rate
    else:
        product.rate = 0
    product.nStars = range(int(product.rate))
    product.nEmptyStars = range(5 - int(product.rate))
    productbenefits=Prod_Benefits.objects.filter(product=product)
    pricing=Product_Pricing_Plan.objects.filter(product=product)
    categories=product.category.all()
    print(categories)
    print(Purchase.objects.filter(product=product))
    totalpurchases=Purchase.objects.filter(product__exact=product).count()
    ##except:
        ##return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request,'productdetails.html',{'prod':product, 'revs':reviews, 'prodbenefs':productbenefits, 'plans':pricing,'purch':totalpurchases})







def accountDetails(request):

    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        form = UpdateClientForm(request.POST, instance=request.user)
        if form.is_valid():
            update = form.save()
            update.user = request.user
            update.save()
            update.refresh_from_db()
            #to stay logged in
            login(request, update.user)
            return render(request,'index.html',{'activelem': 'home'})
    else:
        form = SignUpForm()


    return render(request, 'clientdetails.html', {'user': user, 'form': form})
