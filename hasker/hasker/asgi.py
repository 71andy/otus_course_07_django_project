"""
ASGI config for hasker project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hasker.settings')

application = get_asgi_application()
