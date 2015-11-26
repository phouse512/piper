from django.db import models

from users.models import User

# Create your models here.


class Integrations(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	network_id = models.IntegerField()
	type = models.CharField(max_length=30)
