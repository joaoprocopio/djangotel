import os

from django.core.wsgi import get_wsgi_application

from rastro import observability

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rastro.settings")

observability.instrument()

application = get_wsgi_application()
