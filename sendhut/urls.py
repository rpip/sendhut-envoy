from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from .views import home, about, faqs, privacy, terms


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about-us/$', about, name='about-us'),
    url(r'^faqs/$', faqs, name='faqs'),
    url(r'^terms/$', terms, name='terms'),
    url(r'^privacy/$', privacy, name='privacy'),
    url(r'^partners/', include('sendhut.partners.urls', namespace='partners')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^api/', include('sendhut.api.urls')),
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
