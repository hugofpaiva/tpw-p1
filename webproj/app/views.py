from django.shortcuts import render

# Create your views here.
#foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def renderBase(request):
    return render(request, 'base.html',{'activelem': 'home'})

def shopBaseView(request):
    return render(request,'shop.html',{'activelem': 'shop'})