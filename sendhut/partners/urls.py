from django.conf.urls import url

from .views import PartnerApplication, PartnerApplicationSuccess


urlpatterns = [
    url(r'^$', PartnerApplication.as_view(), name='apply'),
    url(r'^feedback$', PartnerApplicationSuccess.as_view(),
        name='application_feedback'),
]
