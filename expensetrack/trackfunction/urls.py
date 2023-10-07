from django.urls import path
from . import views

urlpatterns = [
    path('addexpense/',views.addexpense,name='addexpense'),
]