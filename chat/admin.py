from django.contrib import admin
from .models import Message

# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'seen', 'date_created')
    
admin.site.register(Message, ChatAdmin)
