from django.db import models

# Create your models here.


class Attendee(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    group_hash = models.CharField(max_length=10, default="test")
