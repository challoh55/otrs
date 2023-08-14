from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Homepage, name='home-page'),
    path('registerteacher/', views.RegisterTeacher, name='register-teacher'),
    path('registerschool/', views.RegisterSchool, name='register-school'),
    path('login/', views.Login, name='login-user'),
    path('logout/', views.Logout, name='logout-user'),
    path('delete-user/', views.delete_user, name='delete_user'),
    # path('pay/', views.pay, name='pay'),
    path('update-user-paid-status', views.update_user_paid_status, name='update_user_paid_status'),


    #reports
    path('reports/', views.reports, name='reports'),
    path('create-pdf', views.pdf_report_create, name='create_pdf'),

    #users Password reset
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='users/password/password_reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password/password_reset_form.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password/password_reset_done.html'), name='password_reset_complete'),
]