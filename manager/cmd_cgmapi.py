#!/usr/bin/python

import socket
import json
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--getwu",action="store_true",help="return work utility formatted as wu=XYZ")
parser.add_option("--gethrav",action="store_true",help="return average hash rate formatted as hr_avg=XYZ")
parser.add_option("--gethr5s",action="store_true",help="return average hash rate formatted as hr_5s=XYZ")
parser.add_option("--hostip",help="specify host IP address",action="store",type="string")
parser.add_option("--command",help="specify cgminer api command",action="store",type="string")
(options,args) = parser.parse_args()


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
#        finally:
#            sock.shutdown(socket.SHUT_RDWR)
#            sock.close()

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

def to_table(retstr=None,ptabs=1):
	print(retstr)
	
if __name__ == "__main__":
	hostip = '127.0.0.1'
	if options.hostip:
		hostip = options.hostip
	cm = CgminerAPI(host=hostip)
	if options.command:
		if options.command == 'stats':
			to_table(cm.stats())
		elif options.command == 'devs':
			to_table(cm.devs())
		else:
			to_table(cm.summary())
	if options.getwu or options.gethrav or options.gethr5s:
		cm_summary = cm.summary()
		hr5s = 0
		hrav = 0
		wu = 0
		if type(cm_summary) == type(dict()):
			if cm_summary.has_key('SUMMARY'):
				if cm_summary['SUMMARY'][0].has_key('MHS av'):
					hrav = int(float(cm_summary['SUMMARY'][0]['MHS av']) / 1024 + 0.4)
				if cm_summary['SUMMARY'][0].has_key('MHS 5s'):
					hr5s = int(float(cm_summary['SUMMARY'][0]['MHS 5s']) / 1024 + 0.4)
				if cm_summary['SUMMARY'][0].has_key('Work Utility'):
					wu = int(cm_summary['SUMMARY'][0]['Work Utility'])
		if options.getwu:
			print("wu=%d" % wu)
		if options.gethrav:
			print("hrav=%d" % hrav)
		if options.gethr5s:
			print("hr5s=%d" % hr5s)

