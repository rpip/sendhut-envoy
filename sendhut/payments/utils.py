from django.conf import settings
from paystackapi.paystack import Paystack
from decimal import Decimal
from sendhut.utils import generate_token


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


def fund_wallet(wallet, amount, ref):
    return wallet.deposit_funds(amount, ref)


def withdraw_from_wallet(wallet, amount):
    return wallet.withdraw(amount)


def get_charge_ref(phone, amount):
    # todo: handle emails sent to phone@sendhut.com
    email = "{}@sendhut.com".format(phone)
    return init_transaction(amount, email).get("data")


def quantize(amount):
    CENTS = Decimal('0.01')
    return amount.quantize(CENTS)


def unquantize_for_paystack(amount):
    "Removes decimal point separators, required for Paystack format"
    return ''.join(str(amount).split('.'))
