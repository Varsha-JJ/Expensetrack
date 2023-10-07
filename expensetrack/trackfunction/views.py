from django.shortcuts import render,redirect
from django.conf import settings

# Create your views here.


def addexpense(request):
    return render(request,"addexpense.html")
