# A custom written authentication backend for piper
#   for more info, see https://docs.djangoproject.com/en/dev/topics/auth/customizing/

from django.conf import settings
from django.contrib.auth.hashers import check_password
from users.models import User

class UserAuthentication(object):


    def authenticate(self, username=None, password=None):
        
