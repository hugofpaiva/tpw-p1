from django.shortcuts import render
from app.forms import *
from app.models import *
# Create your views here.

#foi a maneira mais facil q arranjei para saber qual o elemento ativo na navbar, ja que o shop vai extender o base.html(navbars e essas merdas)
def renderBase(request):
    return render(request, 'base.html',{'activelem': 'home'})

def shopBaseView(request):
    print(Client.objects.get())
    return render(request,'shop.html',{'activelem': 'shop'})

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