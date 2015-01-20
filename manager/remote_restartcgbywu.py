import threading
from expectHandler import ExpectHandler
import time, random
import socket
import json

class CgminerAPI(object):
	""" Cgminer RPC API wrapper. """
	def __init__(self, host='localhost', port=4028):
		self.data = {}
		self.host = host
		self.port = port

	def command(self, command, arg=None):
		""" Initialize a socket connection,
		send a command (a json encoded dict) and
		receive the response (and decode it).
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			sock.settimeout(5)
			sock.connect((self.host, self.port))
			payload = {"command": command}
			if arg is not None:
				# Parameter must be converted to basestring (no int)
				payload.update({'parameter': unicode(arg)})

			sock.send(json.dumps(payload))
			received = self._receive(sock)
		except socket.error:
			return "abc"
#		finally:
#			sock.shutdown(socket.SHUT_RDWR)
#			sock.close()

		return json.loads(received[:-1])

	def _receive(self, sock, size=4096):
		msg = ''
		while 1:
			chunk = sock.recv(size)
			if chunk:
				msg += chunk
			else:
				break
		return msg

	def __getattr__(self, attr):
		""" Allow us to make command calling methods.

		>>> cgminer = CgminerAPI()
		>>> cgminer.summary()

		"""
		def out(arg=None):
			return self.command(attr, arg)
		return out

def perform_task(line):
	WUSTAND = 10
	host = line.strip()
	print "start ... %s" % host
	cm = CgminerAPI(host=host)
	cm_summary = cm.summary()
	wu = 0
	if type(cm_summary) == type(dict()):
		if cm_summary.has_key('SUMMARY'):
			if cm_summary['SUMMARY'][0].has_key('Work Utility'):
				wu = int(cm_summary['SUMMARY'][0]['Work Utility'])
	print("\thost %s seems to have a work utility of %d" % (host,wu))
	if wu > 0 and wu < WUSTAND:
		print("\thost %s is being tried to resart..." % host)
#	time.sleep(int(random.random() * 10))
#	print "stop ... %s" % host
		myHand = ExpectHandler(host)
		myHand.copyhome("restartminer",)
#		myHand.run(["sudo ./restartminer &","sleep 5" ])
#	myHand.run(["cd src/cgminer",])

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
