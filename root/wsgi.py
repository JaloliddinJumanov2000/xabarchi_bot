import os
import sys

# Virtualenv yo‘li (agar virtualenv ishlatayotgan bo‘lsangiz)
# Masalan, agar virtualenv /home/Jaloliddin/.virtualenvs/xabarchi_bot bo‘lsa:
virtualenv_path = '/home/Jaloliddin/.virtualenvs/xabarchi_bot'
activate_this = os.path.join(virtualenv_path, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

# Loyihangiz katalogini sys.path ga qo‘shish
project_path = '/home/Jaloliddin/xabarchi_bot'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Django settings modulini ko‘rsatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

# Django WSGI application yaratish
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
