from django.db import models
from djcelery.models import PeriodicTask


class IngesterTask(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.CharField(max_length=200)
	type = models.CharField(max_length=6)
	json_selector = models.CharField(max_length=100)
	frequency = models.CharField(max_length=30)
	periodic_task = models.ForeignKey(PeriodicTask)
	integration_type = models.CharField(max_length=30)

	class Meta:
		db_table = 'ingester_task'


class IngesterTaskParams(models.Model):
	id = models.AutoField(primary_key=True)
	task = models.ForeignKey(IngesterTask)
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)

	class Meta:
		db_table = 'ingester_task_params'


class IngesterTaskHeaders(models.Model):
	id = models.AutoField(primary_key=True)
	task = models.ForeignKey(IngesterTask)
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)

	class Meta:
		db_table = 'ingester_task_headers'
