# P2PTransfer:
# - from: Sender
# - to: Recipient
# - Amount
# - Description
# - Created
# - Updated
# - # CRUD
# - https://monzo.com/blog/2018/04/05/how-monzo-to-monzo-payments-work/


class TransactionTypes:
    """Enum of possible transactions"""
    LOAD_WALLET = "load-wallet"
    PAYMENT = "wallet-payment"

    CHOICES = [
        (LOAD_WALLET, "load wallet"),
        (PAYMENT, "payment"),
    ]


class PaymentChannels:
    """Enum of possible Payment channels"""
    WALLET = "wallet"
    CASH = "cash"

    CHOICES = [
        (WALLET, "wallet"),
        (CASH, "cash"),
    ]
