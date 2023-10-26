from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('base/',views.base,name='base'),
    path('forgotpwd/',views.forgotpwd,name='forgotpwd'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
]