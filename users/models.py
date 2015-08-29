from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	password = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	access_token = models.CharField(unique=True, max_length=400)
	last_action = models.DateTimeField(default=timezone.now)