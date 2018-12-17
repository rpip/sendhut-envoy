from django.conf import settings
from paystackapi.paystack import Paystack

from sendhut.utils import generate_token


paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


def init(amount, email, reference=None):
    # TODO(yao): confirm Paystack max amount, why 33578.00, appears as 335.78
    return paystack.transaction.initialize(
        reference=reference or generate_token(),
        amount=amount,
        email=email
    )


def verify_transaction(reference):
    response = paystack.transaction.verify(reference)
    return response['status']
