from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from sendhut.db import BaseModel, BaseQuerySet, BaseManager
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from sendhut.utils import sane_repr, generate_token


from . import TransactionTypes


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

    def load_funds(self, amount, ref):
        # log new wallet top transaction
        return Transaction.fund_wallet(self, amount, ref)

    def withdraw(self, amount):
        return Transaction.withdraw_from_wallet(self, amount)

    @property
    def deposits(self):
        return Transaction.get_wallet_deposits(self)

    @property
    def total_deposits(self):
        return sum(x.amount for x in self.deposits)

    @property
    def total_withdrawals(self):
        return sum(x.amount for x in self.withdrawals)

    @property
    def balance(self):
        return self.total_deposits - self.total_withdrawals

    @property
    def withdrawals(self):
        return Transaction.get_wallet_withdrawals(self)

    @property
    def is_empty(self):
        return self.balance.amount > 0


class Transaction(BaseModel):

    ID_PREFIX = 'txn'

    wallet = models.ForeignKey(Wallet, related_name='transactions')
    txn_type = models.CharField(
        max_length=32, choices=TransactionTypes.CHOICES
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
    def withdraw(cls, wallet, amount):
        return cls.objects.create(
            wallet=wallet,
            amount=-amount,
            reference=generate_token(),
            txn_type=TransactionTypes.WALLET_PAYMENT
        )

    @classmethod
    def load_money(cls, wallet, amount, ref):
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
        )

    @classmethod
    def get_wallet_withdrawals(cls, wallet):
        return cls.objects.filter(
            wallet=wallet,
            txn_type=TransactionTypes.WALLET_PAYMENT
        )
