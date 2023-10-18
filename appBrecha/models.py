from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Contact(models.Model):
    PLAN_CHOICES = (
        ('free', 'Free'),
        ('plus', 'Plus'),
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.full_name
