from django.shortcuts import render
from .models import Postedjobs
from school.models import Newjob




def create_notification(recipient, message, subject):
    subject_instances = Newjob.objects.filter(subject=subject)
    for subject_instance in subject_instances:
        if not Postedjobs.objects.filter(recipient=recipient, message=message, subject=subject_instance).exists():
            notification = Postedjobs(recipient=recipient, message=message, subject=subject_instance)
            notification.save()



def view_notification(request):
    subject_notification = Postedjobs.objects.filter(recipient=request.user, message__startswith='A new job in', is_read=False).order_by('-created_at')

    unread_count = subject_notification.count()

    context = {'subject_notification':subject_notification, 'unread_count':unread_count}

    return render(request, 'notification/notification.html', context)