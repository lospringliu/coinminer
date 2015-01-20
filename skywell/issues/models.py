# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import *
from userprofiles.models import UserProfile
import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User, Group

# Create your models here.
class JingTianResult(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	miner = models.ForeignKey(JintianWorker)
	updated = models.BooleanField(default=False)
	def __str__(self):
		if self.updated:
			return self.miner.ipaddress + " updated " + str(self.timestamp)
		else:
			return self.miner.ipaddress + " not updated"
class TodoList(models.Model):
	issuestart = models.DateTimeField(auto_now_add=True)
	issuewith = models.ForeignKey(User,null=True,blank=True,default=None,editable=False)
	issuesolveby = models.ForeignKey(User,related_name='solveby',null=True,blank=True,default=None,editable=False)
	issuetype = models.ForeignKey(IssueType,null=True,blank=True,default=None)
	quantity = models.CharField(_('quantity'),null=True,blank=True,max_length=8,default=None)
	desc = models.CharField(_('description'),max_length=64,null=True,blank=True,default=None)
	note = models.CharField(_('note'),max_length=64,null=True,blank=True,default=None)
	solved = models.BooleanField(_('solved'),default=False)

	class Meta:
		verbose_name = _('todolist')
		verbose_name_plural = _('todolists')
		ordering = [ '-issuestart',  ]
	def __unicode__(self):
		return self.desc
	def fullname(self):
		if self.issuewith:
			return self.issuewith.userprofile.fullname
		else:
			return ''
	fullname.verbose_name = _("fullname")
	def qqdisplay(self):
		if self.issuewith:
			return self.issuewith.userprofile.qqdisplay
		else:
			return ''
	qqdisplay.verbose_name = _("qqdisplay")

class LogRecord(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True,editable=False)
	target = models.ForeignKey(UserProfile,editable=False)
	updator = models.ForeignKey(User,editable=False)
	sha256_first = models.DecimalField(_('sha_first_purchase'),  max_digits=5,decimal_places=2,editable=False)
	sha256_second = models.DecimalField(_('sha_second_purchase'),max_digits=5,decimal_places=2,editable=False)
	scrypt_first = models.IntegerField(_('scrypt_first_purchase'),editable=False)
#	sha256_third = models.IntegerField(_('sha_third_purchase'),editable=False)
	note = models.CharField(_('log note'),max_length=64,editable=False)

	class Meta:
		verbose_name = _('logrecord')
		verbose_name_plural = _('logrecords')
		ordering = [ '-timestamp', ]
	def __unicode__(self):
		return self.note
	def fullname(self):
		if self.target:
			return self.target.fullname
		else:
			return ''
	fullname.verbose_name = _("fullname")
	def qqdisplay(self):
		if self.target:
			return self.target.qqdisplay
		else:
			return ''
	qqdisplay.verbose_name = _("qqdisplay")

