import logging
from django.conf import settings

from twilio.rest import Client

# Get an instance of a logger
logger = logging.getLogger(__name__)


SENDER_ID = "SENDHUT"

VERIFICATION_MESSAGE = "Use {} to verify your Sendhut account. \
DON'T SHARE IT WITH ANYONE. Know more: sendhut.com/safety"

LOGIN_ALERT_MESSAGE = "Somebody logged in your Sendhut account. \
Not you? Immediately reach us at sendhut.com/safety"


def send_sms(recipient, text):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTHTOKEN
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=text,
                        from_=settings.TWILIO_FROM_NUMBER,
                        messaging_service_sid=settings.TWILIO_MSG_SERVICE_SID,
                        to=recipient
                    )
    logger.debug("SMS ID %s", message.sid)


def alert_login(recipient):
    send_sms(recipient, LOGIN_ALERT_MESSAGE)


def push_verification_sms(recipient, token):
    send_sms(recipient, VERIFICATION_MESSAGE.format(token))
