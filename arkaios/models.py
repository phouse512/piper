import datetime

from django.core.serializers.python import Serializer
from django.db import models
from django.core.urlresolvers import reverse
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


class EventSerializer(Serializer):
    def get_dump_object(self, obj):
        self._current['event_date'] = str(obj.date)
        self._current.pop('date')
        self._current['id'] = obj.id
        self._current['url'] = reverse('track', kwargs={
            'group_hash': self._current['group_hash'],
            'event_id': self._current['id']})
        self._current['csv_url'] = reverse('csv', kwargs={
            'group_hash': self._current['group_hash'],
            'event_id': self._current['id']})

        return self._current


class EventAttendance(models.Model):

    id = models.AutoField(primary_key=True)
    first_time = models.IntegerField(default=0)
    attendee = models.ForeignKey(Attendee)
    event = models.ForeignKey(Event)
    timestamp = models.DateTimeField(default=datetime.datetime.now)


class Group(models.Model):

    id = models.AutoField(primary_key=True)
    group_hash = models.CharField(max_length=10, default="test")
    name = models.CharField(max_length=40)


class GroupAdmin(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    group = models.ForeignKey(Group)


class GroupGrades(models.Model):

    id = models.AutoField(primary_key=True)
    group_hash = models.CharField(max_length=10, default="test")
    option_value = models.CharField(max_length=30)


class AdminUsers(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    pw_hash = models.CharField(max_length=512)
    last_login = models.DateTimeField(default=datetime.datetime.now)
