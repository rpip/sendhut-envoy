from django.conf.urls import url, include
from rest_framework import routers
# from rest_framework.schemas import get_schema_view

from . import views

# schema_view = get_schema_view(title='Sendhut API')

# router = routers.DefaultRouter()


urlpatterns = [
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^auth/$', views.AuthToken.as_view()),
    url(r'^me/$', views.UserDetail.as_view(), name='user_details'),
    url(r'^users/password-reset/$', views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^users/password-change/$', views.PasswordChangeView.as_view(),
        name='password_change'),
    url(r'^users/$', views.UserCreate.as_view(), name='users'),
    url(r'^quotes/$', views.Quotes.as_view(), name='quotes'),
    url(r'^schedules(?:/(?P<city>[a-zA-Z]+))?(?:/(?P<type>[a-zA-Z]+))?(?:/(?P<date>[a-zA-Z]+))?/?$',
        views.Schedules.as_view(), name='schedules')
]
