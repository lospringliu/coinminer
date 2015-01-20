#!/usr/bin/python

from __future__ import generators
import os
import sys
import re
import datetime
from optparse import OptionParser
adminmail='xcliu@ca.ibm.com'
adminmails=['xcliu@ca.ibm.com',]
WWW_PATH = '/home/pi/web'
DJANGOPATH = os.path.join(WWW_PATH,'skywell')
sys.path.append(WWW_PATH)
sys.path.append(DJANGOPATH)
#sys.path.append('/pcc/eng/sa/archives/tftpx/pxelinux.cfg/bin')
os.environ["DJANGO_SETTINGS_MODULE"] = "skywell.settings"
parser = OptionParser()
parser.add_option("-v","--verbose",action="store_true",dest="verbose",help="seeing more info")
parser.add_option("--django",action="store_true",dest="django",help="django related actions")
parser.add_option("--updatebitstamp",action="store_true",dest="updatebitstamp",help="update bitstamp report")
parser.add_option("--test",action="store_true",dest="test",help="django related actions")
parser.add_option("--updateworker",action="store_true",dest="updateworker",help="update worker performance")
parser.add_option("--updatepool",action="store_true",dest="updatepool",help="update pool performance")
parser.add_option("--updatereport",action="store_true",dest="updatereport",help="update report")
parser.add_option("--cleanreport",action="store_true",dest="cleanreport",help="clean report")
parser.add_option("--user", dest="username",help="specify the user name",action="store",type="string")
(options,args) = parser.parse_args()

if __name__ == '__main__':
#	from django.core import management
	if options.verbose:
		print(len(args))
		print(str(options))
	if options.test:
		f = open('/tmp/pydjangotest','w')
		f.write(str(datetime.datetime.now()) + "\n")
		f.close()
	if options.django:
		from django.db import models
		from common.functions import *
		from common.models import *
		from django.contrib.auth.models import *
		from userprofiles.models import UserProfile
		from reports.models import *
		import adminfunc
#		print("performing django related tasks")

		if options.cleanreport:
			adminfunc.cleanreport()
		if options.updatereport:
			adminfunc.updatereport()
		if options.updateworker:
			adminfunc.update_worker()
		if options.updatepool:
			adminfunc.update_pool()
		if options.updatebitstamp:
			bs = BitStamp.objects.all()[0]
			bs.update()
			reportbs = ReportBitStamp(high = bs.high,low = bs.low,ask = bs.ask,bid = bs.bid,volume = bs.volume)
			reportbs.save()
#				user = User.objects.get(username=options.username)
#				ibmid = user.ibmid
#				group = user.groups.all()[0]
#				orgchart = group.orgchart
#				if ibmid.is_manager:
#				# make sure each team member has his account
#					adminfunc.create_team_members(user)
#				# create user's manager and levels up till our of platformlab


