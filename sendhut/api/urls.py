from django.conf.urls import url, include
from rest_framework import routers
# from rest_framework.schemas import get_schema_view

from . import views

# schema_view = get_schema_view(title='Sendhut API')

# router = routers.DefaultRouter()


urlpatterns = [
    url(r'^auth/$', views.AuthToken.as_view()),
    url(r'^me/$', views.UserDetail.as_view(), name='user_details'),
    url(r'^quotes/$', views.Quotes.as_view(), name='quotes'),
    url(r'^users/$', views.UserCreate.as_view(), name='users'),
    # url(r'^schema/$', schema_view),
    # url(r'^auth-token/$', include(
    #     'rest_framework.urls', namespace='rest_framework')),
]
