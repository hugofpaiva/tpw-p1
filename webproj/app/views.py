from django.shortcuts import render
from django.db.models import Min, Avg
from app.models import Product, Product_Pricing_Plan, Reviews

# Create your views here.
#foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def renderBase(request):
    return render(request, 'base.html',{'activelem': 'home'})

def shopBaseView(request):
    return render(request,'shop.html',{'activelem': 'shop'})

def shopSearchView(request, prodName, pageNumber):
    if pageNumber<1:
        return render(request, 'notfound.html')

    offset = (pageNumber-1)*12
    products = Product.objects.filter(name__icontains=prodName)
    productsOffset = products[offset:offset+12]
    totalProducts=products.count()

    for product in productsOffset:
        product.price = Product_Pricing_Plan.filter(product__exact=product).aggregate(Min('price'))
        product.rate = int(Reviews.filter(product__exact=product).aggregate(Avg('rating')))
    return render(request,'shop.html',{'activelem': 'shop', 'products': productsOffset, 'totalProducts': totalProducts,'totalPages': round(totalProducts/12), 'actualPage':pageNumber})