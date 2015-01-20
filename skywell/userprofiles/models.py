# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
#from mptt.models import  MPTTModel, TreeForeignKey
from django.core.validators import *
from django.db.models.signals import pre_save

##for user functions
from common.functions import *
from common.models import *
from reports.models import *
from decimal import Decimal
from django.db.models import Max, Sum, Avg, Q


@python_2_unicode_compatible
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	minerid =  models.IntegerField("矿工号",default=10000,validators=[MaxValueValidator(339),MinValueValidator(1)])
#	firstname = models.CharField(_('firstname'),max_length=16)
#	lastname = models.CharField(_('lastname'),max_length=16)
	qqdisplay = models.CharField("QQ昵称",max_length=32)
	fullname = models.CharField("姓名",max_length=24,null=True,blank=True,default=None)
	payname = models.CharField("帐本姓名",max_length=24,null=True,blank=True,default=None)
	idtype = models.ForeignKey(IdType,verbose_name="身份证明类型",default=1)
	idnumber = models.CharField("身份证明号码",max_length=18,blank=True,null=True,default=None)
	phone = models.CharField("电话",max_length=32,default='xxxxxxxxxxx')
	subscription = models.ForeignKey(Subscription,verbose_name="周报订阅",null=True,blank=True)
	coinfund = models.IntegerField('拟转投虚拟币基金(万元)',default=0,validators=[MaxValueValidator(200),MinValueValidator(0)])
	coinfundact = models.IntegerField('A股实际转投虚拟币基金(元)',default=0,validators=[MaxValueValidator(2000000),MinValueValidator(0)])
	hitechfund = models.IntegerField('拟转投高科技基金(万元)',default=0,validators=[MaxValueValidator(200),MinValueValidator(0)])
	hitechfundact = models.IntegerField('A股实际转投高科技基金(元)',default=0,validators=[MaxValueValidator(2000000),MinValueValidator(0)])
	astockfund = models.IntegerField('曾持有A股基金(元)',default=0,validators=[MaxValueValidator(20000000),MinValueValidator(100000)],editable=False)
	astockvalue = models.IntegerField('A股返资',default=0,editable=False)
	astockcredit = models.IntegerField('A股补偿',default=0,editable=False)
	wellcoin = models.IntegerField('拟转投井通(万元)',default=0,validators=[MaxValueValidator(200),MinValueValidator(0)])
	wellcoinact = models.IntegerField('A股实际转投井通(元)',default=0,validators=[MaxValueValidator(2000000),MinValueValidator(0)])
	wellcoin_self = models.IntegerField('内购井通已打款(元),用1000的整数倍',default=0,validators=[MaxValueValidator(2000000),MinValueValidator(0)])
	wellcoin_total = models.IntegerField('井通数量',default=0,validators=[MinValueValidator(0)])
	bitwell = models.DecimalField("矿工比特币买井通(个) - 转到钱包后填表发给一块涟绮",  max_digits=11,decimal_places=8,default=Decimal('0.00000000'))
	sha256_first = models.DecimalField("比特一期",  max_digits=5,decimal_places=2,default=Decimal('0.00'))
	lock_sha256_first = models.NullBooleanField("确认比特一期正确",default=None)
	sha256_second = models.DecimalField("比特二期",max_digits=5,decimal_places=2,default=Decimal('0.00'))
	lock_sha256_second = models.NullBooleanField("确认比特二期正确",default=None)
	sha256_third = models.IntegerField("比特三期",default=0,validators=[MaxValueValidator(5000), MinValueValidator(0)])
	sha256_third_self = models.IntegerField("比特矿机第三期已打款(元),由张海林确认",default=0,validators=[MaxValueValidator(500000), MinValueValidator(0)])
	lock_sha256_third = models.NullBooleanField("比特三期已付款",default=None)
	scrypt_first = models.IntegerField("莱特一期预订",default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
	lock_scrypt_first = models.NullBooleanField("确认莱特已付款",default=None)
	location = models.ForeignKey(Location,verbose_name="所在城市",null=True,blank=True)
	btcwallet = models.CharField(_('bitcoin wallet'),max_length=34,null=True,blank=True)
	ltcwallet = models.CharField(_('litecoin wallet'),max_length=34,null=True,blank=True)
	swcwallet = models.CharField(_('井通钱包地址'),max_length=34,default='',validators=[RegexValidator(regex=r'^j[a-z0-9A-Z]{32,33}$',message="请输入正确的钱包地址")])
	swcwalletprocessed = models.BooleanField(_('已冲值'),default=False,)
	confirmed = models.BooleanField(_('confirmed'),default=False,editable=False)
	vote = models.NullBooleanField(_('agree|disagree'),blank=True,null=True,default=None,editable=False)
	note = models.CharField("注释",max_length=32,null=True,blank=True,default=None)
	notewell = models.TextField("注释",blank=True,null=True,default='')
	changenote = models.CharField("更新原因",max_length=64,default='',)
	btctominer = models.IntegerField('比特币换矿机(台)',default=0)

	class Meta:
		verbose_name = _('userprofile')
		verbose_name_plural = _('userprofiles')
		ordering = [ 'user', ]
	def __str__(self):
		return self.user.username

	def get_banzhu_list(self):
		return Group.objects.get(id=6).user_set.all()

	def user_in_astockfund_group(self):
		gasharefund = Group.objects.get(id=11)
		return gasharefund in self.user.groups.all()

	def user_in_pool_admin_group(self):
		gminerpool = Group.objects.get(id=10)
		return gminerpool in self.user.groups.all()

	def user_in_miner_group(self):
		gminer = Group.objects.get(id=3)
		return gminer in self.user.groups.all()

	def need_confirm_btcpurchase(self):
#		return self.sha256_first + self.sha256_second > Decimal('0.0')
		return self.user_in_miner_group()

	def need_confirm_btcfirst(self):
		return self.need_confirm_btcpurchase() and self.lock_sha256_first == None

	def need_confirm_btcsecond(self):
		return self.need_confirm_btcpurchase() and self.lock_sha256_second == None

	def get_queryset_sha256_first(self):
		return UserProfile.objects.filter(sha256_first__gt=Decimal('0.0')).order_by('-sha256_first')
	
	def get_queryset_sha256_second(self):
		return UserProfile.objects.filter(sha256_second__gt=Decimal('0.0')).order_by('-sha256_second')

	def get_queryset_astockfund(self):
		return UserProfile.objects.filter(astockfund__gt=2000).order_by('-astockfund')

	def get_sum_queryset_astockfund(self):
		return UserProfile.objects.filter(astockfund__gt=2000).aggregate(Sum('astockfund'),Sum('hitechfund'),Sum('coinfund'),Sum('wellcoin'),Sum('astockcredit'),Sum('astockvalue'),Sum('wellcoinact'),Sum('hitechfundact'),Sum('coinfundact'))

	def get_queryset_sha256_third(self):
		return UserProfile.objects.filter(sha256_third__gt=0).order_by('-sha256_third')

	def get_sum_sha256_third(self):
		return self.get_queryset_sha256_third().aggregate(Sum('sha256_third'))['sha256_third__sum']

	def get_queryset_btctominer(self):
		return UserProfile.objects.filter(btctominer__gt=0)

	def get_sum_btctominer(self):
		return self.get_queryset_btctominer().aggregate(Sum('btctominer'))['btctominer__sum']

	def get_queryset_hitechfund(self):
		return UserProfile.objects.filter(hitechfund__gt=0).order_by('-hitechfund')

	def get_queryset_scrypt_first(self):
		return UserProfile.objects.filter(scrypt_first__gt=0).order_by('-scrypt_first')

	def get_queryset_scrypt_first_miner(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(scrypt_first__gt=0).order_by('-scrypt_first')

	def get_sum_scrypt_first_miner(self):
		return self.get_queryset_scrypt_first_miner().aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def get_sum_scrypt_first_excludeminer(self):
		return self.get_queryset_scrypt_first_excludeminer().aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def get_queryset_scrypt_first_excludeminer(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.exclude(user__groups=gminer).filter(scrypt_first__gt=0).order_by('-scrypt_first')

	def get_queryset_oversea(self):
		return UserProfile.objects.filter(location__province__parent__id__gt=1).order_by('location')

	def get_total_todolist_solved(self):
		from issues.models import TodoList 
		return TodoList.objects.filter(solved=True)

	def get_total_todolist_unsolved(self):
		from issues.models import TodoList 
		return TodoList.objects.filter(solved=False)

	def todolist(self):
		from issues.models import TodoList 
		return TodoList.objects.filter(solved=False)[:20]

	def get_total_logactions(self):
		from issues.models import LogRecord 
		return LogRecord.objects.all()

	def get_logrecords(self):
		from issues.models import LogRecord 
		return LogRecord.objects.all()[:15]

	def users_imported(self):
		return User.objects.all()

	def users_minergrp_imported(self):
		gminer = Group.objects.get(id=3)
		return self.users_imported().filter(groups=gminer).exclude(username__startswith='client')

	def user_in_banzhu_group(self):
		return Group.objects.get(id=6) in self.user.groups.all()

	def user_in_superuser_set(self):
		return self.user.username in superusers_set

	def users_activated(self):
		return User.objects.filter(is_active=True)

	def users_minergrp_activated(self):
		gminer = Group.objects.get(id=3)
		return self.users_activated().filter(groups=gminer)

	def sum_hitechfund(self):
		return UserProfile.objects.all().aggregate(Sum('hitechfund'))['hitechfund__sum']

	def count_hitechfund_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(hitechfund__gt=0).count()

	def sum_hitechfund_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).aggregate(Sum('hitechfund'))['hitechfund__sum']

	def sum_scrypt_first(self):
		return UserProfile.objects.all().aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def count_scrypt_first_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(scrypt_first__gt=0).count()

	def sum_scrypt_first_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def get_queryset_scrypt_first_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(scrypt_first__gt=0)

	def confirmed_sum_scrypt_first(self):
		return UserProfile.objects.filter(lock_scrypt_first=True).aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def confirmed_sum_scrypt_first_minergrp(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(lock_scrypt_first=True).aggregate(Sum('scrypt_first'))['scrypt_first__sum']

	def confirmed_sum_sha256_first(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(lock_sha256_first=True).aggregate(Sum('sha256_first'))['sha256_first__sum']

	def sum_sha256_first(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.exclude(user__username__startswith='client').filter(user__groups=gminer).aggregate(Sum('sha256_first'))['sha256_first__sum']

	def confirmed_sum_sha256_second(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.filter(user__groups=gminer).filter(lock_sha256_second=True).aggregate(Sum('sha256_second'))['sha256_second__sum']

	def sum_sha256_second(self):
		gminer = Group.objects.get(id=3)
		return UserProfile.objects.exclude(user__username__startswith='client').filter(user__groups=gminer).aggregate(Sum('sha256_second'))['sha256_second__sum']

	def sum_coinfund(self):
		return UserProfile.objects.all().aggregate(Sum('coinfund'))['coinfund__sum']

	def max_scrypt_first(self):
		return UserProfile.objects.all().aggregate(Max('scrypt_first'))['scrypt_first__max']

	def max_sha256_first(self):
		return UserProfile.objects.all().aggregate(Max('sha256_first'))['sha256_first__max']

	def max_sha256_second(self):
		return UserProfile.objects.all().aggregate(Max('sha256_second'))['sha256_second__max']

	def max_coinfund(self):
		return UserProfile.objects.all().aggregate(Max('coinfund'))['coinfund__max']

	def sum_blocks_mined(self):
		return MinerFactory.objects.all().aggregate(Sum('blocks'))['blocks__sum']

	def sum_coins_mined(self):
		return MinerFactory.objects.all().aggregate(Sum('blocks'))['blocks__sum'] * 25

	def sum_coins_payed(self):
		return MinerFactory.objects.all().aggregate(Sum('coins'))['coins__sum']

	def sum_coins_pending(self):
		return MinerFactory.objects.all().aggregate(Sum('coinspending'))['coinspending__sum']

	def get_top_ten_devicerejctratio(self):
		return JintianWorker.objects.all().order_by('-device_reject_ratio')[:10]

	def sum_jtworker_wuhr(self):
		return self.sum_jtworker_wu() / 54
	def sum_jtworker_wu(self):
		retnum = JintianWorker.objects.exclude(wu=-1).exclude(is_expired=True).filter(wu__lte=1000).aggregate(Sum('wu'))['wu__sum']
		if JintianWorker.objects.exclude(wu=-1).exclude(is_expired=True).filter(wu__lte=2000).filter(wu__gt=1000):
			retnum += JintianWorker.objects.exclude(wu=-1).exclude(is_expired=True).filter(wu__gt=1000).filter(wu__lte=2000).aggregate(Sum('wu'))['wu__sum'] /  32
		return retnum

	def sum_jtworker_hash(self):
		return JintianWorker.objects.all().aggregate(Sum('hr_5'))['hr_5__sum'] / 1024

	def sum_jtworker_hash_accepted(self):
		retvalue = 0.0
		for jw in JintianWorker.objects.all():
			retvalue += float(jw.hr_5) * ( 100.0 - jw.pool_reject_ratio ) / 100
		return int(retvalue) / 1024

	def sum_factory_hash_128(self):
		return MinerFactory.objects.all().aggregate(Sum('hr_128'))['hr_128__sum']

	def sum_factory_hash_256(self):
		return MinerFactory.objects.all().aggregate(Sum('hr_256'))['hr_256__sum']

	def sum_factory_hash_225(self):
		return MinerFactory.objects.all().aggregate(Sum('hr_225'))['hr_225__sum']

	def sum_factory_hash_300(self):
		return MinerFactory.objects.all().aggregate(Sum('hr_300'))['hr_300__sum']

	def sum_factory_hash_120(self):
		return MinerFactory.objects.all().aggregate(Sum('hr_120'))['hr_120__sum']

	def get_pools(self):
		return MinerFactory.objects.all()
	
	def get_total_jtworkers(self):
		return JintianWorker.objects.filter(is_expired=False)

	def get_total_jtworkers_dead(self):
		return self.get_total_jtworkers().filter(hr_5=0)

	def get_total_jtworkers_injured(self):
		return self.get_total_jtworkers().filter(hr_5__gt=0).filter(Q(asc0=0) | Q(asc1=0) | Q(asc2=0) | Q(asc3=0) | Q(asc4=0))

	def get_total_jtworkers_dead_180(self):
		return self.get_total_jtworkers_dead().exclude(ipaddress__startswith='192')

	def get_total_jtworkers_injured_180(self):
		return self.get_total_jtworkers_injured().exclude(ipaddress__startswith='192')

	def get_total_jtworkers_dead_10(self):
		return self.get_total_jtworkers_dead().filter(ipaddress__startswith='10')

	def get_total_jtworkers_injured_10(self):
		return self.get_total_jtworkers_injured().filter(ipaddress__startswith='10')

	def get_total_jtworkers_dead_192(self):
		return self.get_total_jtworkers_dead().filter(ipaddress__regex=r'^192|^183')

	def get_total_jtworkers_injured_192(self):
		return self.get_total_jtworkers_injured().filter(ipaddress__regex=r'^192|^183')

	def get_total_jtworkers_fighting(self):
		return self.get_total_jtworkers().filter(hr_5__gt=0).exclude(Q(asc0=0) | Q(asc1=0) | Q(asc2=0) | Q(asc3=0) | Q(asc4=0))

	def get_total_jtworkers_fighting_180(self):
		return self.get_total_jtworkers_fighting().exclude(ipaddress__startswith='192')

	def get_total_jtworkers_fighting_10(self):
		return self.get_total_jtworkers_fighting().filter(ipaddress__startswith='10')

	def get_total_jtworkers_fighting_192(self):
		return self.get_total_jtworkers_fighting().filter(ipaddress__regex=r'^192|^183')

	def get_total_jtworkers_180(self):
		return self.get_total_jtworkers().exclude(ipaddress__startswith='192').order_by('wu')

	def get_total_jtworkers_10(self):
		return self.get_total_jtworkers().filter(ipaddress__startswith='10').order_by('wu')

	def get_total_jtworkers_192(self):
		return self.get_total_jtworkers().filter(ipaddress__startswith='192').order_by('wu')

	def get_total_workers(self):
		return MinerWorker.objects.filter(is_expired=False).count() + int(MinerWorker.objects.get(name='default').hr_225 / MinerWorker.objects.exclude(name='default').exclude(is_expired=True).aggregate(Avg('hr_225'))['hr_225__avg'])

	def get_workers(self):
		return MinerWorker.objects.exclude(hr_300=0)

	def get_bad_jtworkers(self,badmargin=600):
		return JintianWorker.objects.exclude(is_expired=True).filter(ipaddress__startswith='192').filter(Q(hr_5__lt=badmargin) | Q(asc0=0) | Q(asc1=0) | Q(asc2=0) | Q(asc3=0) | Q(asc4=0)).order_by('hr_5','name')

	def get_bad_jtworkers2(self,badmargin=600):
		return JintianWorker.objects.exclude(is_expired=True).exclude(ipaddress__startswith='192').filter(Q(hr_5__lt=badmargin) | Q(asc0=0) | Q(asc1=0) | Q(asc2=0) | Q(asc3=0) | Q(asc4=0)).order_by('hr_5','name')

	def get_bad_jtworkers3(self,badmargin=600):
		return JintianWorker.objects.exclude(is_expired=True).filter(ipaddress__startswith='10').filter(Q(hr_5__lt=badmargin) | Q(asc0=0) | Q(asc1=0) | Q(asc2=0) | Q(asc3=0) | Q(asc4=0)).order_by('hr_5','name')

	def get_bad_workers(self,badmargin=600):
		return MinerWorker.objects.exclude(is_expired=True).filter(hr_225__lt=badmargin)

	def gen_bad_jtworkers_charts(self):
		if not self.get_bad_jtworkers():
			return None
		workers = list()
		for worker in self.get_bad_jtworkers():
			workers.append(worker)
		from reports.models import ReportByJingTianWorker, ReportByJingtianFactory
		jqplots = []
		jqplots2 = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		labels = []
		labels2 = []
		plotdata = []
		plotdata2 = []
		labels2.append('hashrate-total-self-calculated')
		labels2.append('number-of-workers-managed')
		title2 = 'hashrate vs number of miners self calculated'
		plotid2 = re.sub(r' ','-',title2)
		for rp in ReportByJingtianFactory.objects.all().order_by('reporttime'):
			jqplotdata3 += [ [str(rp.reporttime),int(rp.hr_5)] ]
			jqplotdata4 += [ [str(rp.reporttime),int(rp.numworkers)] ]
		plotdata2 += [jqplotdata3, ]
		plotdata2 += [jqplotdata4, ]
		jqplots += [ [plotid2, gen_dateline_js(plotid=plotid2,jqplotdata=plotdata2,title=(title2 + " in Th/s").upper(),labels=labels2,forceTickAt100=False, height='400px')] ]

#		for worker in workers:
#			labels.append("hashrate-sampling-avg" + "-" + worker.name)
#			jqplotdata2 = []
#			for rp in ReportByJingTianWorker.objects.filter(worker=worker).filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(3)).order_by('reporttime'):
#				jqplotdata2 += [ [str(rp.reporttime),int(rp.hr_5)] ]
#			plotdata += [jqplotdata2, ]
#		title = 'hashrate of 10 minute sampling for problematic workers'
#		plotid = re.sub(r' ','-',title)
#		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=plotdata,title=(title + " in Gh/s").upper(),labels=labels,forceTickAt100=False, height='400px')] ]
		return jqplots

	def gen_bad_workers_charts(self):
		if not self.get_bad_workers():
			return None
		workers = list()
		for worker in self.get_bad_workers():
			workers.append(worker)
		from reports.models import ReportByWorker
		jqplots = []
		jqplots2 = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		labels = []
		plotdata = []
		for worker in workers:
			labels.append("hashrate-22m" + "-" + worker.name)
			jqplotdata2 = []
			for rp in ReportByWorker.objects.filter(worker=worker).filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(3)).order_by('reporttime'):
				jqplotdata2 += [ [str(rp.reporttime),int(rp.hr_225)] ]
			plotdata += [jqplotdata2, ]
		title = 'hashrate of 22m for problematic workers'
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=plotdata,title=(title + " in Gh/s").upper(),labels=labels,forceTickAt100=False, height='400px')] ]
		return jqplots

	def gen_bitstamp_charts(self):
		from reports.models import ReportBitStamp
		jqplots = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		jqplotdata5 = []
		labels = [ 'bid', 'ask' ]
#		labels = [ 'bid', 'ask','high','low' ]
		for rp in ReportBitStamp.objects.filter(reporttime__gt=datetime.datetime(2013,11,1,12)):
			jqplotdata2 += [ [str(rp.reporttime),float(rp.bid)] ]
			jqplotdata3 += [ [str(rp.reporttime),float(rp.ask)] ]
#			jqplotdata4 += [ [str(rp.reporttime),float(rp.high)] ]
#			jqplotdata5 += [ [str(rp.reporttime),float(rp.low)] ]
		jqplotdata = [jqplotdata2,jqplotdata3]
#		jqplotdata = [jqplotdata2,jqplotdata3,jqplotdata4,jqplotdata5]
		title = 'bitstamp graphing big picture'
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=(title).upper(),labels=labels,forceTickAt0=False,forceTickAt100=False, fill=[0,1])] ]
		title = 'bitstamp graphing small picture'
		plotid = re.sub(r' ','-',title)
		jqplotdata2 = []
		jqplotdata3 = []
#		for rp in ReportBitStamp.objects.filter(reporttime__gt=datetime.datetime(2014,6,15)):
#			jqplotdata2 += [ [str(rp.reporttime),float(rp.bid)] ]
#			jqplotdata3 += [ [str(rp.reporttime),float(rp.ask)] ]
#		jqplotdata = [jqplotdata2,jqplotdata3]
#		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=(title).upper(),labels=labels,forceTickAt0=False,forceTickAt100=False, fill=[0,1])] ]
		return jqplots

	def gen_worker_charts(self):
		from reports.models import ReportByFactory
		jqplots = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		labels = [ 'pool-hashrate-128s', 'pool-hashrate-256s','pool-hashrate-22m' ]
		for rp in ReportByFactory.objects.all().filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(3)).order_by('reporttime'):
			jqplotdata2 += [ [str(rp.reporttime),int(rp.hr_128)] ]
			jqplotdata3 += [ [str(rp.reporttime),int(rp.hr_256)] ]
			jqplotdata4 += [ [str(rp.reporttime),int(rp.hr_225)] ]
		jqplotdata = [jqplotdata2,jqplotdata3,jqplotdata4,]
		title = 'pool hashrate statistics'
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=(title + " in Gh/s").upper(),labels=labels,forceTickAt100=False, height='400px')] ]
		return jqplots

	def gen_pool_charts(self):
		from reports.models import ReportByFactory
		jqplots = []
		jqplotdata = []
		jqplotdatan = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		jqplotdata5 = []
		jqplotdata6 = []
		jqplotdata7 = []
		jqplotdata8 = []
		labels1 = []
		labels = []
		pools = []
		for pool in MinerFactory.objects.all():
			pools.append(pool)
			labels1.append('coin-mined-' + pool.name)
			labels1.append('coin-paid-' + pool.name)
			labels.append('pool-hashrate-128s-' + pool.name)
			labels.append('pool-hashrate-256s-' + pool.name)
			labels.append('pool-hashrate-22.5m-' + pool.name)
			labels.append('pool-hashrate-3h-' + pool.name)
			labels.append('pool-hashrate-12h-' + pool.name)
#		labels = [ ['coins-mined','coins-payed'], 'pool-hashrate-256-seconds' ]
#			for rp in ReportByFactory.objects.all().filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(0,60 * 60 * 12)).order_by('reporttime'):
			for rp in ReportByFactory.objects.filter(reportdate__gt=datetime.date.today()-datetime.timedelta(5)).order_by('reporttime'):
				jqplotdata2 += [ [str(rp.reporttime),int(rp.blocks * 25)] ]
				jqplotdata3 += [ [str(rp.reporttime),int(rp.coins)] ]
				jqplotdata5 += [ [str(rp.reporttime),int(rp.hr_256)] ]
				jqplotdata4 += [ [str(rp.reporttime),int(rp.hr_128)] ]
				jqplotdata6 += [ [str(rp.reporttime),int(rp.hr_225)] ]
				jqplotdata7 += [ [str(rp.reporttime),int(rp.hr_300)] ]
				jqplotdata8 += [ [str(rp.reporttime),int(rp.hr_120)] ]
			jqplotdata += [jqplotdata2, jqplotdata3,]
			jqplotdatan += [jqplotdata4, jqplotdata5,jqplotdata6,jqplotdata7,jqplotdata8,]
		title = 'coines mined vs paid'
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=title.upper(),labels=labels1,forceTickAt100=False, height='300px')] ]
		title = 'pool hashrate statistics'
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdatan,title=(title + " in Th/s").upper(),labels=labels,forceTickAt100=False, height='500px')] ]
		return jqplots

	def gen_user_charts(self,classwide=False):
		jqplots = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		labels = [ 'users total', 'users activated' ]
		if not classwide:
			for rp in UsageReportByUsage.objects.filter(usage=self).order_by('reportdate'):
				jqplotdata2 += [ [str(rp.reporttime),int(rp.hoststotal)] ]
				jqplotdata3 += [ [str(rp.reporttime),int(rp.hostsvirtual)] ]
				jqplotdata4 += [ [str(rp.reporttime),int(rp.hostsphysical)] ]
			jqplotdata = [ jqplotdata2, jqplotdata3, jqplotdata4 ]
			jqplots += [ ['globalview', gen_dateline_js(plotid='globalview',jqplotdata=jqplotdata,title='GENERAL VIEW - ' + self.name.upper(),labels=labels)] ]
			jqplotdata = []
			jqplotdata2 = []
			jqplotdata3 = []
			jqplotdata4 = []
		else:
			for gp in Usage.objects.all():
				(reportbyusage,created) = UsageReportByUsage.objects.get_or_create(reportdate=datetime.date.today(),usage=gp)
				if created:
					jqplotdata2 += [ [str(gp.name), int('1') ] ]
					jqplotdata3 += [ [str(gp.name), int('1') ] ]
				else:
					jqplotdata2 += [ [str(gp.name), int(reportbyusage.hostsvirtual) ] ]
					jqplotdata3 += [ [str(gp.name), int(reportbyusage.hostsphysical) ] ]
			jqplotdata += [ jqplotdata2 ]
			jqplotdata4 += [ jqplotdata3 ]
			jqplotdata2 = []
			jqplotdata3 = []
			for gp in Usage.objects.all():
				(reportbyusage,created) = UsageReportByUsage.objects.get_or_create(reportdate=datetime.date.today()-datetime.timedelta(7),usage=gp)
				if created:
					jqplotdata2 += [ [str(gp.name), int('1') ] ]
					jqplotdata3 += [ [str(gp.name), int('1') ] ]
				else:
					jqplotdata2 += [ [str(gp.name), int(reportbyusage.hostsvirtual) ] ]
					jqplotdata3 += [ [str(gp.name), int(reportbyusage.hostsphysical) ] ]
			jqplotdata += [ jqplotdata2 ]
			jqplotdata4 += [ jqplotdata3 ]
			jqplotdata2 = []
			jqplotdata3 = []
			for gp in Usage.objects.all():
				(reportbyusage,created) = UsageReportByUsage.objects.get_or_create(reportdate=datetime.date.today()-datetime.timedelta(30),usage=gp)
				if created:
					jqplotdata2 += [ [str(gp.name), int('1') ] ]
					jqplotdata3 += [ [str(gp.name), int('1') ] ]
				else:
					jqplotdata2 += [ [str(gp.name), int(reportbyusage.hostsvirtual) ] ]
					jqplotdata3 += [ [str(gp.name), int(reportbyusage.hostsphysical) ] ]
			jqplotdata += [ jqplotdata2 ]
			jqplotdata4 += [ jqplotdata3 ]
			jqplots += [ ['virtual-today-weekbefore-monthbefore', gen_donut_js(plotid='virtual-today-weekbefore-monthbefore',jqplotdata=jqplotdata,title='VIRTUAL SESSIONS')] ]
			jqplots += [ ['physical-today-weekbefore-monthbefore', gen_donut_js(plotid='physical-today-weekbefore-monthbefore',jqplotdata=jqplotdata4,title='PHYSICAL MACHINES')] ]
		return jqplots
def preuserprofile(sender,instance=None,created=None,**kwargs):
	instance.wellcoin_total = int( instance.wellcoin_self * 1000 )	
	instance.wellcoin_total += int( instance.bitwell * 3000 * 1000 )
	if instance.user_in_miner_group():
		if instance.sha256_first:
			instance.wellcoin_total += int( instance.sha256_first * 55000 * 1000 * 10 / 7 )	
		if instance.sha256_second:
			instance.wellcoin_total += int( instance.sha256_second * 50000 * 1000 * 10 / 7 )	
		if instance.sha256_third_self:
			instance.wellcoin_total += int( instance.sha256_third_self * 1000 * 10 / 7 )	
	instance.wellcoin_total += int( instance.astockcredit * 1000 ) + int( instance.wellcoinact * 1000 )	

pre_save.connect(preuserprofile,sender=UserProfile,dispatch_uid='modellevelpostsave')
