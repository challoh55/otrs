from django.db import models
from users.models import User
from school.models import Newjob



# Teacher resume model 
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    idnumber = models.IntegerField()
    dob = models.DateField()
    description = models.TextField(default=False)
    image = models.ImageField(upload_to='profile_pics')
    resume = models.FileField(upload_to='resumes')
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    

# application model
class Application(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    newjob = models.ForeignKey(Newjob, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.teacher)
