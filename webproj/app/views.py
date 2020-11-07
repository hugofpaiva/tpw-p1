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
        product.rate = Reviews.objects.filter(product__exact=product).aggregate(Avg('rating'))['rating__avg']
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
