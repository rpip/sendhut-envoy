import logging
import requests
from urllib.parse import urlencode, quote_plus
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)


SENDER_ID = "SENDHUT"

SUCCESS_CODE = 1000


VERIFICATION_MESSAGE = "Use {} to verify your Sendhut account. \
DON'T SHARE IT WITH ANYONE. Know more: sendhut.com/safety"

LOGIN_ALERT_MESSAGE = "Somebody logged in your Sendhut account. \
Not you? Immediately reach us at sendhut.com/safety"


def send_sms(recipient, message):
    params = dict(
        msg=message,
        to=recipient,
        sender_id=SENDER_ID,
        key=settings.MNOTIFY_API_KEY
    )
    params = urlencode(params, quote_via=quote_plus)
    url = "{}?{}".format(settings.MNOTIFY_SERVER_URL, params)
    response = requests.get(url).json()
    if response != SUCCESS_CODE:
        # Log an error message
        logger.error("SMS failed: %s", response["message"])
        return False

    return True


def alert_login(number):
    send_sms(number, LOGIN_ALERT_MESSAGE)


def push_verification_sms(recipient, token):
    send_sms(recipient, VERIFICATION_MESSAGE.format(token))
