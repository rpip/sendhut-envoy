import logging
from django.db.models import Q
from django.conf import settings

from .models import User

from sendhut.utils import generate_sms_token
from sendhut import factory
logger = logging.getLogger(__name__)


def get_user(username):
    # atm, username == phone_number
    if is_demo_number(username):
        return factory.get_demo_user()

    try:
        user = User.objects.filter(
            Q(username=username) |
            Q(phone=username) |
            Q(email=username))
        return user[0] if user else None
    except User.DoesNotExist:
        return None


def is_demo_number(phone_number):
    return phone_number[4:] == settings.DEMO_USER_NUMBER[4:]


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


def set_auth_token(phone, lock=True):
    # todo: implement login locking mechanism:
    # phone number logs in only one session.
    # for when lock is False, assume demo user
    r = settings.REDIS
    key = "auth:{}".format(phone)
    token = generate_sms_token(4) if lock else settings.DEMO_USER_TOKEN
    ttl = settings.SMS_TTL
    logger.debug("SMS token => %s: %s", key, token)
    r.setex(key, token, ttl)
    return token


def verify_token(phone, token):
    # checks that the token exists and hasn't expired
    r = settings.REDIS
    key = "auth:{}".format(phone)
    user_token = r.get(key)
    logger.debug("Verify SMS token => %s: %s # %s", key, token, user_token)
    return (user_token and user_token.decode('utf-8') == token)


def logout(user):
    user.auth_token.delete()
