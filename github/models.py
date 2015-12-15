from django.db import models

from users.models import User


class GithubIntegration(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	github_id = models.CharField(max_length=50)
	github_username = models.CharField(max_length=120)
	oauth_token = models.CharField(max_length=256)
	expires_at = models.DateTimeField()
	oauth_is_valid = models.BooleanField(default=False)

	class Meta:
		db_table = 'github_integrations'
