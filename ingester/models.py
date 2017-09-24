from django.db import models

# THIS IS DEPRECATED
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


class IngesterJob(models.Model):
	id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=300)
	last_run = models.DateTimeField()
	job_class = models.CharField(max_length=30)

	class Meta:
		db_table = 'ingester_job'


# TODO: these might later become relevant once we try to further generalize
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
