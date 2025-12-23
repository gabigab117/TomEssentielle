from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.apps import apps
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from . import settings
from .views import Accueil


urlpatterns = [
    path('', Accueil.as_view(), name='accueil'),
    path('utilisateur/',include('utilisateur.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('django-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("",include(apps.get_app_config("oscar").urls[0])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
