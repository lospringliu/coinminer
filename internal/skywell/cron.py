#!/usr/bin/python

import os,sys, time, random, threading
sys.path.append('/home/pi/web/skywell')
os.environ["DJANGO_SETTINGS_MODULE"] = "skywell.settings"
from common.models import *
for jw in JintianWorker.objects.filter(is_expired=False).exclude(ipaddress__startswith='192.168'):
#for jw in JintianWorker.objects.filter(is_expired=False).filter(ipaddress__startswith='192.168'):
	print("updating miner %s" % str(jw))
	jw.update()
