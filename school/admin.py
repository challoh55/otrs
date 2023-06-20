from django.contrib import admin
from .models import School, Newjob

# display School table in admins page
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'description', 'address', 'website', 'contact', 'school_type')
    
admin.site.register(School, SchoolAdmin)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school', 'subject', 'salary', 'description', 'requirements', 'qualifications', 'created_at', 'is_active')
    
admin.site.register(Newjob, SchoolAdmin)