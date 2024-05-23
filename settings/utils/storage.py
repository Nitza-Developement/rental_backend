from django.conf import settings
from decouple import config
from django.core.files.storage import FileSystemStorage

from settings.utils.url_signer import sign_url


class SignedUrlsStorage(FileSystemStorage):
    def __init__(self, hours=1, location=None, base_url=None, *args, **kwargs):
        self.hours = hours
        super().__init__(
            location=location or settings.MEDIA_SIGNED_ROOT,
            base_url=base_url or settings.MEDIA_SIGNED_URL,
            *args,
            **kwargs
        )

    def url(self, name):
        return self.get_signed_url(name)

    def get_signed_url(self, name: str, hours: float = None) -> str:
        url = super().url(name)
        return sign_url(url, hours=hours or self.hours)
