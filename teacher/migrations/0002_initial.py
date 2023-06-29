# Generated by Django 4.2.1 on 2023-06-27 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('teacher', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('idnumber', models.IntegerField()),
                ('dob', models.DateField()),
                ('description', models.TextField(default=False)),
                ('image', models.ImageField(upload_to='profile_pics')),
                ('resume', models.FileField(upload_to='resumes')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='newjob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.newjob'),
        ),
        migrations.AddField(
            model_name='application',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
