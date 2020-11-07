from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.db.models import Min, Avg
from app.forms import *
from app.models import *
# Create your views here.

#foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def renderBase(request):
    return render(request, 'base.html',{'activelem': 'home'})

def shopBaseView(request):
    return render(request, 'shop.html', {'activelem': 'shop'})

def shopSearchView(request, prodName, pageNumber):
    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12
    products = Product.objects.filter(name__icontains=prodName)
    productsOffset = products[offset:offset+12]
    totalProducts=products.count()

    for product in productsOffset:
        product.price = Product_Pricing_Plan.objects.filter(product__exact=product).aggregate(Min('price'))
        product.rate = int(Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg'])
    return render(request,'shop.html',{'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,'totalPages': round(totalProducts/12), 'actualPage':pageNumber})

def register(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            client = Client(user=user)
            client.save()
            return render(request,'base.html',{'activelem': 'home'})
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form':form})

def prodDetails(request,idprod):
    try:
        product=Product.objects.get(id=idprod)
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request,'productdetails.html',{'prod':product})
