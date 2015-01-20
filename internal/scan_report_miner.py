#!/usr/bin/python

import os,sys
import re,subprocess
import  time, random, threading
if len(sys.argv) < 2:
	print "Usage: %s network_cidr" % sys.argv[0]
	sys.exit()
if not os.path.exists('/usr/bin/fping'):
	print('this utility utilizes fping, install it first')
	print('on debian, run apt-get update; apt-get install fping')
	sys.exit()
if not os.path.exists('/home/pi/web/skywell/common'):
	print('this utility needs to run on the same web server and web server should be /home/pi/web/skywell')
	sys.exit()
print("\tscanning for the live miners ...")
live_hosts = subprocess.check_output(['/bin/bash','-c',"/usr/bin/fping -a -A -g %s 2>/dev/null; exit 0" % sys.argv[1]]).strip()
print("\tretrieving the macaddresses for the live miners")
arps =  subprocess.check_output(['/bin/bash','-c',"/usr/bin/fping -a -A %s > /dev/null; arp -n ; exit 0" % re.sub(r'\n',' ',live_hosts)]).strip()
print("")
print("now let's update the information into our database")
numcounter = 0
sys.path.append('/home/pi/web/skywell')
os.environ["DJANGO_SETTINGS_MODULE"] = "skywell.settings"
from common.models import *
walletother,created = Wallet.objects.get_or_create(name='other',cointype=CoinType.objects.get(name='litecoin'))
poolunknown,created = MinerFactory.objects.get_or_create(name='unknown',cointype=CoinType.objects.get(name='litecoin'))
for line in arps.split('\n'):
	if re.match(r'.*b8:27:eb',line):
		numcounter += 1
		parts = line.split()
		ipaddress = parts[0]
		macaddress = parts[2]
		if len(macaddress) == 17:
			try:
				miner = JintianWorker.objects.get(macaddress =  macaddress)
				if miner.is_expired:
					miner.is_expired = False
				if miner.ipaddress != ipaddress:
					miner.ipaddress = ipaddress
				miner.save()
				print("... updated ... %s" % str(miner))
			except JintianWorker.MultipleObjectsReturned:
				miner = JintianWorker.objects.filter(macaddress =  macaddress)[0]
				if miner.is_expired:
					miner.is_expired = False
				if miner.ipaddress != ipaddress:
					miner.ipaddress = ipaddress
				miner.save()
				print("... updated ... %s" % str(miner))
			except JintianWorker.DoesNotExist:
				try:
					miner = JintianWorker.objects.get(ipaddress =  ipaddress)
					if miner.is_expired:
						miner.is_expired = False
					if miner.macaddress != macaddress:
						miner.macaddress = macaddress
					miner.save()
					print("... updated ... %s" % str(miner))
				except JintianWorker.MultipleObjectsReturned:
					miner = JintianWorker.objects.filter(ipaddress =  ipaddress)[0]
					if miner.is_expired:
						miner.is_expired = False
					if miner.macaddress != macaddress:
						miner.macaddress = macaddress
					miner.save()
				except JintianWorker.DoesNotExist:
					miner, created = JintianWorker.objects.get_or_create(ipaddress=ipaddress,factory=poolunknown,macaddress=macaddress,name=ipaddress,wallet=walletother)
					print("... created ... %s" % str(miner))
print("total %g miners found and updated or created" % numcounter)
#for jw in JintianWorker.objects.filter(is_expired=False).exclude(ipaddress__startswith='192.168'):
#	print("updating miner %s" % str(jw))
#	jw.update()
