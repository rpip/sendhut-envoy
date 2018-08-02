from django.conf.urls import url

from .endpoints import (
    AuthTokenEndpoint,
    LogoutEndpoint,
    ProfileEndpoint,
    RegistrationEndpoint,
    SchedulesEndpoint,
    QuotesEndpoint,
    PasswordResetEndpoint,
    PasswordChangeEndpoint,
    DeliveryEndpoint,
    DeliveryDetailEndpoint
)

urlpatterns = [
    url(r'^auth/logout/?$', LogoutEndpoint.as_view(), name='logout'),
    url(r'^auth/reset-password/?$', PasswordResetEndpoint.as_view(),
        name='password_reset'),
    url(r'^auth/change-password/?$', PasswordChangeEndpoint.as_view(),
        name='password_change'),
    url(r'^auth/?$', AuthTokenEndpoint.as_view(), name='auth-token'),
    url(r'^me/?$', ProfileEndpoint.as_view(), name='profile'),
    url(r'^users/?$', RegistrationEndpoint.as_view(), name='users'),
    url(r'^quotes/?$', QuotesEndpoint.as_view(), name='quotes'),
    url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
        SchedulesEndpoint.as_view(), name='schedules'),
    url(r'^deliveries/(?P<delivery_id>.+)/?$', DeliveryDetailEndpoint.as_view(),
        name='delivery_detail'),
    url(r'^deliveries/?$', DeliveryEndpoint.as_view(), name='delivery')
]
