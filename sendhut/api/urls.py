from django.conf.urls import url

from .endpoints import (
    AuthTokenEndpoint,
    LogoutEndpoint,
    LoginEndpoint,
    ProfileEndpoint,
    SchedulesEndpoint,
    QuotesEndpoint,
    QuotesV1Endpoint,
    DeliveryEndpoint,
    DeliveryDetailEndpoint,
    AddressBookEndpoint,
    ContactDetailEndpoint,
)

urlpatterns = [
    url(r'^auth/logout/?$', LogoutEndpoint.as_view()),
    url(r'^auth/verify?$', AuthTokenEndpoint.as_view()),
    url(r'^auth/login?$', LoginEndpoint.as_view()),
    url(r'^me/?$', ProfileEndpoint.as_view()),
    url(r'^quotes-v1/?$', QuotesV1Endpoint.as_view()),
    url(r'^quotes/?$', QuotesEndpoint.as_view()),
    url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
        SchedulesEndpoint.as_view()),
    url(r'^deliveries/(?P<delivery_id>.+)/?$', DeliveryDetailEndpoint.as_view()),
    url(r'^deliveries/?$', DeliveryEndpoint.as_view()),
    url(r'^contacts/?$', AddressBookEndpoint.as_view()),
    url(r'^contacts/(?P<contact_id>.+)/?$', ContactDetailEndpoint.as_view()),
]
