from django.shortcuts import render
from .models import Postedjobs, ApplicationNotifs
from school.models import Newjob
from teacher.models import Application



def create_postedjob_notification(recipient, message, subject):
    subject_instances = Newjob.objects.filter(subject=subject)
    for subject_instance in subject_instances:
        if not Postedjobs.objects.filter(recipient=recipient, message=message, subject=subject_instance).exists():
            notification = Postedjobs(recipient=recipient, message=message, subject=subject_instance)
            notification.save()

def create_application_notification(recipient, message, application):
    application_instance = Application.objects.get(id=application)
    if not ApplicationNotifs.objects.filter(recipient=recipient, message=message, application=application_instance).exists():
        notification = ApplicationNotifs(recipient=recipient, message=message, application=application_instance)
        notification.save()



def view_notification(request):
    username = request.user.username

    subject_notification = Postedjobs.objects.filter(recipient=request.user, message__startswith='A new job in', is_read=False).order_by('-created_at')
    unread_count = subject_notification.count()

    application_notification = ApplicationNotifs.objects.filter(recipient=request.user, message__startswith='A new application', is_read=False).order_by('-created_at')
    unread_count1 = application_notification.count()

    context = {'username':username, 'subject_notification':subject_notification, 'unread_count':unread_count, 'application_notification':application_notification, 'unread_count1':unread_count1}

    return render(request, 'notification/notification.html', context)