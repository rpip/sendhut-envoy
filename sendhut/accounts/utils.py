import logging
from django.db.models import Q

from .models import User


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
def create_user(phone, password, email=None):
    user = User(phone=phone, username=phone)
    if email:
        user.email = email
    user.set_password(password)
    user.save()
    return user


def authenticate(username, password):
    user = get_user(username)
    if user and user.check_password(password):
        return user

    return None


def trigger_password_reset(username):
    # send sms if username is phone, else email
    logger.log('sending password reset')


def change_password(user, old_password, new_password):
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()

    return False


def logout(user):
    user.auth_token.delete()
