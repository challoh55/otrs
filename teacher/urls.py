from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_home, name='teacher_home'),
    path('teacher-resume/', views.Resume, name='teacher_resume'),
    path('update-resume/', views.update_resume, name='update_resume'),
    path('view-job/', views.view_job, name='view_job'),
    path('applied-jobs', views.applied_jobs, name='applied_jobs'),
    path('delete-application', views.delete_application, name='delete_application'),
    path('update-user-paid-status', views.update_user_paid_status, name='update_user_paid_status'),


]