import six
from uuid import uuid4

from django.contrib.gis.db import models

from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from sendhut.utils import sane_repr, image_upload_path

from sendhut.db import BaseModel

# https://www.hypertrack.com/blog/2017/08/23/guide-storing-querying-serializing-location-data-django-postgresql/


class Image(BaseModel):

    ID_PREFIX = 'img'

    ONE_DAY = 60 * 60 * 24

    image = ImageField(upload_to=image_upload_path)

    class Meta:
        db_table = "image"

    def generate_unique_path(cls, timestamp):
        pieces = [six.text_type(x) for x in divmod(
            int(timestamp.strftime('%s')), cls.ONE_DAY)]
        pieces.append(uuid4().hex)
        return u'/'.join(pieces)

    def thumb_sm(self):
        return get_thumbnail(self.image, '128x128', crop='center')

    def thumb_lg(self):
        return get_thumbnail(self.image, '585x312', crop='center')

    def __str__(self):
        return str(self.id)


class Address(BaseModel):

    ID_PREFIX = 'add'

    # actual address
    address = models.CharField(max_length=120)
    # apt number or company name
    apt = models.CharField(max_length=42, null=True, blank=True)
    # geo co-ordinates: lat,lon
    location = models.PointField(null=True, spatial_index=True, geography=True)
    photo = models.ForeignKey(Image, related_name='address', blank=True, null=True)
    notes = models.CharField(max_length=252, null=True, blank=True)

    class Meta:
        db_table = 'address'

    __repr__ = sane_repr('county', 'city', 'postcode')

    def __str__(self):
        return self.address


class Contact(BaseModel):

    ID_PREFIX = 'cnt'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=40, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)
