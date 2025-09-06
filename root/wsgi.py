import os
import sys

# Django loyihangiz papkasini sys.path ga qo‘shish
path = '/home/jaloliddin/xabarchi_bot'   # loyihangiz joylashgan to‘liq yo‘l
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xabarchi_bot.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
