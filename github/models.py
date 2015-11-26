from django.db import models

from users.models import User

# Create your models here.

class GithubIntegration(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	github_id = models.CharField(max_length=50)
	oauth_token = models.CharField(max_length=256)
	expires_at = models.DateTimeField()