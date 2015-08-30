# A custom written authentication backend for piper
#   for more info, see https://docs.djangoproject.com/en/dev/topics/auth/customizing/


from django.contrib.auth.hashers import check_password
from users.models import User


class UserAuthentication(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)

            if check_password(password, user.password):
                return user

            return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None