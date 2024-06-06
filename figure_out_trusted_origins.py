<<EOF
from django.conf import settings
from urllib.parse import urlparse

print([urlparse(origin).netloc.lstrip("*") for origin in settings.CSRF_TRUSTED_ORIGINS])
print({origin for origin in settings.CSRF_TRUSTED_ORIGINS if "*" not in origin})
EOF