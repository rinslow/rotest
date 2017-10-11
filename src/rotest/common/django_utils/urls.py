"""Django definitions for the administrator site urls."""
# pylint: disable=no-name-in-module
import django
from django.contrib import admin
from django.conf.urls import include, url


admin.autodiscover()

urls = [url(r'^admin/', include(admin.site.urls))]

if "1.7" <= django.get_version() < "1.8":
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urls)
else:
    urlpatterns = urls
