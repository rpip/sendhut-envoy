from django.conf import settings

from sendhut.checkout.models import Order
from sendhut.stores.models import FOOD_TAGS
from sendhut import utils


def get_setting_as_dict(name, short_name=None):
    short_name = short_name or name
    try:
        return {short_name: getattr(settings, name)}
    except AttributeError:
        return {}


# request is a required parameter
# pylint: disable=W0613
def default_currency(request):
    return get_setting_as_dict('DEFAULT_CURRENCY')


def mobile_check(request):
    return {'is_mobile': utils.is_mobile(request)}
