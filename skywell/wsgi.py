import os
import sys
sys.path.insert(0,'/export/app/skywell')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skywell.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
