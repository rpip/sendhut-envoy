from django.conf.urls import url

from .endpoints import (
    AuthTokenEndpoint,
    ProfileEndpoint,
    RegistrationEndpoint,
    SchedulesEndpoint,
    QuotesEndpoint
)

urlpatterns = [
    # url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^auth/$', AuthTokenEndpoint.as_view(), name='auth-token'),
    url(r'^me/?$', ProfileEndpoint.as_view(), name='profile'),
    # url(r'^users/password-reset/$', views.PasswordResetView.as_view(),
    #     name='password_reset'),
    # url(r'^users/password-change/$', views.PasswordChangeView.as_view(),
    #     name='password_change'),
    url(r'^users/$', RegistrationEndpoint.as_view(), name='users'),
    url(r'^quotes/?$', QuotesEndpoint.as_view(), name='quotes'),
    url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
        SchedulesEndpoint.as_view(), name='schedules')
]
