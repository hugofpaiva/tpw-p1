from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Min, Avg, Count
import math
from app.forms import *
from app.models import *
import random
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def indexView(request):
    numBanners = random.randint(2, 6)
    productsBanner = []
    totalProds = Product.objects.count()

    for _ in range(numBanners):
        index = random.randint(0, totalProds - 1)

        prod = Product.objects.all()[index]

        if prod not in productsBanner:
            productsBanner.append(prod)

    # Vai contar o nº de ocorrências noutra tabela e ordenar pelas ocorrências
    bestSellers = Product.objects.annotate(numVendasProd=Count('purchase'))

    bestSellers = list(bestSellers[:6])

    for best in bestSellers:
        best.tags = "best"

    newArrivals = Product.objects.all().order_by('-id')

    newArrivalsDistinct = []

    count = 0
    for arrival in newArrivals:
        if (count == 6):
            break
        if arrival not in bestSellers:
            arrival.tags = "new"
            arrival.new = True
            newArrivalsDistinct.append(arrival)
            count += 1
        else:
            index = bestSellers.index(arrival)
            bestSellers[index].new = True
            bestSellers[index].tags += " new"

    products = newArrivalsDistinct + bestSellers

    for product in products:
        product.price = round(
            Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'], 2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))
        product.nEmptyStars = range(5 - int(product.rate))

    return render(request, 'index.html', {'activelem': 'home', 'productsBanner': productsBanner, 'products': products})


def shopSearchView(request, prodName, pageNumber):
    if pageNumber < 1:
        return render(request, 'notfound.html')

    offset = (pageNumber - 1) * 12
    products = Product.objects.filter(name__icontains=prodName)
    productsOffset = products[offset:offset + 12]
    totalProducts = products.count()
    leftPages = totalProducts - pageNumber
    totalPages = round(totalProducts / 12)

    categories = Category.objects.all()
    developers = Developer.objects.all()

    if totalPages == 0:
        totalPages = 1

    if leftPages <= 2:
        rangeLeftPages = range(leftPages)
    else:
        rangeLeftPages = range(2)

    for category in categories:
        category.numProd = Product.objects.filter(category__exact=category).count()

    for product in productsOffset:
        product.price = round(
            Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'], 2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))

        product.nEmptyStars = range(5 - int(product.rate))
    return render(request, 'shop.html',
                  {'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,
                   'totalPages': totalPages, 'actualPage': pageNumber, 'leftPages': leftPages,
                   'rangeLeftPages': rangeLeftPages, 'categories': categories, 'developers': developers})


def shopView(request, pageNumber=1):
    if pageNumber < 1:
        return render(request, 'notfound.html')

    offset = (pageNumber - 1) * 12
    products = Product.objects.all()
    productsOffset = products[offset:offset + 12]
    totalProducts = products.count()

    totalPages = math.ceil(totalProducts / 12)

    categories = Category.objects.all()

    developers = Developer.objects.all()

    if totalPages == 0: totalPages = 1
    leftPages = totalPages - pageNumber
    if leftPages <= 2:
        rangeLeftPages = range(leftPages)
    else:
        rangeLeftPages = range(2)

    for category in categories:
        category.numProd = Product.objects.filter(category__exact=category).count()

    for product in productsOffset:
        product.price = round(
            Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))['price__min'], 2)
        rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))
        product.nEmptyStars = range(5 - int(product.rate))
    return render(request, 'shop.html',
                  {'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,
                   'totalPages': totalPages, 'actualPage': pageNumber, 'leftPages': leftPages,
                   'rangeLeftPages': rangeLeftPages, 'categories': categories, 'developers': developers})


def register(request):
    if request.method == "POST":
        myform = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            client = Client(user=user)
            client.save()
            return render(request, 'index.html', {'activelem': 'home'})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def prodDetails(request, idprod):
    if request.method == "POST":
        form= proceedtoCheckoutForm(request.POST)
        if form.is_valid():
            form_prodid= form.cleaned_data.get("productid")
            if idprod != form_prodid:
                return  HttpResponseNotFound("Something went wrong!")
            paymenttype= form.cleaned_data.get("paymenttype")
            valuetopay= Product_Pricing_Plan.objects.get(id=paymenttype)
            print(valuetopay.price)
            return   HttpResponse("Sucess!")
            #

    else:
        myform = proceedtoCheckoutForm()
        # try:
        product = Product.objects.get(id=idprod)
        reviews = Reviews.objects.filter(product=product)
        paginator = Paginator(reviews, 1)  # shows 1 review per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        numreviews = reviews.count()
        for review in reviews:
            review.nStars = range(int(review.rating))
            review.nEmptyStars = range(5 - int(review.rating))
            print(review.nStars, review.nEmptyStars)
        rate = reviews.aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars = range(int(product.rate))
        product.nEmptyStars = range(5 - int(product.rate))
        productbenefits = Prod_Benefits.objects.filter(product=product)
        pricing = Product_Pricing_Plan.objects.filter(product=product)
        categories = product.category.all()
        print(categories)
        print(Purchase.objects.filter(product=product))
        totalpurchases = Purchase.objects.filter(product__exact=product).count()
        ##except:
        ##return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'productdetails.html',
                      {'prod': product, 'revs': page_obj, 'prodbenefs': productbenefits, 'plans': pricing,
                       'purch': totalpurchases, 'numreviews': numreviews, 'myform':myform})


def fill_form(client):
    form = UpdateClientForm()
    form.fields['username'].initial = client.user.username
    form.fields['first_name'].initial = client.user.first_name
    form.fields['last_name'].initial = client.user.last_name
    form.fields['email'].initial = client.user.email
    return form


@csrf_exempt
def complete_transaction(request, num):
    print("crl")
    if request.method == 'POST':
        print("entrei!")
        print(request.id)
        print(num)
        return HttpResponse('')


# ver isto melhor ta cancro como a merda
def accountDetails(request):
    user = User.objects.get(username=request.user.username)
    client = Client.objects.get(user_id=user.id)
    if request.method == "POST":
        form = UpdateClientForm(request.POST, instance=request.user)
        if form.is_valid():
            update = form.save()
            print(update)
            update.client = request.user
            client = Client.objects.get(user_id=update.client.id)
            update.save()
            update.refresh_from_db()
            # to stay logged in

            # Because after changes in account, the system logout the user
            login(request, update.client)
            form = fill_form(client)
            return render(request, 'clientdetails.html', {'user': client, 'form': form})
    else:
        form = fill_form(client)
    return render(request, 'clientdetails.html', {'user': client, 'form': form})
