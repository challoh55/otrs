# Generated by Django 4.2.1 on 2023-07-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
    ]
