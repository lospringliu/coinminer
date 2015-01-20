# -*- coding: utf-8 -*-
from django.db import models
from common.models import *
import datetime
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class ReportBitStamp(models.Model):
	reporttime = models.DateTimeField(default=datetime.datetime.now)
	high = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	low = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	ask = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	bid = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
	volume = models.DecimalField(max_digits=14,decimal_places=8,default=Decimal('0.00'))
	class Meta:
		ordering = [ 'reporttime', ]
	def __unicode__(self):
		return 'bitstamp info @ ' + str(self.reporttime)

class ReportByJingtianFactory(models.Model):
	reportdate = models.DateField(default=datetime.datetime.today)
	reporttime = models.DateTimeField(default=datetime.datetime.now)
	factory = models.ForeignKey(MinerFactory,verbose_name=_('miner factory'),null=True,blank=True)
	blocks = models.PositiveIntegerField(_("blocks mined"), default=0)
	coins = models.PositiveIntegerField(_("coins payed"), default=0)
	coinspending = models.PositiveIntegerField(_("coins pending"), default=0)
	numworkers = models.IntegerField("number of workers", default=0)
	hr_5 = models.IntegerField("sampling hashrate per 10 minutes", default=0)
	hr_256 = models.IntegerField("256s hashrate", default=0)
	hr_225= models.IntegerField("22.5m hashrate", default=0)
	hr_300= models.IntegerField("3小时算力", default=0)
	hr_120= models.IntegerField("12小时算力", default=0)
	class Meta:
		ordering = [ '-reportdate', 'factory', ]
		verbose_name = _('reportbyjingtian')
		verbose_name_plural = _('reportbyjingtians')
	def __unicode__(self):
		return 'usage info for jingtian @ ' + str(self.reporttime)

class ReportByFactory(models.Model):
	reportdate = models.DateField(default=datetime.datetime.today)
	reporttime = models.DateTimeField(default=datetime.datetime.now)
	factory = models.ForeignKey(MinerFactory,verbose_name=_('miner factory'),null=True,blank=True)
	blocks = models.PositiveIntegerField(_("blocks mined"), default=0)
	coins = models.PositiveIntegerField(_("coins payed"), default=0)
	coinspending = models.PositiveIntegerField(_("coins pending"), default=0)
	hr_128 = models.IntegerField("128s hashrate", default=0)
	hr_256 = models.IntegerField("256s hashrate", default=0)
	hr_225= models.IntegerField("22.5m hashrate", default=0)
	hr_300= models.IntegerField("3小时算力", default=0)
	hr_120= models.IntegerField("12小时算力", default=0)
	class Meta:
		ordering = [ '-reportdate', 'factory', ]
		verbose_name = _('report by factory')
		verbose_name_plural = _('report by factorys')
	def __unicode__(self):
		return 'usage info by factory @ ' + str(self.reporttime)

class ReportByWorker(models.Model):
	reportdate = models.DateField(default=datetime.datetime.today)
	reporttime = models.DateTimeField(default=datetime.datetime.now)
	worker = models.ForeignKey(MinerWorker,null=True,blank=True)
	hr_225= models.IntegerField("22.5m hashrate", default=0)
	hr_300 = models.IntegerField("3h hashrate", default=0)
	hr_120 = models.IntegerField("12h hashrate", default=0)
	class Meta:
		ordering = [ '-reportdate', '-reporttime','hr_225', ]
		verbose_name = _('report by worker')
		verbose_name_plural = _('report by workers')

	def __unicode__(self):
		return 'usage info by ' + self.worker.name + ' @ ' + str(self.reporttime)

class ReportByJingTianWorker(models.Model):
	reportdate = models.DateField(default=datetime.datetime.today)
	reporttime = models.DateTimeField(default=datetime.datetime.now)
	worker = models.ForeignKey(JintianWorker,null=True,blank=True)
	hr_5= models.IntegerField("sample hashrate", default=0)
	hr_225= models.IntegerField("22.5m hashrate", default=0)
	hr_300 = models.IntegerField("3h hashrate", default=0)
	hr_120 = models.IntegerField("12h hashrate", default=0)
	class Meta:
		ordering = [ '-reportdate', '-reporttime','hr_225', ]
		verbose_name = _('report by worker')
		verbose_name_plural = _('report by workers')

	def __unicode__(self):
		return 'usage info by ' + self.worker.name + ' @ ' + str(self.reporttime)

