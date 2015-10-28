from django.db import models

from users.models import User


class Group(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)

	class Meta:
		db_table = 'groups'


class GroupMembership(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)

	class Meta:
		db_table = 'groups_membership'
