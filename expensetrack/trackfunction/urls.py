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
    path('generate_pdf_yearly/', views.generate_pdf_yearly, name='generate_pdf_yearly'),
    path('generate_pdf_monthly/', views.generate_pdf_monthly, name='generate_pdf_monthly'),
    path('generate_pdf_file_category/', views.generate_pdf_file_category, name='generate_pdf_file_category'),


    

    
]

    
