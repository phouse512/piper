import datetime

from django.db import models

# Create your models here.


class Users(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    pin = models.CharField(max_length=10)
    email = models.CharField(max_length=150)
    join_date = models.DateTimeField(default=datetime.datetime.now)
    points_total = models.DecimalField(default=0, decimal_places=3, max_digits=15)


class Poll(models.Model):

    id = models.AutoField(primary_key=True)
    open = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    weight = models.IntegerField(default=1)
    question = models.CharField(max_length=250)
    correct_id = models.IntegerField(default=None)
    created = models.DateTimeField(default=datetime.datetime.now)
    finish_time = models.DateTimeField()


class Answers(models.Model):

    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, related_name='answers')


class Votes(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, related_name='votes')
    poll = models.ForeignKey(Poll, related_name='votes')
    answer = models.ForeignKey(Answers, related_name='votes', default=1)
    created = models.DateTimeField(default=datetime.datetime.now)


class Scores(models.Model):

    id = models.AutoField(primary_key=True)
    points = models.DecimalField(default=0, decimal_places=3, max_digits=15)
    created = models.DateTimeField(default=datetime.datetime.now)
    vote = models.ForeignKey(Votes)
    user = models.ForeignKey(Users)
