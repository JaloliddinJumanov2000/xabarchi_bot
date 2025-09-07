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

# Virtualenv yo‘lini sozlash
activate_this = '/home/Jaloliddin/.virtualenvs/myvirtualenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))