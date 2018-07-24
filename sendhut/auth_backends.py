from django.contrib.auth.hashers import check_password
from sendhut.accounts.models import User
from sendhut.accounts.utils import get_user


class UsernamePhoneAuthentication:

    def authenticate(self, request, username=None, password=None):
        user = get_user(username)
        if user:
            # Check password of the user we found
            if check_password(password, user.password):
                return user

        # No user was found, return None - triggers default login failed
        return None

    # Required for the backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
