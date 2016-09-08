import datetime

from django.db import models

# Create your models here.


class Attendee(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    group_hash = models.CharField(max_length=10, default="test")


class Event(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    group_hash = models.CharField(max_length=10, default="test")
    date = models.DateField(default=datetime.datetime.now)
    on = models.BooleanField(default=False)


class EventAttendance(models.Model):

    id = models.AutoField(primary_key=True)
    first_time = models.IntegerField(default=0)
    attendee = models.ForeignKey(Attendee)
    event = models.ForeignKey(Event)

