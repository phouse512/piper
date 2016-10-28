from django.contrib import admin
from poller.models import Poll
from poller.models import Answers
from poller.models import Votes
from poller.models import Scores
from poller.models import Users

# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ['question']

admin.site.register(Poll, PollAdmin)
admin.site.register(Answers)
admin.site.register(Votes)
admin.site.register(Scores)
admin.site.register(Users)


