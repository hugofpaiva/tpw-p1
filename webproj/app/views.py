from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Min, Avg, Count
import math

from app.filters import ProductFilter
from app.forms import *
from app.models import *
import random
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

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
        product.Roundprice = round(
            product.price, 2)
        product.nStars = range(int(product.stars))
        product.nEmptyStars = range(5 - int(product.stars))

    return render(request, 'index.html', {'activelem': 'home', 'productsBanner': productsBanner, 'products': products})


def shopView(request):
    # Falta Aplicar nova paginação
    if request.GET.get('page') is None:
        pageNumber=1
    else:
        pageNumber = int(request.GET.get('page'))

    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12

    products = ProductFilter(request.GET, queryset=Product.objects.all())

    products = products.qs

    productsOffset = products[offset:offset+12]
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
        product.Roundprice = round(product.price, 2)
        product.nStars = range(int(product.stars))
        product.nEmptyStars = range(5 - int(product.stars))

    return render(request, 'shop.html',
                  {'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,
                   'totalPages': totalPages, 'actualPage': pageNumber, 'leftPages': leftPages,
                   'rangeLeftPages': rangeLeftPages, 'categories': categories, 'developers': developers, 'getParams': request.GET})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
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
    product = Product.objects.get(id=idprod)
    if request.method == "POST":
        form = proceedtoCheckoutForm(request.POST)
        if form.is_valid():
            form_prodid = form.cleaned_data.get("productid")
            if idprod != form_prodid:
                return HttpResponseNotFound("Something went wrong!")

            paymenttype = form.cleaned_data.get("paymenttype")
            valuetopay = Product_Pricing_Plan.objects.get(id=paymenttype)
            print(valuetopay.price)
            client = Client.objects.filter(user_id=request.user.id)
            client = client[0]

            if client.balance < valuetopay.price:
                return HttpResponse("You do not have enough credit!")
            p = Purchase.objects.filter(client=client, product=product)
            print(p)
            #only assert that the user does not have the same product twice
            if p.exists():
                return HttpResponse("Product already bought")
            else:
                # already verified before if this is the correct product
                p = Purchase(client=client, product=product)
                client.balance -= valuetopay.price
                client.save()
                p.save()
                return HttpResponse("Sucess!")


    else:
        myform = proceedtoCheckoutForm()
        # try:

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
                       'purch': totalpurchases, 'numreviews': numreviews, 'myform': myform})


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
        form_pw = UpdatePasswordForm(request.user, request.POST)
        if 'old_password' not in request.POST:
            print("fields")
            if form.is_valid():
                update = form.save()
                update.client = request.user
                client = Client.objects.get(user_id=update.client.id)
                update.save()
                update.refresh_from_db()
                #to stay logged in

                #Because after changes in account, the system logout the user
                login(request, update.client)
                form=fill_form(client)
                return render(request,'clientdetails.html',{'user': client, 'form': form, 'form_pw': form_pw})
        else:
            print("pw")
            if form_pw.is_valid():
                user = form_pw.save()
                update_session_auth_hash(request, form_pw.user)
                user.client = request.user
                client = Client.objects.get(user_id=user.client.id)
                user.save()
                user.refresh_from_db()
                #to stay logged in

                #Because after changes in account, the system logout the user
                login(request, user.client)
                form = fill_form(client)
                return render(request,'clientdetails.html',{'user': client, 'form_pw': form_pw, 'form': form})
    else:
        form = fill_form(client)
        form_pw = UpdatePasswordForm(request.user)
    return render(request, 'clientdetails.html', {'user': client, 'form': form, 'form_pw': form_pw})
