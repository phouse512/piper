from django.shortcuts import render
from ingester.models import IngesterJob

# Create your views here.

# this method handles incoming calls from setcronjob, and triggers the action based on job_id
def trigger_job(request, job_id):

	job = IngesterJob.objects.filter(id=job_id)
	if not job:
	# 	task does not exist for whatever reason
		print "fail"

	return job_id
