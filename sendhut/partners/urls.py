from django.conf.urls import url

from .views import PartnerApplication


urlpatterns = [
    url(r'^$', PartnerApplication.as_view(), name='apply'),
]
