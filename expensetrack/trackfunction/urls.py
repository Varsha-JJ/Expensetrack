from django.urls import path
from . import views

urlpatterns = [
    path('addexpense/',views.addexpense,name='addexpense'),
    path('viewexpense/',views.viewexpense,name='viewexpense'),
    path('editexpense/',views.editexpense,name='editexpense'),
    path('history/',views.history,name='history'),
    path('report/',views.report,name='report'),
]