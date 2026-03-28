import os

from django.core.wsgi import get_wsgi_application

from djangotel import telemetry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangotel.settings")

telemetry.setup()

application = get_wsgi_application()
