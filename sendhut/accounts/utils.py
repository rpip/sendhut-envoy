import logging
from django.db.models import Q
from django.conf import settings

from .models import User

from sendhut.utils import generate_sms_token

logger = logging.getLogger(__name__)


def get_user(username):
    try:
        user = User.objects.filter(
            Q(username=username) |
            Q(phone=username) |
            Q(email=username))
        return user[0] if user else None
    except User.DoesNotExist:
        return None


# users
def create_user(phone, first_name=None, last_name=None, email=None):
    user = User(
        phone=phone, username=phone,
        email=email, first_name=first_name,
        last_name=last_name)

    user.save()
    return user


def authenticate(username, token):
    user = get_user(username)
    if user and verify_token(user, token):
        return user

    return None


def set_auth_token(phone):
    r = settings.REDIS
    key = "auth:{}".format(phone)
    token = generate_sms_token(4)
    # expires in 3 minutes
    r.setex(key, token, 180)
    return token


def verify_token(phone, token):
    # checks that the token exists and hasn't expired
    r = settings.REDIS
    user_token = r.get("auth:{}".format(phone))
    return (user_token and user_token.decode('utf-8') == token)


def logout(user):
    user.auth_token.delete()
