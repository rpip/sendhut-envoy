from schematics.models import Model
from schematics.types import StringType, ListType
from schematics.exceptions import DataError


class Schema(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def is_valid(self):
        try:
            self.validate()
            return True, self.to_primitive()
        except DataError as ex:
            errors = {k: v.to_primitive() for k, v in ex.messages.items()}
            return False, errors


class DeliveryQuoteRequest(Schema):
    pickup = StringType(required=True)
    dropoffs = ListType(StringType, max_size=4, required=True)
