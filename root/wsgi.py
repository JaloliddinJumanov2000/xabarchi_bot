import os
import sys

# Loyihangiz joylashgan katalogni sys.path ga qo‘shish
path = '/home/Jaloliddin/xabarchi_bot'
if path not in sys.path:
    sys.path.append(path)

# Django settings modulini ko‘rsatish
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'

# Django WSGI application yaratish
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
