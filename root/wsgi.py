import os
import sys

path = '/home/jaloliddin/xabarchi_bot'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xabarchi_bot.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
