"""
websocket feeds:

[
  "driver_locations.barcelona",
  {
    "id": 333644644,
    "created_at": "2018-06-17T19:09:51.932+02:00",
    "driver_id": 50406,
    "latitude": 41.43416173,
    "longitude": 2.2277651,
    "status": "on_duty",
    "transport_type": "motorbike"
  }
]
"""

class TransportTypes:
    """Enum of possible transport types"""
    BIKE = "bike"
    CAR = "car"
    VAN = "van"
    PICKUP = "pickup"
    TRUCK = "truck"

    CHOICES = [
        (BIKE, "bike"),
        (CAR, "car"),
        (VAN, "van"),
        (PICKUP, "pickup")
    ]


class PackageTypes:
    """Enum of possible package sizes"""
    EXTRA_SMALL = 'extra_small'
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

    CHOICES = [
        (EXTRA_SMALL, "Extra small"),
        (SMALL, "Small"),
        (MEDIUM, "Medium"),
        (LARGE, "Large"),
        (EXTRA_LARGE, "Extra large")
    ]


class DeliveryStatus:
    """Enum of possible delivery statuses."""

    PENDING = "pending"
    PICK_UP = "pick_up"
    ALMOST_PICKUP = "almost_pickup"
    WAITING_AT_PICKUP = "waiting_at_pickup"
    PICKUP_COMPLETE = "pickup_complete"
    DROPOFF = "dropoff"
    ALMOST_DROPOFF = "almost_dropoff"
    WAITING_AT_DROPOFF = "waiting_at_dropoff"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"
    RETURNED = "returned"
    SCHEDULED = "scheduled"
    EXPIRED = "expired"

    CHOICES = [
        (PENDING,  "Pending - We've accepted the delivery and will be assigning it to a courier"),
        (PICK_UP, "Pick Up - Courier is assigned and is en route to pick up the items"),
        (ALMOST_PICKUP, "Almost Pickup - The driver is close to the pickup point"),
        (WAITING_AT_PICKUP, "Waiting At Pickup The driver is waiting at the pickup point"),
        (PICKUP_COMPLETE, "Picking Complete - Courier has picked up the items"),
        (DROPOFF, "Dropoff - Courier is moving towards the dropoff"),
        (ALMOST_DROPOFF, "Almost Dropoff - The driver is close to the delivery point"),
        (WAITING_AT_DROPOFF, "Waiting At Dropoff - The driver is waiting at the delivery point"),
        (CANCELLED, "Cancelled -  Items won't be delivered. Deliveries are either canceled by the customer or by our customer service team"),
        (DELIVERED, "Delivered - The package has been delivered successfully"),
        (RETURNED, "Returned - The delivery was returned"),
        (SCHEDULED, "Scheduled - The job has been scheduled. It will start later"),
        (EXPIRED, "Expired - job has expired. No driver accepted the job. It didn't cost any money")
    ]


class CancellationReasons:
    """Enum of possible cancellation reasons"""
    ETA_TOO_LONG = "eta-too-long"
    NO_CONNECTION = "no-connection"

    CHOICES = [
        (ETA_TOO_LONG, "eta is too long"),
        (NO_CONNECTION, "couldn't connect to courier")
    ]


class ZoneRegions:
    """Enum of zones"""
    CHOICES = []
