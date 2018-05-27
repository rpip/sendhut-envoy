from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from sendhut.accounts.views import LoginView, LogoutView, SignupView

from .views import home, about, faqs, privacy, terms


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about-us/$', about, name='about-us'),
    url(r'^faqs/$', faqs, name='faqs'),
    url(r'^terms/$', terms, name='terms'),
    url(r'^privacy/$', privacy, name='privacy'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='signin'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('sendhut.accounts.urls', namespace='accounts')),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('loginas.urls'))
]

# Change admin site title
admin.site.site_header = "Sendhut"
admin.site.site_title = "Sendhut Admin"


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]
