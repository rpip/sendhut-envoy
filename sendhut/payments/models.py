from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from sendhut.db import BaseModel, BaseQuerySet, BaseManager
from djmoney.models.fields import MoneyField

from sendhut.utils import sane_repr, generate_token


from . import TransactionTypes, PaymentChannels


class WalletQuerySet(BaseQuerySet):
    """
    A specialized queryset for dealing with wallets.
    """
    def get_service_wallet(self, user):
        """Return scheduled deliveries"""
        return self.filter(user=user).first()


class WalletManager(BaseManager):
    pass


class Wallet(BaseModel):
    """service wallet"""

    ID_PREFIX = 'wlt'

    user = models.ForeignKey(get_user_model(), related_name='wallets')

    class Meta:
        db_table = 'wallet'

    __repr__ = sane_repr('user',)

    def __str__(self):
        return "<%s>: %d".format(self.id, self.get_balance())

    objects = WalletManager.from_queryset(WalletQuerySet)()

    def deposit_funds(self, amount, ref):
        # log new wallet top transaction
        return Transaction.fund_wallet(self, amount, ref)

    def make_payment(self, amount):
        return Transaction.pay_from_wallet(self, amount)

    @property
    def deposits(self):
        return Transaction.get_wallet_deposits(self)

    @property
    def total_deposits(self):
        return sum(x.amount for x in self.deposits)

    @property
    def withdrawals(self):
        return Transaction.get_wallet_withdrawals(self)

    @property
    def total_withdrawals(self):
        return sum(x.amount for x in self.withdrawals)

    @property
    def balance(self):
        return self.total_deposits - self.total_withdrawals

    @property
    def is_empty(self):
        return self.balance.amount > 0

    @property
    def discount_rate(self):
        return settings.WALLET_DISCOUNT_RATE


class Transaction(BaseModel):

    ID_PREFIX = 'txn'

    wallet = models.ForeignKey(
        Wallet, related_name='transactions', null=True, blank=True)
    reference = models.CharField(max_length=40, blank=True, null=True)
    txn_type = models.CharField(
        max_length=32, choices=TransactionTypes.CHOICES
    )
    channel = models.CharField(
        max_length=32, choices=PaymentChannels.CHOICES,
        null=True, blank=True
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        null=True, blank=True
    )

    class Meta:
        db_table = 'transactions'

    __repr__ = sane_repr('wallet', 'type', 'amount')

    @classmethod
    def pay_from_wallet(cls, wallet, amount):
        cls.make_payment(
            amount=amount,
            wallet=wallet,
            txn_type=TransactionTypes.WALLET_PAYMENT,
            channel=TransactionTypes.WALLET
        )

    @classmethod
    def make_payment(
            cls, amount, txn_type, channel,
            reference=None, wallet=None):
        return cls.objects.create(
            amount=amount,
            reference=reference or generate_token(),
            txn_type=txn_type,
            wallet=wallet
        )

    @classmethod
    def fund_wallet(cls, wallet, amount, ref):
        return cls.objects.create(
            wallet=wallet,
            amount=amount,
            reference=ref,
            txn_type=TransactionTypes.LOAD_WALLET
        )

    @classmethod
    def get_wallet_deposits(cls, wallet):
        return cls.objects.filter(
            wallet=wallet,
            txn_type=TransactionTypes.LOAD_WALLET
        ).all()

    @classmethod
    def get_wallet_withdrawals(cls, wallet):
        return cls.objects.filter(
            wallet=wallet,
            txn_type=TransactionTypes.WALLET_PAYMENT
        ).all()


class ServicePayment(BaseModel):
    """
    Service payment.

    Reference for payment transactions
    """
    ID_PREFIX = 'pay'
    channel = models.CharField(
        max_length=32, choices=PaymentChannels.CHOICES
    )
