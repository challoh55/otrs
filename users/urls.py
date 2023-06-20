from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage, name='home-page'),
    path('home/', views.Homepage, name='home'),
    path('registerteacher/', views.RegisterTeacher, name='register-teacher'),
    path('registerschool/', views.RegisterSchool, name='register-school'),
    path('login/', views.Login, name='login-user'),
    path('logout/', views.Logout, name='logout-user'),
]