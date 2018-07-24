from django.db.models import Q
from .models import User


def get_user(username):
    try:
        user = User.objects.filter(
            Q(username=username) |
            Q(phone=username) |
            Q(email=username))
        user = user[0] if user else None
    except User.DoesNotExist:
        return None
