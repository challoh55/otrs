from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Postedjobs
class PostedjobsAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'message', 'is_read', 'created_at')
    
admin.site.register(Postedjobs, PostedjobsAdmin)