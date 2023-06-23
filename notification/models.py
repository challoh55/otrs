from django.db import models

# Create your models here.
from users.models import User
from school.models import Newjob




class Postedjobs(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Newjob, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
