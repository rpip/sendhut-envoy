from django.contrib.gis.db import models
from jsonfield import JSONField
from django.urls import reverse

from safedelete.models import SafeDeleteModel
from safedelete.admin import SafeDeleteAdmin, highlight_deleted
from safedelete.models import SOFT_DELETE_CASCADE, HARD_DELETE

from sendhut.utils import generate_token


class UpdateMixin(object):
    def update(self, **kwargs):
        if self._state.adding:
            raise self.DoesNotExist
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())


class BaseModel(SafeDeleteModel, UpdateMixin):
    """
    An abstract base class model that provides
    self-updating ``created`` and ``modified`` fields.
    """

    def make_id(self):
        return '{}_{}'.format(self.ID_PREFIX, generate_token(12))

    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.CharField(max_length=16, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)
    metadata = JSONField(blank=True, null=True, max_length=360)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.make_id()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name),
                       args=[self.id])

    class Meta:
        abstract = True  # Set this model as Abstract

    def hard_delete(self):
        self.delete(force_policy=HARD_DELETE)


# from django.contrib.gis.admin import GeoModelAdmin
class BaseModelAdmin(SafeDeleteAdmin):

    exclude = ('metadata',)
    _list_display = (highlight_deleted,) + SafeDeleteAdmin.list_display
    _list_filter = SafeDeleteAdmin.list_filter
    actions = ('hard_delete',) + SafeDeleteAdmin.actions

    def hard_delete(self, request, queryset):
        self.message_user(request, "{} successfully deleted".format(queryset.count()))
        return queryset.delete(force_policy=HARD_DELETE)

    hard_delete.short_description = "HARD Delete selected items"

    def get_list_display(self, request):
        return tuple(self.list_display) + self._list_display

    def get_list_filter(self, request):
        return tuple(self.list_filter) + self._list_filter
