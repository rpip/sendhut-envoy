class DeliveryVolumes:
    """Enum of possible cancellation rea"""
    KICKING_OFF = "kicking-off"
    GROWING = "growing"
    EXPANDING = "expanding"
    SCALING = "scaling"

    CHOICES = [
        (KICKING_OFF, "0-50 deliveries per month"),
        (GROWING, "0-100 deliveries per month"),
        (EXPANDING, "100-200 deliveries per month"),
        (SCALING, "300+ deliveries per month")
    ]
