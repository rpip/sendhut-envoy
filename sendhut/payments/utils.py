from django.conf import settings
from paystackapi.paystack import Paystack

from sendhut.utils import generate_token
from .models import Wallet


paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


def init_transaction(amount, email, reference=None):
    # TODO(yao): confirm Paystack max amount, why 33578.00, appears as 335.78
    return paystack.transaction.initialize(
        reference=reference or generate_token(),
        amount=amount,
        email=email
    )


def verify_transaction(reference):
    response = paystack.transaction.verify(reference)
    return response['status']


def fund_wallet(user, amount, ref):
    return Wallet.deposit_money(user.service_wallet, amount, ref)


def withdraw_from_wallet(user, amount):
    return Wallet.withdraw(user.service_wallet, amount)
