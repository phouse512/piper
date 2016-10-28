from django.contrib import admin
from poller.models import Poll
from poller.models import Answers
from poller.models import Votes
from poller.models import Scores
from poller.models import Users

# Register your models here.

admin.site.register(Poll)
admin.site.register(Answers)
admin.site.register(Votes)
admin.site.register(Scores)
admin.site.register(Users)


class PollAdmin(admin.ModelAdmin):
    list_display = ['question']