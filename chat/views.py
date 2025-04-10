from notification.models import ApplicationNotifs, Postedjobs
from django.db.models import Q
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import User, Message


@login_required
def chat_room(request, user_id):
    username = request.user.username

    application_notification = ApplicationNotifs.objects.filter(recipient=request.user, message__startswith='A new application', is_read=False)
    unread_count1 = application_notification.count() 

    subject_notification = Postedjobs.objects.filter(recipient=request.user, message__startswith='A new job in', is_read=False).order_by('-created_at')
    unread_count = subject_notification.count()    


    # gets other user to chat with
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(Q(receiver=request.user, sender=other_user)).order_by('date_created')

    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user))

    user_list = User.objects.all()
    user = request.user

    unread_messages_count = {}  
    for user2 in user_list:
        unread_messages = Message.objects.filter(receiver=user, sender=user2, seen=False)
        unread_messages_count[user2.id] = unread_messages.count()
        # print(f"Unread messages for user {user2.username}: {unread_messages_count[user2.id]}")

    context = {'unread_count':unread_count, 'unread_count1':unread_count1, 'username':username, 'other_user': other_user, 'messages': messages, 'user_list': user_list, 'unread_messages_count': unread_messages_count}
    return render(request, 'chat/chatroom.html', context)


@login_required
def ajax_load_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(seen=False).filter(Q(receiver=request.user, sender=other_user)).order_by('date_created')
    message_list = [{
        'seen': message.sender.username,
        'message': message.message,
        'sent': message.sender == request.user
    }for message in messages]

    messages.update(seen=True)

    if request.method == 'POST':
        message = json.loads(request.body)
        m = Message.objects.create(receiver=other_user, sender=request.user, message=message)
        message_list.append({
            'sender': request.user.username,
            'message': m.message,
            'sent': True,
        })
    return JsonResponse(message_list, safe=False)
