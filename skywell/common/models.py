# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from common.functions import *
from django.utils.encoding import python_2_unicode_compatible
import datetime
import time
import re
import os,sys
from decimal import Decimal
#from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
@python_2_unicode_compatible
class ResourceType(models.Model):
	name = models.CharField(_('name'),max_length=16,unique=True)
	class Meta:
		verbose_name = _('resourcetype')
		verbose_name_plural = _('resourcetypes')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class IdType(models.Model):
	name = models.CharField(_('name'),max_length=16,unique=True)
	class Meta:
		verbose_name = _('idtype')
		verbose_name_plural = _('idtypes')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class IssueType(models.Model):
	name = models.CharField(_('name'),max_length=16,unique=True)
	class Meta:
		verbose_name = _('issuetype')
		verbose_name_plural = _('issuetypes')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class CoinType(models.Model):
	name = models.CharField(_('name'),max_length=16,unique=True)
	class Meta:
		verbose_name = _('cointype')
		verbose_name_plural = _('cointypes')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class Wallet(models.Model):
	wallet = models.CharField(max_length=34,unique=True)
	cointype = models.ForeignKey(CoinType,verbose_name=_('cointype'),null=True,blank=True,default=None)
	name = models.CharField(max_length=16,blank=True,null=True,default="update me")
	class Meta:
		pass
	def __str__(self):
		if self.name != 'update me':
			return self.name
		else:
			return self.wallet
	class Admin:
		pass

@python_2_unicode_compatible
class ShareResource(models.Model):
	name = models.CharField(_('Resource Name'),max_length=16,unique=True)
	resourcetype = models.ForeignKey(ResourceType,verbose_name=_('resourcetype'),null=True,blank=True,default=None)
	provider = models.ForeignKey(User,verbose_name=_('provider'),null=True,blank=True,default=None)
	description = models.CharField(_('description'),max_length=128)
	uri = models.URLField(_('link'),max_length=64,default='http://url/')
	class Meta:
		verbose_name = _('share resource')
		verbose_name_plural = _('share resources')
	def __str__(self):
		return self.name
	def link_in_web(self):
		if re.match(r'http',self.uri):
			return "<a href=\"" + self.uri + "\" target=\"_new\">" + self.uri + "</a>"
		else:
			return self.uri
	link_in_web.verbose_name = _('link')
	link_in_web.allow_tags = True


@python_2_unicode_compatible
class BitStamp(models.Model):
	high = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	low = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	ask = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	bid = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	volume = models.DecimalField(max_digits=14,decimal_places=8,default=Decimal('0.00'))
	class Meta:
		verbose_name = 'bitstamp'
		verbose_name_plural = 'bitstamp'

	def __str__(self):
	    return "ask: " + str(self.ask) + "\tbid: " + str(self.bid)

	def update(self):
		import subprocess
		import json
		try:
			outjson = subprocess.check_output(['/bin/bash','-c','wget -o /dev/null -O- --no-check-certificate https://www.bitstamp.net/api/ticker/'])
			outvalues = json.loads(outjson)
			self.high = Decimal(outvalues['high'])
			self.low = Decimal(outvalues['low'])
			self.ask = Decimal(outvalues['ask'])
			self.bid = Decimal(outvalues['bid'])
			self.volume = Decimal(outvalues['volume'])
			self.save()
		except  subprocess.CalledProcessError:
			pass
@python_2_unicode_compatible
class BtcFund(models.Model):
	name = models.CharField("基金名称",max_length=16,unique=True)
	cointype = models.ForeignKey(CoinType,verbose_name=_('cointype'),null=True,blank=True,default=None)
	coins = models.PositiveIntegerField('coin balance',default=0)
	website = models.URLField(max_length=96,default="https://blockchain.info/en/address/1cBCnJdfUUv2QdkdzsAWoah1AmhkWTKZP")
	class Meta:
		verbose_name = 'btc fund'
		verbose_name_plural = 'btc funds'

	def __str__(self):
	    return str(self.coins)

	def get_balance(self):
		from requests import get
		html = get(self.website)
		linescoins = re.compile(r'.*id=\"final_balance\".*',re.M).findall(html.text)
		for line in linescoins:
			valuematch = re.match(r".*<span data-c=\".*\">(?P<coins>.*)BTC</span></font>.*",line)
			if valuematch:
				valuedict = valuematch.groupdict()
				try:
					values = int(float(valuematch.groupdict()['coins'].strip()) + 0.4)
				except ValueError:
					values = self.coins
				self.coins = values
				self.save()

@python_2_unicode_compatible
class MinerFactory(models.Model):
	name = models.CharField(_('Miner Factory Name'),max_length=16,unique=True)
	blocks = models.PositiveIntegerField(_('blocks found'),default=0)
	cointype = models.ForeignKey(CoinType,verbose_name=_('cointype'),null=True,blank=True,default=None)
	coins = models.PositiveIntegerField(_('coins payed'),default=0)
	coinspending = models.PositiveIntegerField(_('coins pending'),default=0)
	hr_128 = models.PositiveIntegerField(_('hashrate in 128s'),default=0)
	hr_256 = models.PositiveIntegerField(_('hashrate in 256s'),default=0)
	hr_225 = models.PositiveIntegerField(_('hashrate in 22.5m'),default=0)
	hr_300 = models.PositiveIntegerField('矿池3小时算力',default=0)
	hr_120 = models.PositiveIntegerField('矿池12小时算力',default=0)
	link = models.CharField(_('Miner Factory Link'),max_length=96)
	website = models.URLField(max_length=32,default="http://website")
	class Meta:
		verbose_name = _('miner factory')
		verbose_name_plural = _('miner factorys')
	def __str__(self):
	    return self.name + "@" + str(self.hr_128) + "Th/s Payed " + str(self.coins) + " " + self.cointype.name
	class Admin:
	    pass
	def coinsmined(self):
		return 25 * self.blocks
	def gen_charts(self):
		from reports.models import ReportByFactory
		jqplots = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		jqplotdata5 = []
		jqplotdata6 = []
		jqplotdata7 = []
		jqplotdata8 = []
		labels1 = [ 'pool-coins-mined-' + self.name, 'pool-coins-payed-' + self.name ]
		labels = [ 'pool-hashrate-128s-' + self.name, 'pool-hashrate-256s-' + self.name, 'pool-hashrate-22m-' + self.name, 'pool-hashrate-3h-' + self.name, 'pool-hashrate-12h-' + self.name ]
#		labels = [ ['coins-mined','coins-payed'], 'pool-hashrate-256-seconds' ]
		for rp in ReportByFactory.objects.filter(factory=self).filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(5)).order_by('reporttime'):
			jqplotdata2 += [ [str(rp.reporttime),int(rp.blocks * 25)] ]
			jqplotdata3 += [ [str(rp.reporttime),int(rp.coins)] ]
			jqplotdata5 += [ [str(rp.reporttime),int(rp.hr_256)] ]
			jqplotdata4 += [ [str(rp.reporttime),int(rp.hr_128)] ]
			jqplotdata6 += [ [str(rp.reporttime),int(rp.hr_225)] ]
			jqplotdata7 += [ [str(rp.reporttime),int(rp.hr_300)] ]
			jqplotdata8 += [ [str(rp.reporttime),int(rp.hr_120)] ]
#			jqplotdata += [jqplotdata2, jqplotdata3]
		jqplotdata = [jqplotdata2, jqplotdata3,]
		title = 'coines mined vs paid' + " " + self.name
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=title.upper(),labels=labels1,forceTickAt100=False, height='300px')] ]
		jqplotdata = [jqplotdata4, jqplotdata5,jqplotdata6,jqplotdata7,jqplotdata8,]
		title = 'pool hashrate statistics' + " " + self.name
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=jqplotdata,title=(title + " in Th/s").upper(),labels=labels,forceTickAt100=False, height='500px')] ]
		return jqplots

	def history(self):
		return "<a href=\"/django/admin/reports/reportbyfactory/?factory_id__exact=" + str(self.id) + "\" target=\"_new\">历史</a>"
	history.allow_tags = True

	def visualize(self):
		return "<a href=\"/django/charts/?model=MinerFactory&name=" + self.name + "\" target=\"_new\">图表</a>"
	visualize.allow_tags = True

	def get_blocks(self):
		from requests import get
		if self.name == 'eligius':
			html = get("http://eligius.st/~wizkid057/newstats/blocks.php")
			ret = re.findall("1swrtyBsp", html.text)
			self.blocks = max(len(ret)/2,self.blocks)
			self.save()

	def get_pay(self):
		from requests import get
		if self.name == 'eligius':
			hurl = self.website + self.link
			html = get(hurl)
			if not html.status_code == 200:
				return
			linescoinspending = re.compile(r'.*Estimated Total:.*',re.M).findall(html.text)
			linescoins = re.compile(r'.*All time total payout:.*',re.M).findall(html.text)
			for line in linescoinspending:
				valuematch = re.match(r".*<TD>Estimated Total: </TD><TD style=\"text-align: right;\">(?P<coinspending>.*)BTC</TD>.*",line)
				valuematchhr = re.match(r".*<TD>12 hours</TD><TD style=\"text-align: right;\">(?P<hr_120>.*)</TD><TD.*<TD>3 hours</TD><TD style=\"text-align: right;\">(?P<hr_300>.*)</TD><TD.*<TD>22.5 minutes</TD><TD style=\"text-align: right;\">(?P<hr_225>.*)</TD><TD.*<TD>256 seconds</TD><TD style=\"text-align: right;\">(?P<hr_256>.*)</TD><TD.*<TD>128 seconds</TD><TD style=\"text-align: right;\">(?P<hr_128>.*)</TD><TD style=\"text-align.*BUTTON.*",line)
				if valuematch:
					valuedict = valuematch.groupdict()
					try:
						values = int(float(valuematch.groupdict()['coinspending'].strip()))
					except ValueError:
						values = 0
					self.coinspending = values
					self.save()
				if valuematchhr:
					valuedict = valuematchhr.groupdict()
					for k in valuedict.keys():
						rer = re.match('(.*) Th.*',valuedict[k]) 
						if rer:
							values = rer.groups()[0]
						elif re.match('(.*) Gh.*',valuedict[k]):
							values = re.match('(.*) Gh.*',valuedict[k]).groups()[0]
							try:
								values = str(float(values) / 1000)
							except ValueError:
								values = '1.0'
						else:
							values = '1.0'
						try:
							valuedict[k] = int(float(re.sub(r',','',values)))
						except ValueError:
							valuedict[k] = 1
							
					hr_225 = valuedict['hr_225']
					hr_128 = valuedict['hr_128']
					hr_256 = valuedict['hr_256']
					hr_300 = valuedict['hr_300']
					hr_120 = valuedict['hr_120']
					self.hr_128 = hr_128
					self.hr_225 = hr_225
					self.hr_256 = hr_256
					self.hr_300 = hr_300
					self.hr_120 = hr_120
					self.save()
			for line in linescoins:
				valuematch = re.match(r".*</table>All time total payout:(?P<coins>.*)BTC<BR>.*",line)
				if valuematch:
					valuedict = valuematch.groupdict()
					try:
						values = int(float(valuematch.groupdict()['coins'].strip()))
					except ValueError:
						values = self.coins
					self.coins = values
					self.save()

@python_2_unicode_compatible
class JintianWorker(models.Model):
	name = models.CharField('矿机名称',max_length=16)
	wallet = models.ForeignKey(Wallet,verbose_name='钱包',null=True,blank=True,default=None)
	ipaddress = models.IPAddressField("IP地址")
	macaddress = models.CharField("mac address",max_length=17,blank=True,null=True,default=None)
	mmaddress = models.CharField("management address",max_length=17,blank=True,null=True,default=None)
	apiport = models.PositiveIntegerField('端口',default=4028)
	factory = models.ForeignKey(MinerFactory, verbose_name='所在矿场',null=True,blank=True,default=None)
	note = models.CharField('注释',max_length=32,default=None,null=True,blank=True)
	device_reject_ratio = models.PositiveIntegerField('硬件拒绝率',default=0,editable=False)
	pool_reject_ratio = models.PositiveIntegerField('矿场拒绝率',default=0,editable=False)
	hr_5 = models.PositiveIntegerField('总计算力',default=0,editable=False)
	wu = models.IntegerField('WorkUtil',default=0,editable=False)
	asc0 = models.PositiveIntegerField('板0算力',default=0,editable=False)
	asc1 = models.PositiveIntegerField('板1算力',default=0,editable=False)
	asc2 = models.PositiveIntegerField('板2算力',default=0,editable=False)
	asc3 = models.PositiveIntegerField('板3算力',default=0,editable=False)
	asc4 = models.PositiveIntegerField('板4算力',default=0,editable=False)
	asc5 = models.PositiveIntegerField('板5算力',default=0,editable=False)
	asc0_cores = models.PositiveIntegerField('板0核心数目',default=0,editable=False)
	asc1_cores = models.PositiveIntegerField('板1核心数目',default=0,editable=False)
	asc2_cores = models.PositiveIntegerField('板2核心数目',default=0,editable=False)
	asc3_cores = models.PositiveIntegerField('板3核心数目',default=0,editable=False)
	asc4_cores = models.PositiveIntegerField('板4核心数目',default=0,editable=False)
	asc5_cores = models.PositiveIntegerField('板5核心数目',default=0,editable=False)
	asc0_temp = models.CharField('板0温度',max_length=32,null=True,blank=True,editable=False)
	asc1_temp = models.CharField('板1温度',max_length=32,null=True,blank=True,editable=False)
	asc2_temp = models.CharField('板2温度',max_length=32,null=True,blank=True,editable=False)
	asc3_temp = models.CharField('板3温度',max_length=32,null=True,blank=True,editable=False)
	asc4_temp = models.CharField('板4温度',max_length=32,null=True,blank=True,editable=False)
	asc5_temp = models.CharField('板5温度',max_length=32,null=True,blank=True,editable=False)
	is_expired = models.BooleanField(default=False)
	class Meta:
		verbose_name = '井天矿机'
		verbose_name_plural = '井天矿机'
		unique_together = ("ipaddress", "apiport")
		ordering = [ 'name', ]
	def __str__(self):
	    return self.ipaddress
	class Admin:
	    pass
	def tempcut(self):
		max_temp = 0
		if self.asc0_temp:
			for temp in self.asc0_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		if self.asc1_temp:
			for temp in self.asc1_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		if self.asc2_temp:
			for temp in self.asc2_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		if self.asc3_temp:
			for temp in self.asc3_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		if self.asc4_temp:
			for temp in self.asc4_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		if self.asc5_temp:
			for temp in self.asc5_temp.split('-'):
				max_temp = max(max_temp,int(temp))
		return max_temp
	def rtdata_server(self):
		if re.match(r'^10.10',self.ipaddress):
			return "http://58.211.84.2:8000/jtminer/"
		elif re.match(r'^192.168',self.ipaddress):
			return	"http://183.213.16.34:8000/jtminer/"
		else:
			return "https://ec2-54-213-74-78.us-west-2.compute.amazonaws.com/django/jtminer/"
	rtdata_server.allow_tags = True
	def update(self):
		from pycgminer import CgminerAPI
		cm = CgminerAPI(host=self.ipaddress,port=self.apiport)
		cm_summary = cm.summary()
		self.hr_5 = 0
		self.wu = -1
		if type(cm_summary) == type(dict()):
			if cm_summary.has_key('SUMMARY'):
				if cm_summary['SUMMARY'][0].has_key('MHS av'):
					self.hr_5 = int(float(cm_summary['SUMMARY'][0]['MHS av']) / 1024 + 0.4)
				if cm_summary['SUMMARY'][0].has_key('Pool Rejected%'):
					self.pool_reject_ratio = int(cm_summary['SUMMARY'][0]['Pool Rejected%'])
				if cm_summary['SUMMARY'][0].has_key('Device Rejected%'):
					self.device_reject_ratio = int(cm_summary['SUMMARY'][0]['Device Rejected%'])
				if cm_summary['SUMMARY'][0].has_key('Work Utility'):
					self.wu = int(cm_summary['SUMMARY'][0]['Work Utility'])
		else:
			self.save()
			return None
		cm_stats = cm.stats()
		if type(cm_stats) == type(dict()):
			if cm_stats.has_key('STATS'):
				for asc in cm_stats['STATS']:
					if asc.has_key('CS'):
						if asc['STATS'] == 0:
							self.asc0_temp = asc['Temperature']
							self.asc0_cores = asc['cores']
						elif asc['STATS'] == 1:
							self.asc1_temp = asc['Temperature']
							self.asc1_cores = asc['cores']
						elif asc['STATS'] == 2:
							self.asc2_temp = asc['Temperature']
							self.asc2_cores = asc['cores']
						elif asc['STATS'] == 3:
							self.asc3_temp = asc['Temperature']
							self.asc3_cores = asc['cores']
						elif asc['STATS'] == 4:
							self.asc4_temp = asc['Temperature']
							self.asc4_cores = asc['cores']
						elif asc['STATS'] == 5:
							self.asc5_temp = asc['Temperature']
							self.asc5_cores = asc['cores']
						else:
							pass
		cm_devs = cm.devs()
		if type(cm_devs) == type(dict()):
			if cm_devs.has_key('DEVS'):
				for asc in cm_devs['DEVS']:
					if asc.has_key('MHS av'):
						if asc['ID'] == 0:
							self.asc0 = int(float(asc['MHS av']) / 1024 + 0.4)
						elif asc['ID'] == 1:
							self.asc1 = int(float(asc['MHS av']) / 1024 + 0.4)
						elif asc['ID'] == 2:
							self.asc2 = int(float(asc['MHS av']) / 1024 + 0.4)
						elif asc['ID'] == 3:
							self.asc3 = int(float(asc['MHS av']) / 1024 + 0.4)
						elif asc['ID'] == 4:
							self.asc4 = int(float(asc['MHS av']) / 1024 + 0.4)
						elif asc['ID'] == 5:
							self.asc5 = int(float(asc['MHS av']) / 1024 + 0.4)
						else:
							pass
		self.save()

	def to_table(self):
		ptabs = 1
		from pycgminer import CgminerAPI
		cm = CgminerAPI(host=self.ipaddress)
		cm_summary = cm.summary()
		retstring = "\t" * ptabs + "<table>\n"
		retstring += "\t" * ptabs + "\t<tr><td>\n"
		if type(cm_summary) == type(dict()):
			for key in cm_summary.keys():
				if key == 'STATUS' or key == 'id':
					continue
				retstring += "\t" * ptabs + "\t<tr><td>\n"
				retstring += "\t" * ptabs + "\t" + str(key) + "\n"
				retstring += "\t" * ptabs + "\t</td></tr>\n"
				retstring += html_tablize(cm_summary[key],ptabs=ptabs+3)
		retstring += "\t" * ptabs + "\t</td></tr>\n"
		retstring += "\t" * ptabs + "\t<tr><td>\n"
		cm_summary = cm.devs()
		if type(cm_summary) == type(dict()):
			for key in cm_summary.keys():
				if key == 'STATUS' or key == 'id':
					continue
				retstring += "\t" * ptabs + "\t<tr><td>\n"
				retstring += "\t" * ptabs + "\t" + str(key) + "\n"
				retstring += "\t" * ptabs + "\t</td></tr>\n"
				retstring += html_tablize(cm_summary[key],ptabs=ptabs+3)
		retstring += "\t" * ptabs + "\t</td></tr>\n"
		retstring += "\t" * ptabs + "</table>\n"
		return retstring

	def show_astable(self):
		retstring = """
		<table>
		"""
		retstring += "<tr><td>IP: " + self.ipaddress + "</td><td>Work Utility: " + str(self.wu) + "</td><td>Hash Rate: " + str(self.hr_5) + "</td><td>Name: " + self.name + "</td></tr>"
		retstring += "<tr><td>板0</td><td>hashrate:%4g</td><td>cores:%3g</td><td>温度:%s</td>" % (self.asc0,self.asc0_cores,self.asc0_temp)
		retstring += "<tr><td>板1</td><td>hashrate:%4g</td><td>cores:%3g</td><td>温度:%s</td>" % (self.asc1,self.asc1_cores,self.asc1_temp)
		retstring += "<tr><td>板2</td><td>hashrate:%4g</td><td>cores:%3g</td><td>温度:%s</td>" % (self.asc2,self.asc2_cores,self.asc2_temp)
		retstring += "<tr><td>板3</td><td>hashrate:%4g</td><td>cores:%3g</td><td>温度:%s</td>" % (self.asc3,self.asc3_cores,self.asc3_temp)
		retstring += "<tr><td>板4</td><td>hashrate:%4g</td><td>cores:%3g</td><td>温度:%s</td>" % (self.asc4,self.asc4_cores,self.asc4_temp)
		retstring += """
		</table>
		"""
		return retstring

	def as_table(self):
		retstring = """
		<table>
		"""
		from pycgminer import CgminerAPI
		cm = CgminerAPI(host=self.ipaddress)
		cm_summary = cm.summary()
		if type(cm_summary) == type(dict()):
			for key in cm_summary.keys():
				if key == 'STATUS' or key == 'id':
					continue
				value = cm_summary[key]
				retstring += "\n\t\t<tr><a name=\"%s\"><td>%s</td>" % (self.ipaddress,str(key))
				if type(value) == type(list()):
					retstring += "\n\t\t<td><table>"
					for listitem in value:
						if type(listitem) == type(dict()):
							retstring += "\n\t\t\t<td><table>"
							for kkey in listitem.keys():
								retstring += "\n\t\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(listitem[kkey]))
							retstring += "\n\t\t\t</table></td>"
						else:
							retstring += "\n\t\t\t<tr><td>%s</td></tr>" % str(listitem)
					retstring += "\n\t\t</table></td>"
				elif type(value) == type(dict()):
					retstring += "\n\t\t<td><table>"
					for kkey in value.keys():
						retstring += "\n\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(value[kkey]))
					retstring += "\n\t\t</table></td>"
				else:
					retstring += "\n\t\t<td>%s</td>" % str(value)
				retstring += "\n\t\t</tr>"
		else:
			retstring += "<tr><td>无法连接到API，请汇报给运维人员</td></tr>"
			retstring += """
			</table>
			"""
			return retstring
		cm_summary = cm.stats()
		if type(cm_summary) == type(dict()):
			for key in cm_summary.keys():
				if key == 'STATUS' or key == 'id':
					continue
				value = cm_summary[key]
				retstring += "\n\t\t<tr><a name=\"%s\"><td>%s</td>" % (self.ipaddress,str(key))
				if type(value) == type(list()):
					retstring += "\n\t\t<td><table>"
					for listitem in value:
						if type(listitem) == type(dict()):
							retstring += "\n\t\t\t<td><table>"
							for kkey in listitem.keys():
								retstring += "\n\t\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(listitem[kkey]))
							retstring += "\n\t\t\t</table></td>"
						else:
							retstring += "\n\t\t\t<tr><td>%s</td></tr>" % str(listitem)
					retstring += "\n\t\t</table></td>"
				elif type(value) == type(dict()):
					retstring += "\n\t\t<td><table>"
					for kkey in value.keys():
						retstring += "\n\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(value[kkey]))
					retstring += "\n\t\t</table></td>"
				else:
					retstring += "\n\t\t<td>%s</td>" % str(value)
				retstring += "\n\t\t</tr>"
		else:
			retstring += "<tr><td>无法连接到API，请汇报给运维人员</td></tr>"
		cm_summary = cm.devs()
		if type(cm_summary) == type(dict()):
			for key in cm_summary.keys():
				if key == 'STATUS' or key == 'id':
					continue
				value = cm_summary[key]
				retstring += "\n\t\t<tr><a name=\"%s\"><td>%s</td>" % (self.ipaddress,str(key))
				if type(value) == type(list()):
					retstring += "\n\t\t<td><table>"
					for listitem in value:
						if type(listitem) == type(dict()):
							retstring += "\n\t\t\t<td><table>"
							for kkey in listitem.keys():
								retstring += "\n\t\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(listitem[kkey]))
							retstring += "\n\t\t\t</table></td>"
						else:
							retstring += "\n\t\t\t<tr><td>%s</td></tr>" % str(listitem)
					retstring += "\n\t\t</table></td>"
				elif type(value) == type(dict()):
					retstring += "\n\t\t<td><table>"
					for kkey in value.keys():
						retstring += "\n\t\t\t<tr><td>%s</td><td>%s</td></tr>" % (str(kkey),str(value[kkey]))
					retstring += "\n\t\t</table></td>"
				else:
					retstring += "\n\t\t<td>%s</td>" % str(value)
				retstring += "\n\t\t</tr>"
		else:
			retstring += "<tr><td>无法连接到API，请汇报给运维人员</td></tr>"
		retstring += """
		</table>
		"""
		return retstring
	as_table.allow_tags = True
	def details(self):
		return "<a href=\"/django/jtminer/?minerid=" + str(self.id) + "\" target=\"_new\">详细数据</a>"
	details.allow_tags = True

@python_2_unicode_compatible
class MinerWorker(models.Model):
	name = models.CharField(_('Miner Worker Name'),max_length=16)
	factory = models.ForeignKey(MinerFactory, verbose_name=_('Miner Factory Name'),null=True,blank=True,default=None)
	is_expired = models.BooleanField(default=False)
	hr_225 = models.PositiveIntegerField(_('hashrate in 22.5m'),default=0)
	hr_300= models.PositiveIntegerField(_('hashrate in 3h'),default=0)
	hr_120= models.PositiveIntegerField(_('hashrate in 12h'),default=0)
	class Meta:
		verbose_name = _('miner worker')
		verbose_name_plural = _('miner workers')
		unique_together = ("name", "factory")
		ordering = [ 'factory', 'hr_225', ]
	def __str__(self):
	    return self.name + '@' + str(self.hr_225) + "Gh/s in " + self.factory.name + " for " + self.factory.cointype.name
	class Admin:
	    pass
	def gen_charts(self):
		from reports.models import ReportByWorker
		jqplots = []
		jqplots2 = []
		jqplotdata = []
		jqscript = ""
		jqplotdata2 = []
		jqplotdata3 = []
		jqplotdata4 = []
		labels = [ 'hashrate-22m', 'hashrate-3h','hashrate-12h' ]
		for rp in ReportByWorker.objects.filter(worker=self).filter(reporttime__gt=datetime.datetime.now() - datetime.timedelta(3)).order_by('reporttime'):
			jqplotdata2 += [ [str(rp.reporttime),int(rp.hr_225)] ]
			jqplotdata3 += [ [str(rp.reporttime),int(rp.hr_300)] ]
			jqplotdata4 += [ [str(rp.reporttime),int(rp.hr_120)] ]
		plotdata = [jqplotdata2, jqplotdata3, jqplotdata4,]
		title = 'hashrate of 22m 3h 12h for ' + self.name
		plotid = re.sub(r' ','-',title)
		jqplots += [ [plotid, gen_dateline_js(plotid=plotid,jqplotdata=plotdata,title=(title + " in Gh/s").upper(),labels=labels,forceTickAt100=False, height='400px')] ]
		return jqplots
	def history(self):
		return "<a href=\"/django/admin/reports/reportbyworker/?o=-1.2&worker__id__exact=" + str(self.id) + "\" target=\"_new\">历史</a>"
	history.allow_tags = True
	def visualize(self):
		return "<a href=\"/django/charts/?model=MinerWorker&name=" + self.name + "\" target=\"_new\">图表</a>"
	visualize.allow_tags = True

@python_2_unicode_compatible
class TransferContent(models.Model):
	name = models.CharField(_('transfer content'),max_length=16,unique=True)
	displayname = models.CharField(_('transfer display name'),max_length=32,null=True,blank=True)
	class Meta:
		verbose_name = _('transfercontent')
		verbose_name_plural = _('transfercontents')
	def __str__(self):
	    return self.displayname
	class Admin:
	    pass

@python_2_unicode_compatible
class Subscription(models.Model):
	name = models.CharField(_('name'),max_length=16,unique=True)
	class Meta:
		verbose_name = _('subscription')
		verbose_name_plural = _('subscriptions')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class Country(models.Model):
	name = models.CharField("国家",max_length=16,unique=True)
	creator = models.ForeignKey(User,verbose_name=_('creator'),blank=True,default=None,editable=False,null=True)
	class Meta:
		verbose_name = _('country')
		verbose_name_plural = _('countrys')
	def __str__(self):
	    return self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class Province(models.Model):
	name = models.CharField("省份",max_length=16,unique=True)
	parent = models.ForeignKey(Country,verbose_name="国家",related_name='provinces')
	creator = models.ForeignKey(User,verbose_name=_('creator'),blank=True,default=None,editable=False,null=True)
	class Meta:
		verbose_name = _('province')
		verbose_name_plural = _('provinces')
		ordering = ['-parent',]
	def __str__(self):
	    return self.parent.name + "->" + self.name
	class Admin:
	    pass

@python_2_unicode_compatible
class Location(models.Model):
	name = models.CharField("城市",max_length=16,unique=True)
	province = models.ForeignKey(Province,verbose_name="省份",related_name='locations')
	parent = models.ForeignKey('self',verbose_name=_('belong to'),null=True,default=None,blank=True,related_name='children')
	creator = models.ForeignKey(User,verbose_name=_('creator'),blank=True,default=None,editable=False,null=True)
	class Meta:
		verbose_name = _('location')
		verbose_name_plural = _('locations')
		ordering = ['province',]
	def __str__(self):
	    return self.province.__unicode__() + "->" + self.name
	class Admin:
	    pass
