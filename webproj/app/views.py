from django.http import HttpResponseNotFound, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Min, Avg, Count
import math
from app.forms import *
from app.models import *
import random
from django.contrib.auth import authenticate, login
import datetime
import calendar
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def indexView(request):
    numBanners = random.randint(2, 6)
    productsBanner = []

    tot_purch = []
    totalProds = Product.objects.count()
    Product.objects = Product.objects.filter()
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


def shopView(request):

    if request.GET.get('page') is None:
        pageNumber=1
    else:
        pageNumber = int(request.GET.get('page'))

    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12
    parameters = {field_name: value for field_name, value in request.GET.items()
                 if value and field_name in Product._meta.get_fields}
    print(parameters)
    print(Product._meta.get_fields())
    products = Product.objects.filter()
    print(products)
    productsOffset = products[offset:offset+12]
    totalProducts=products.count()

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


def datetime_offset_by_months(datetime_origin, n=1):

    one_day = datetime.timedelta(days=1)
    q, r = divmod(datetime_origin.month + n, 12)

    datetime_offset = datetime.datetime(
        datetime_origin.year + q, r + 1, 1) - one_day

    if datetime_origin.month != (datetime_origin + one_day).month:
        return datetime_offset

    if datetime_origin.day >= datetime_offset.day:
        return datetime_offset

    return datetime_offset.replace(day= datetime_origin.day)

#class used to process valid forms in the products view
class Products_Forms_Processing:

    def __init__(self,client,product):
        self.client=client
        self.product=product
    def check_curr_form(self,form,request):
        if isinstance(form,PurchaseForm):
            return self.payment_form_process(form,request)
        elif isinstance(form,FavoritesForm):
            print("cuuuuu")
            return self.favorites_form_process(form, request)
        else:
            return  Http404("Something went wrong")


    def payment_form_process(self, form,request):
        paymenttype = form.cleaned_data.get("paymenttype")
        valuetopay = Product_Pricing_Plan.objects.get(id=paymenttype)
        print(valuetopay.price)
        p = Purchase.objects.filter(client=self.client, product=self.product)
        #check if client has already the product
        if p.exists() and p[0].has_paid_until():
            request.session.__setitem__("last_request_error", "You already have this product!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #check if the client has enough balance
        elif self.client.balance < valuetopay.price:
            request.session.__setitem__("last_request_error", "You do not have enough credit to complete the purchase!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #process the purchase
        else:
            if valuetopay.plan_type != 'FREE':
                if valuetopay.plan_type == 'MONTHLY':
                    print(datetime.date.today())
                    p.set_paid_until(datetime_offset_by_months(datetime.date.today()))
                else:
                    oneyear = datetime.date.today()
                    for i in range(1, 13):
                        oneyear = datetime_offset_by_months(oneyear)
                    p.set_paid_until(oneyear)
            self.client.balance -= valuetopay.price
            self.client.save()
            p.save()
            request.session.__setitem__("last_request_success", "Success in the completion of the purchase!" )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def favorites_form_process(self, form,request):
        print("ola")
        client_favorites=self.client.favorites.all()
        if self.product not in client_favorites:
            self.client.favorites.add(self.product)
            request.session.__setitem__("last_request_success", "Product " + self.product.name + " successfully added to your favorites!")
        else:
            self.client.favorites.remove(self.product)
            request.session.__setitem__("last_request_success", "Product " + self.product.name + " successfully removed to your favorites!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def prodDetails(request, idprod):
    product = Product.objects.get(id=idprod)
    client = Client.objects.filter(user_id=request.user.id)
    client = client[0]
    if request.method == "POST":
        print(request.session)
        form_purchases,form_favorites = PurchaseForm(request.POST),FavoritesForm(request.POST)
        response=None
        handler = Products_Forms_Processing(client, product)
        if form_purchases.is_valid():
            print(form_purchases.cleaned_data.items())
            response=handler.check_curr_form(form_purchases,request)
        elif form_favorites.is_valid():
            handler = Products_Forms_Processing(client, product)
            response = handler.check_curr_form(form_favorites, request)
        return response
    else:
        form_purchases,form_favorites = PurchaseForm(),FavoritesForm()
        reviews = Reviews.objects.filter(product=product)
        numreviews = reviews.count()
        # --- Django Pagination ---
        paginator = Paginator(reviews, 1)  # shows 1 review per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # ------------------------
        # check if product is already, or not, added to the client's favorites
        is_fav=False
        if product in client.favorites.all(): is_fav=True

        for review in reviews:
            review.nStars = range(int(review.rating))
            review.nEmptyStars = range(5 - int(review.rating))
            print(review.nStars, review.nEmptyStars)
        rate = reviews.aggregate(Avg('rating'))['rating__avg']
        if rate:
            product.rate = rate
        else:
            product.rate = 0
        product.nStars, product.nEmptyStars  = range(int(product.rate)),range(5 - int(product.rate))
        productbenefits = Prod_Benefits.objects.filter(product=product)
        pricing = Product_Pricing_Plan.objects.filter(product=product)
        categories = product.category.all()
        totalpurchases = Purchase.objects.filter(product__exact=product).count()
        data= {'prod': product, 'revs': page_obj, 'prodbenefs': productbenefits,
               'plans': pricing, 'purch': totalpurchases, 'numreviews': numreviews, 'form_purch': form_purchases, ' form_fav':form_favorites, 'is_fav': is_fav }
        if  request.session.get("last_request_error") is not None:
            print("cucu")
            data["errors"]  = request.session.get("last_request_error")
            del request.session["last_request_error"]
        if   request.session.get("last_request_success") is not None:
            data["successes"] = request.session.get("last_request_success")
            del request.session["last_request_success"]
        return render(request, 'productdetails.html', data)


def fill_form(client):
    form = UpdateClientForm()
    form.fields['username'].initial = client.user.username
    form.fields['first_name'].initial = client.user.first_name
    form.fields['last_name'].initial = client.user.last_name
    form.fields['email'].initial = client.user.email
    return form



# ver isto melhor ta cancro como a merda
def accountDetails(request):
    user = User.objects.get(username=request.user.username)
    client = Client.objects.get(user_id=user.id)

    # favourites
    fav = client.favorites.all()

    if request.method == "POST":
        form = UpdateClientForm(request.POST, instance=request.user)
        form_pw = UpdatePasswordForm(request.user, request.POST)
        if 'old_password' not in request.POST:
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
                return render(request,'clientdetails.html',{'user': client, 'form': form, 'form_pw': form_pw, 'favourites': fav})
        else:
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
                return render(request,'clientdetails.html',{'user': client, 'form_pw': form_pw, 'form': form, 'favourites': fav})
    else:
        form = fill_form(client)
        form_pw = UpdatePasswordForm(request.user)

    return render(request, 'clientdetails.html', {'user': client, 'form': form, 'form_pw': form_pw, 'favourites': fav})


