"""
WSGI config for service_runner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
from service_runner.manage import prepare
import os

from django.core.wsgi import get_wsgi_application

prepare()

application = get_wsgi_application()
