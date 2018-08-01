from decimal import Decimal
from urllib.parse import urljoin
from datetime import datetime, timedelta
from functools import singledispatch
from enum import Enum
import json
import hashlib
import random
import string
import re

from dateutil import parser
from django.conf import settings
from django.utils.encoding import iri_to_uri
from django.contrib.sites.models import Site

from faker import Faker
import redis
from djmoney.money import Money
from django.core.serializers.json import DjangoJSONEncoder


MOBILE_AGENT_RE = re.compile(r".*(iphone|ios|mini|mobile|androidtouch)", re.IGNORECASE)

REDIS = redis.StrictRedis(
    host=settings.REDIS_URL.hostname,
    port=settings.REDIS_URL.port,
    password=settings.REDIS_URL.password)


def sane_repr(*attrs):
    if 'id' not in attrs and 'pk' not in attrs:
        attrs = ('id', ) + attrs

    def _repr(self):
        cls = type(self).__name__

        pairs = ('%s=%s' % (a, repr(getattr(self, a, None))) for a in attrs)

        return u'<%s at 0x%x: %s>' % (cls, id(self), ', '.join(pairs))

    return _repr


def image_upload_path(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)

    return 'uploads/%s%s' % (
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower()
    )


def generate_token(length=14):
    "Returns a random alphanumeric string with the given length."
    chars = random.choices(string.ascii_letters + string.digits, k=length)
    return ''.join(chars)


def hash_data(data, hash_length=190, data_type=None):
    salt = "ValentinaIsTheMostAwsomeDogInTheWord"
    if data:
        data = "{}{}".format(data, salt)
        data_hashed = hashlib.sha512(data.encode('utf-8')).hexdigest()
        data_hashed = data_hashed[0:hash_length]
    else:
        data_hashed = None
    return data_hashed


def generate_random_name():
    fake = Faker()
    token = generate_token()
    word = '{}-{}-{}'.format(token, fake.color_name(), fake.street_name())
    return word.replace(' ', '-')


def unslugify(text):
    return text.replace('-', ' ').replace('_', ' ')


def is_mobile(request):
    """Return True if the request comes from a mobile device."""
    UA = request.META.get('HTTP_USER_AGENT')
    if UA:
        if MOBILE_AGENT_RE.match(UA):
            return True

    return False


def generate_password_token(email):
    token = generate_token(13)
    REDIS.setex(token, 60 * 5, email)
    return token


def check_password_token(token):
    return REDIS.get(token)


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)


@to_serializable.register(datetime)
def ts_datetime(val):
    """Used if *val* is an instance of datetime."""
    return val.isoformat() + "Z"


@to_serializable.register(Money)
def ts_money(val):
    """Used if *val* is an instance of Money."""
    return val.amount


class JSONSerializer:
    """
    Simple wrapper around json for session serialization
    """
    def dumps(self, obj):
        serialized = json.dumps(obj, separators=(',', ':'), default=to_serializable)
        return serialized.encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))


class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except:
            return json_encode(obj)


def json_encode(data):
    return json.dumps(data, default=to_serializable)


def build_absolute_uri(location):
    # type: (str, bool, saleor.site.models.SiteSettings) -> str
    host = Site.objects.get_current().domain
    protocol = 'https' if settings.ENABLE_SSL else 'http'
    current_uri = '%s://%s' % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)


def quantize(amount):
    CENTS = Decimal('0.01')
    return amount.quantize(CENTS)


def unquantize_for_paystack(amount):
    "Removes decimal point separators, required for Paystack format"
    return ''.join(str(amount).split('.'))


def asap_delivery_estimate():
    return datetime.now() + timedelta(minutes=35)


def windows_from_time_string(time_str):
    start, end = time_str.split('-')
    return parser.parse(start.strip()), parser.parse(end.strip())


def update_model_fields(instance, data):
    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()
    return instance
