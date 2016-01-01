import requests

from piper import settings

BASE_URL = "https://www.setcronjob.com/api/"

class CronJobApi(object):

	def __init__(self):
		self.access_key = settings.CRON_JOB_KEY


	def create_cronjob(self, datetime, callback_url):
		result = requests.post("")


	def delete_cronjob(self, cron_id):
		result = requests.post()

	def get_all_cronjobs(self):
		result = requests.get("")

