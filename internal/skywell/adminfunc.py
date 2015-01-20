from django.contrib.auth.models import User, Permission, Group
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import re
from common.functions import *
from common.models import *
from userprofiles.models import *
import subprocess
from requests import get
from django.db.models import Avg, Max, Q
from decimal import Decimal
import random

def clean_username(username):
	"""
	Performs any cleaning on the "username" prior to using it to get or
	create the user object.  Returns the cleaned username.

	By default, returns the username unchanged.
	"""
	username = username.strip().lower()
	if re.match(r'.*@.*',username):
		username = username.split('@')[0]
	return username

def cleanreportbyjingtianworker(tdelta=5):
	res = dict()
	reportdate = datetime.date.today() - datetime.timedelta(tdelta)
	reporttime = datetime.datetime.now() - datetime.timedelta(tdelta)	
	for worker in JintianWorker.objects.all():
		res[worker] =  ReportByJingTianWorker.objects.filter(worker=worker).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)).aggregate(Avg('hr_5'))
		if res[worker]['hr_5__avg']:
			print('starts cleaning worker report %s' % worker.ipaddress)
			for rp in ReportByJingTianWorker.objects.filter(worker=worker).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)):
				rp.delete()
			rp = ReportByJingTianWorker(reportdate=reportdate,reporttime=reporttime,worker=worker,hr_5=int(float(res[worker]['hr_5__avg'])))
			rp.save()

def cleanreportbyworker(tdelta=2):
	res = dict()
	reportdate = datetime.date.today() - datetime.timedelta(tdelta)
	reporttime = datetime.datetime.now() - datetime.timedelta(tdelta)	
	for worker in MinerWorker.objects.all():
		res[worker] =  ReportByWorker.objects.filter(worker=worker).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)).aggregate(Avg('hr_120'),Avg('hr_300'),Avg('hr_225'))
		if res[worker]['hr_120__avg'] and res[worker]['hr_300__avg'] and res[worker]['hr_225__avg']:
			print('starts cleaning worker report')
			ReportByWorker.objects.filter(worker=worker).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)).delete()
			rp = ReportByWorker(reportdate=reportdate,reporttime=reporttime,worker=worker,hr_225=int(float(res[worker]['hr_225__avg'])),hr_300=int(float(res[worker]['hr_300__avg'])),hr_120=int(float(res[worker]['hr_120__avg'])))
			rp.save()

def cleanreportbypool(tdelta=4):
	res = dict()
	reportdate = datetime.date.today() - datetime.timedelta(tdelta)
	reporttime = datetime.datetime.now() - datetime.timedelta(tdelta)	
	for pool in MinerFactory.objects.all():
		res[pool] =  ReportByFactory.objects.filter(factory=pool).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)).aggregate(Avg('hr_128'),Avg('hr_256'),Avg('hr_225'),Max('coins'),Max('blocks'))
		if res[pool]['hr_128__avg'] and res[pool]['hr_256__avg'] and res[pool]['hr_225__avg'] and res[pool]['coins__max'] and res[pool]['blocks__max']:
			print('starts cleaning pool report')
			ReportByFactory.objects.filter(factory=pool).filter(reportdate=datetime.date.today()-datetime.timedelta(tdelta)).delete()
			rp = ReportByFactory(reportdate=reportdate,reporttime=reporttime,factory=pool,hr_225=int(float(res[pool]['hr_225__avg'])),hr_256=int(float(res[pool]['hr_256__avg'])),hr_128=int(float(res[pool]['hr_128__avg'])),coins=res[pool]['coins__max'],blocks=res[pool]['blocks__max'])
			rp.save()

def cleanreport():
	cleanreportbyworker()
	cleanreportbypool()
	cleanreportbyjingtianworker()

def updatereportbyjtworker():
	dtnow = datetime.datetime.now()
	for worker in JintianWorker.objects.all():
		report = ReportByJingTianWorker(worker=worker,reporttime=dtnow)
		report.hr_5 = worker.hr_5
		report.save()
	report = ReportByJingtianFactory(reporttime=dtnow)
	report.numworkers = JintianWorker.objects.exclude(is_expired=True).count()
	report.hr_5 = int(ReportByJingTianWorker.objects.filter(reporttime=dtnow).aggregate(Sum('hr_5'))['hr_5__sum'] / 1024.0 + 0.4)
	report.save()

def updatereportbyworker():
	dtnow = datetime.datetime.now()
	for worker in MinerWorker.objects.all():
		report = ReportByWorker(worker=worker,reporttime=dtnow)
		report.hr_225 = worker.hr_225
		report.hr_300 = worker.hr_300
		report.hr_120 = worker.hr_120
		report.save()

def updatereportbypool():
	dtnow = datetime.datetime.now()
	for pool in MinerFactory.objects.all():
		report = ReportByFactory(factory=pool,reporttime=dtnow)
		report.blocks = pool.blocks
		report.coins = pool.coins
		report.coinspending = pool.coinspending
		report.hr_128 = pool.hr_128
		report.hr_256 = pool.hr_256
		report.hr_225 = pool.hr_225
		report.hr_300 = pool.hr_300
		report.hr_120 = pool.hr_120
		report.save()

def update_pool():
	for pool in MinerFactory.objects.all():
		pool.get_blocks()
		pool.get_pay()

def update_jtworker(worker=None):
	if not worker:
		for worker in JintianWorker.objects.exclude(is_expired=True):
			worker.update()
	else:
		worker.update()

def update_worker(pool=None):
	if not pool:
		for pool in MinerFactory.objects.all():
			update_worker(pool=pool)
#			return update_worker(pool=pool)
	else:
		hurl = pool.website + pool.link
		html = get(hurl)
		active_worker_set = set()
		if not html.status_code == 200:
			return
		lines = re.compile(r'^<TR class=.userstats.*TR>$',re.M).findall(html.text)
		workername = 'default'
		for line in lines:
			valuematch = re.match(r".*12 Hours</I></TD><TD>(?P<twelveh>.*)/s</TD><TD>.*class=.userstats.*3 Hours</I></TD><TD>(?P<threeh>.*)/s</TD><TD>.*userstats.*22.5 Minutes</I></TD><TD>(?P<twotwofive>.*)/s</TD>.*<b>(?P<worker>.*)</b>.*",line)
			if valuematch:
				valuedict = valuematch.groupdict()
				if workername:
					worker,created = MinerWorker.objects.get_or_create(name=workername,factory=pool)
					active_worker_set.add(worker)
					workername = valuedict['worker']
					valuedict.pop('worker')
					for k in valuedict.keys():
						rer = re.match('(.*) Gh',valuedict[k]) 
						if rer:
							values = rer.groups()[0]
						elif re.match('(.*) Th',valuedict[k]):
							values = re.match('(.*) Th',valuedict[k]).groups()[0]
							try:
								values = str(float(values) * 1000)
							except ValueError:
								values = '1.0'
						else:
							values = '1.0'
						try:
							valuedict[k] = int(float(re.sub(r',','',values)))
						except ValueError:
							valuedict[k] = 1
							
					hr_300 = valuedict['threeh']
					hr_120 = valuedict['twelveh']
					hr_225 = valuedict['twotwofive']
					worker.hr_120 = hr_120
					worker.hr_225 = hr_225
					worker.hr_300 = hr_300
					worker.is_expired = False
					worker.save()
		for worker in MinerWorker.objects.all():
			if not worker in active_worker_set:
				worker.is_expired = True
				worker.hr_120 = 0
				worker.hr_225 = 0
				worker.hr_300 = 0
				worker.save()

#					print(worker.name, worker.hr_225, worker.hr_300, worker.hr_120)
#		return lines

def load_qq_group(file=None,group=None):
	if file:
		if group:
			origuserset = set()
			newuserset = set()
			for user in group.user_set.all():
				origuserset.add(user)
			for line in file:
				nickname_qqnumber = line.strip().split('(')
				nickname = nickname_qqnumber[0].strip()
				qqnumber = re.sub(r'\)','',nickname_qqnumber[1].strip())
				user,created = User.objects.get_or_create(username=qqnumber)
				if created:
					print("created ... " + qqnumber + "\t" + nickname)
					user.is_active = False
					user.is_staff = True
					user.save()
				if not user.email:
					user.email = qqnumber + "@qq.com"
					user.save()
				newuserset.add(user)
				group.user_set.add(user)
				try:
					userprofile = UserProfile.objects.get(user=user)
				except UserProfile.DoesNotExist:
					userprofile = UserProfile(user=user)
					userprofile.minerid = random.random() * 100000 + 102000
					userprofile.qqdisplay = nickname
					userprofile.save()
			file.close()
			return [origuserset, newuserset]
		else:
			for line in file:
				nickname_qqnumber = line.strip().split('(')
				minerid = line.strip().split('-')[0]
				qqnumber = re.sub(r'\)','',nickname_qqnumber[1].strip())
				print("updating ... " + qqnumber + "\t" + minerid)
				try:
					minerid = int(minerid)
					userprofile = UserProfile.objects.get(user__username=qqnumber)
					userprofile.minerid = minerid
					userprofile.save()
				except ValueError:
					print("\tunable to update ... " + qqnumber + "\t" + minerid)
			file.close()
					

def load_qq_group_result(file=None,group=None,less=False,more=False,qqnum_ini=1):
	if file and group:
		if less:
			for line in file:
				values = line.strip().split('\t')
				fullname = values[0]
				sha256_first = Decimal(str(values[2]))
				sha256_second = Decimal(str(values[3]))
				nickname = fullname
				payname = fullname
				qqnumber = "client%02g" %  qqnum_ini
				qqnum_ini += 1
				print("generating ... " + qqnumber + "\t" + nickname)
				user,created = User.objects.get_or_create(username=qqnumber)
				if created:
					user.is_active = False
					user.is_staff = True
					user.save()
				if not user.email:
					user.email = qqnumber + "@qq.com"
					user.save()
				group.user_set.add(user)
				userprofile,created = UserProfile.objects.get_or_create(user=user)
				if created:
					userprofile.minerid = random.random() * 100000 + 102000
					userprofile.qqdisplay = nickname
					userprofile.fullname = fullname
					userprofile.payname = payname
					userprofile.sha256_first = sha256_first
					userprofile.sha256_second = sha256_second
					userprofile.save()
		elif more:
			for line in file:
				values = line.strip().split('\t')
				fullname = values[0]
				sha256_first = Decimal(values[2])
				sha256_second = Decimal(values[3])
				nickname = values[1]
				payname = fullname
				qqnumber = "client%02g" %  qqnum_ini
				qqnum_ini += 1
				print("generating ... " + qqnumber + "\t" + nickname)
				user,created = User.objects.get_or_create(username=qqnumber)
				if created:
					user.is_active = False
					user.is_staff = True
					user.save()
				if not user.email:
					user.email = qqnumber + "@qq.com"
					user.save()
				group.user_set.add(user)
				userprofile,created = UserProfile.objects.get_or_create(user=user)
				if created:
					userprofile.minerid = random.random() * 100000 + 102000
					userprofile.qqdisplay = nickname
					userprofile.fullname = fullname
					userprofile.payname = payname
					userprofile.sha256_first = sha256_first
					userprofile.sha256_second = sha256_second
					userprofile.save()
		else:
			pass

def updatereporttest(ipstarts=None):
	if ipstarts:
		for jtworker in JintianWorker.objects.filter(ipaddress__startswith=ipstarts):
			print(str(jtworker))
			jtworker.update()
	else:
		update_jtworker()
def updatereport(ipstarts='180.97.82'):
	update_worker()
	updatereportbyworker()
	update_pool()
	updatereportbypool()
	if ipstarts:
		for jtworker in JintianWorker.objects.filter(ipaddress__startswith=ipstarts):
			pass
#			jtworker.update()
	else:
		update_jtworker()
	updatereportbyjtworker()

def load_records_by_qqdisplay3(type=None,file=None,group=None,fileout=None):
	if file:
		for line in file:
			qqdisplay = line.split('\t')[1]
			quantity = line.split('\t')[2]
			fullname = line.split('\t')[0]
			try:
				print("\t\t" + qqdisplay)
				up = UserProfile.objects.get(qqdisplay=qqdisplay)
#				if group:
#					u = up.user
#					u.groups.add(group)
				if type == 'decimal':
					quantity = Decimal(quantity)
#				else:
#					quantity = int(quantity)
#				print("\t\t" + up.qqdisplay + "  " + str(quantity))
				if up.sha256_second == quantity:
					print('wow')
					up.fullname = fullname
					up.save()
			except UserProfile.DoesNotExist:
#				print(line)
				if fileout:
				  fileout.write(line)
	if fileout:
		fileout.close()
def load_records_by_qqdisplay(type=None,file=None,group=None,fileout=None):
	if file:
		for line in file:
			qqdisplay = line.split()[0]
			quantity = line.split()[1]
			try:
#				print("\t\t" + qqdisplay)
				up = UserProfile.objects.get(qqdisplay=qqdisplay)
				if group:
					u = up.user
					u.groups.add(group)
				if type == 'decimal':
					quantity = Decimal(quantity)
				else:
					quantity = int(quantity)
				print(str(up) + "  " + str(quantity))
				up.sha256_second = quantity
				up.save()
			except UserProfile.DoesNotExist:
#				print(line)
				if fileout:
				  fileout.write(line)

def load_records_by_qqnumber(type=None,file=None,group=None,fileout=None):
	if file:
		for line in file:
			qqnumber = line.strip().split()[0]
			quantity = line.strip().split()[2]
			nickname = line.strip().split()[1]
			try:
				up = UserProfile.objects.get(user__username=qqnumber)
				if group:
					u = up.user
#					u.groups.add(group)
				if type == 'decimal':
					quantity = Decimal(quantity)
				else:
					quantity = int(quantity)
				print("\t" + up.user.username + "\t" + str(up.scrypt_first) + "\t" + str(quantity) + "\t" + up.qqdisplay)
				print("\t" + nickname)
				up.scrypt_first = quantity
#				print(up.scrypt_first)
				up.save()
			except UserProfile.DoesNotExist:
				print(line)
				if fileout:
				  fileout.write(line)

def export_result(file=None):
	if not file:
		for up in UserProfile.objects.filter(user__groups=Group.objects.get(id=3)).filter(Q(sha256_first__gt=Decimal('0.00')) | Q(sha256_second__gt=Decimal('0.0'))).order_by('payname'):
			print(up.user.username.encode('utf-8') + '\t' + up.payname.encode('utf-8') + '\t' + up.qqdisplay.encode('utf-8') + '\t' + str(up.sha256_first.normalize()) + '\t' + str(up.sha256_second.normalize()) + '\t' + str((up.sha256_first + up.sha256_second).normalize()))
	else:
		for up in UserProfile.objects.filter(user__groups=Group.objects.get(id=3)).filter(Q(sha256_first__gt=Decimal('0.00')) | Q(sha256_second__gt=Decimal('0.0'))).order_by('payname'):
#			file.write(up.payname.encode('utf-8') + '\t' + str(up.sha256_first.normalize()) + '\t' + str(up.sha256_second.normalize()) + '\t' + str((up.sha256_first + up.sha256_second).normalize()) + '\n')
			file.write(up.user.username.encode('utf-8') + '\t' + up.payname.encode('utf-8') + '\t' + up.qqdisplay.encode('utf-8') + '\t' + str(up.sha256_first.normalize()) + '\t' + str(up.sha256_second.normalize()) + '\t' + str((up.sha256_first + up.sha256_second).normalize()) + '\n')
		file.flush()
		file.close()
