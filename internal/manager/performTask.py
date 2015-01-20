import threading
from expectHandler import ExpectHandler
import time, random

def perform_task(line):
	host = line.strip()
	print "start ... %s" % host
	myHand = ExpectHandler(host)
	myHand.copyhome("mycommand",)
	myHand.run([ "sudo ./mycommand &", "sleep 15" ])

if __name__ == "__main__":
	import sys, os
	if len(sys.argv) < 2:
		print "Usage: performTask.py <host_file_name>"
		sys.exit()
	file_name = sys.argv[1]
	if not os.path.exists(file_name):
		print "File %s not exist." % file_name
		sys.exit()
	if len(sys.argv) > 2:
		threadpool = int(sys.argv[2])
	else:
		threadpool = 10
	with open(file_name) as input:
		thread_list = []
		for line in input.readlines():
			line = line.strip()
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
