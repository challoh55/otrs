from django.urls import path
from . import views

urlpatterns = [
    path('', views.school_home, name='school_home'),
    path('home/', views.school_home, name='home'),
    path('school-profile/', views.school_profile, name='school_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('view-teacher/', views.view_teacher, name='view_teacher'),
    path('view-posted-jobs/', views.view_posted_jobs, name='view_posted_jobs'),
    path('add-newjob/', views.add_new_job, name='add_newjob'),
    path('update-new-job/', views.update_new_job, name='update_new_job'),
    path('delete-job', views.delete_job, name='delete_job'),
    path('activate-job', views.activate_job, name='activate_job'),
    path('inactivate-job', views.inactivate_job, name='inactivate_job'),
    path('all-applicants/', views.all_applicants, name='all_applicants'),
    path('applicants-for-subject/<str:subject>/', views.applicants_for_subject, name='applicants_for_subject'),
    path('school-profile/update-user-paid-status', views.update_user_paid_status, name='update_user_paid_status'),

]