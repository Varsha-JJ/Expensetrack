from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('addexpense/',views.addexpense,name='addexpense'),
    path('viewexpense/',views.viewexpense,name='viewexpense'),
    path('editexpense/',views.editexpense,name='editexpense'),
    path('history/',views.history,name='history'),
    path('report/',views.report,name='report'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
]