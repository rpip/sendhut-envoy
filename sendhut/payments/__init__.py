class TransactionTypes:
    """Enum of possible transactions"""
    LOAD_WALLET = "load-wallet"
    PAYMENT = "payment"
    WALLET_PAYMENT = "wallet-payment"

    CHOICES = [
        (LOAD_WALLET, "load wallet"),
        (PAYMENT, "payment"),
        (WALLET_PAYMENT, "wallet payment"),
    ]


class PaymentChannels:
    """Enum of possible Payment channels"""
    WALLET = "wallet"
    PAYMENT = "payment"

    CHOICES = [
        (WALLET, "wallet"),
        (PAYMENT, "payment"),
    ]
