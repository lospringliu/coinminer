import threading
from expectHandler import ExpectHandler
import os, time, random

def perform_task(line):
	host = line.strip()
	print "start ... %s" % host
#	time.sleep(int(random.random() * 10))
#	print "stop ... %s" % host
	myHand = ExpectHandler(host)
#	myHand.run(["cd src/cgminer",])
	myHand.copyhome("restartminer",)
	myHand.run(["sudo ./restartminer &", ])

if __name__ == "__main__":
	import sys, os
	if len(sys.argv) < 2:
		print "Usage: performTask.py ipstarts"
		sys.exit()
	if len(sys.argv) > 2:
		threadpool = int(sys.argv[2])
	else:
		threadpool = 20
	sys.path.append('/export/app/skywell')
	os.environ["DJANGO_SETTINGS_MODULE"] = "skywell.settings"
	from common.models import JintianWorker
	thread_list = []
	for jw in JintianWorker.objects.filter(ipaddress__startswith=sys.argv[1]).filter(is_expired=False).filter(hr_5=0):
		line = jw.ipaddress
		if line:
			t = threading.Thread(name=line,target=perform_task, args=(line,))
			thread_list.append(t)
	for th in thread_list:
		while threading.active_count() > threadpool:
			time.sleep(1)
		th.start()
		print("active threads in queue: %g" % (threading.active_count() - 1))
	while threading.active_count() != 1:
		print("%s threads left to run" % (threading.active_count() - 1))
#		for th in threading.enumerate():
#			print("%s %s" % (th.name,th.ident))
		time.sleep(5)


	print "Total change: %i" % len(thread_list)
