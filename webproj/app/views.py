from django.shortcuts import render

# Create your views here.

def renderBase(request):
    return render(request, 'base.html')