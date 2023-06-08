# from django.contrib.auth.models import User
from main.models import User


class AuthBackend:
    """
    Custom authentication backend.

    Allows users to log in using their email address or name.
    """
    def authenticate(self, request, username=None, password=None):
        """
        Overrides the authenticate method to allow users to log in using their email address or name.
        """
        try:
            user = User.find_one({'name': username})
            # user = User.objects.get(email=username)
            if not user:
                user = User.find_one({'email': username})
            if user.try_login(password):
                return user
            return None
        except TypeError:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address or name.
        """
        try:
            return User.find_one({'_id': user_id})
        except TypeError:
            return None
