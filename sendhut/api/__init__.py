from schematics.models import Model
from schematics.types import StringType, ListType


class DeliveryQuoteRequest(Model):
    pickup = StringType(required=True)
    dropoffs = ListType(StringType, max_size=4, required=True)
