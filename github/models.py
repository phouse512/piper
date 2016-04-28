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


class CommitLog(models.Model):
    id = models.AutoField(primary_key=True)
    github_id = models.IntegerField()  # github id of the user
    time = models.DateTimeField()
    sha = models.CharField(max_length=200)  # unique id of commit
    additions = models.IntegerField()
    deletions = models.IntegerField()

    class Meta:
        db_table = 'commit_log'


class FileModificationLog(models.Model):
    id = models.AutoField(primary_key=True)
    commit = models.ForeignKey(CommitLog)
    status = models.CharField(max_length=50)
    additions = models.IntegerField()
    deletions = models.IntegerField()
    file_name = models.CharField(max_length=200)
    file_extension = models.CharField(max_length=20)

    class Meta:
        db_table = 'file_modification_log'
