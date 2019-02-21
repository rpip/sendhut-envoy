from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from .views import (
    HomeView, AboutView, FAQView,
    PrivacyView, TermsView, BusinessView
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about-us/?$', AboutView.as_view(), name='about-us'),
    url(r'^faqs/?$', FAQView.as_view(), name='faqs'),
    url(r'^terms/?$', TermsView.as_view(), name='terms'),
    url(r'^privacy/?$', PrivacyView.as_view(), name='privacy'),
    url(r'^partners/?$', include('sendhut.partners.urls', namespace='partners')),
    url(r'^business/?$', BusinessView.as_view(), name='business'),
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
