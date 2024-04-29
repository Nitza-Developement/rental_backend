import re
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from settings.utils.url_signer import ServeSignedUrlsStorageLocalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rental.urls')),
    re_path(r'^%s(?P<path>.*)$' % re.escape(
        settings.MEDIA_SIGNED_URL.lstrip('/')
    ), ServeSignedUrlsStorageLocalView.as_view()),
]
