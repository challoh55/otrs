from django.contrib import admin
from .models import Teacher, Application

# display teacher table in admins page

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'phonenumber', 'subject', 'location', 'idnumber', 'dob', 'gender', 'image', 'resume', 'description')
    
    
admin.site.register(Teacher, TeacherAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'newjob_id', 'teacher_id', 'teacher','newjob', 'application_date', 'status')

admin.site.register(Application, ApplicationAdmin)