from django.conf.urls import url

from . import endpoints

urlpatterns = [
    # url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^auth/$', endpoints.AuthToken.as_view(), name='auth-token'),
    # url(r'^me/$', views.UserDetail.as_view(), name='user_details'),
    # url(r'^users/password-reset/$', views.PasswordResetView.as_view(),
    #     name='password_reset'),
    # url(r'^users/password-change/$', views.PasswordChangeView.as_view(),
    #     name='password_change'),
    # url(r'^users/$', views.UserCreate.as_view(), name='users'),
    # url(r'^quotes/$', views.Quotes.as_view(), name='quotes'),
    # url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
    #     views.Schedules.as_view(), name='schedules')
]
