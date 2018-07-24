from sendhut.accounts.models import User
from sendhut.utils import generate_random_name


# users
def create_user(phone, email, password):
    username = generate_random_name()
    user = User(phone=phone, email=email, username=username)
    user.set_password(password)
    user.save()
    return user


def authenticate(username, password):
    pass


def trigger_password_reset(username):
    pass


def change_password(user, new_password, new_password_repeat):
    pass


def logout(self):
    pass


def update_model_fields(instance, data):
    pass
