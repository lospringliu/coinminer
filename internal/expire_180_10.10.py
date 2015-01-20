#!/usr/bin/python

import os,sys
sys.path.append('/home/pi/web/skywell')
os.environ["DJANGO_SETTINGS_MODULE"] = "skywell.settings"
from common.models import *
for jw in JintianWorker.objects.filter(ipaddress__startswith='180'):
  jw.is_expired = True
  jw.save()
  print(str(jw))
for jw in JintianWorker.objects.filter(ipaddress__startswith='10.10'):
  jw.is_expired = True
  jw.save()
  print(str(jw))
