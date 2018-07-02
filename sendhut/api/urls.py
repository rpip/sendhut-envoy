from django.conf.urls import url, include
from rest_framework import routers
# from rest_framework.schemas import get_schema_view

from . import views

# schema_view = get_schema_view(title='Sendhut API')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'addresses', views.AddressViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^quotes/$', views.DeliveryQuote.as_view()),
    # url(r'^api-token/$', views.AuthToken.as_view()),
    # url(r'^schema/$', schema_view),
    # url(r'^auth-token/$', include(
    #     'rest_framework.urls', namespace='rest_framework')),
]
