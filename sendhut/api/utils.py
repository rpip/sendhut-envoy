from django.template.defaultfilters import slugify

from sendhut.accounts.models import User
from sendhut.accounts.utils import get_user
from sendhut.utils import generate_random_name


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
    pass


def change_password(user, new_password):
    user.set_password(new_password)
    user.save()


def logout(user):
    user.auth_key.delete()


def update_model_fields(instance, data):
    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()
    return instance


# delivery
def create_delivery(data):
    pass


def get_deliveries(user, status):
    pass


def delivery_detail(delivery_id):
    pass
