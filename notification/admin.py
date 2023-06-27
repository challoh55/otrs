from django.contrib import admin
from .models import Postedjobs, ApplicationNotifs

#posted jobs notifications admin
class PostedjobsAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'message', 'is_read', 'created_at')
    
admin.site.register(Postedjobs, PostedjobsAdmin)


#application notifications admin
class ApplicationNotifsAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'application', 'message', 'is_read', 'created_at')
    
admin.site.register(ApplicationNotifs, ApplicationNotifsAdmin)