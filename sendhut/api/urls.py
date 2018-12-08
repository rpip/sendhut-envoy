from django.conf.urls import url

from .endpoints import (
    AuthTokenEndpoint,
    LogoutEndpoint,
    ProfileEndpoint,
    RegistrationEndpoint,
    SchedulesEndpoint,
    QuotesEndpoint,
    QuotesV1Endpoint,
    PasswordResetEndpoint,
    PasswordChangeEndpoint,
    DeliveryEndpoint,
    DeliveryDetailEndpoint
)

urlpatterns = [
    url(r'^auth/logout/?$', LogoutEndpoint.as_view()),
    url(r'^auth/reset-password/?$', PasswordResetEndpoint.as_view()),
    url(r'^auth/change-password/?$', PasswordChangeEndpoint.as_view()),
    url(r'^auth/?$', AuthTokenEndpoint.as_view()),
    url(r'^me/?$', ProfileEndpoint.as_view()),
    url(r'^users/?$', RegistrationEndpoint.as_view()),
    url(r'^quotes-v1/?$', QuotesV1Endpoint.as_view()),
    url(r'^quotes/?$', QuotesEndpoint.as_view()),
    url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
        SchedulesEndpoint.as_view()),
    url(r'^deliveries/(?P<delivery_id>.+)/?$', DeliveryDetailEndpoint.as_view()),
    url(r'^deliveries/?$', DeliveryEndpoint.as_view())
]
