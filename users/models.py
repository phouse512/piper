from django.core.serializers.python import Serializer
from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    last_action = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'


class AccountLogin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    action_time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'account_logins'


class UserTokens(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_tokens'


class UserSerializer(Serializer):
    def end_object( self, obj ):
        self._current['id'] = obj._get_pk_val()
        self.objects.append( self._current )
