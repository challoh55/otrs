from django.db import models
from users.models import User

# school profile model 
class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default=False)
    address = models.CharField(max_length=100, default=False)
    description = models.TextField(default=False)
    contact = models.CharField(max_length=20, default=False)
    website = models.URLField(default=False)
    school_type =models.CharField(max_length=100, default=False)


    def __str__(self):
        return self.user.username

#new job model
class Newjob(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE) 
    subject = models.CharField(max_length=100, null=True)
    salary = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    requirements = models.TextField(null=True)
    qualifications = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject