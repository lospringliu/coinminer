# -*- coding: utf-8 -*-
from django.contrib import admin
from userprofiles.models import *
from userprofiles.models import UserProfile as OverseaInfo
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from issues.models import *
from django.utils.encoding import force_unicode
from django.contrib.admin import helpers
from django.shortcuts import render_to_response
from django import http, template
import random


# Register your models here.
class MyUserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['user','minerid','fullname','location','payname','qqdisplay','lock_sha256_first','sha256_first', 'lock_sha256_second','sha256_second', 'lock_scrypt_first','scrypt_first','changenote']
	def clean_changenote(self):
		if len(self.cleaned_data['changenote']) < 4:
			raise ValidationError('请留下修改原因',code='required')
		return self.cleaned_data["changenote"]

class UserProfileAdmin(admin.ModelAdmin):
#	list_display = ('user','fullname','location','lock_sha256_first','sha256_first', 'lock_sha256_second','sha256_second','lock_scrypt_first', 'scrypt_first','sha256_third')
	list_display = ('user','minerid','fullname','payname','lock_sha256_first','sha256_first','lock_sha256_second','sha256_second','btctominer','scrypt_first','location',)
	list_per_page = 10
	list_max_show_all = 3000
	list_filter = ('lock_sha256_first','lock_sha256_second','lock_scrypt_first','user__groups','location__province__parent')
	search_fields = ['user__username','payname','qqdisplay','fullname','location__name','location__province__name']
#	fields = ['user','fullname','qqdisplay','sha256_first', 'sha256_second', 'scrypt_first', 'changenote']
	readonly_fields = ('user','lock_sha256_first','lock_sha256_second','lock_scrypt_first')
	form = MyUserProfileForm
	actions = ['reset_minerid','reset_password','confirm_sha256_first','confirm_sha256_second','add_newuser','confirm_scrypt_first','remove_from_miners_group','add_into_miners_group']
#	list_editable = ('minerid',)
#	readonly_fields = ('user','wellcoin','hitechfund','lock_sha256_first','lock_sha256_second','lock_scrypt_first','sha256_third','subscription','coinfund','btcwallet','ltcwallet','location')

	def has_change_permission(self,request, obj=None):
		if obj and not ( obj.id == request.user.userprofile.id and obj.user_in_miner_group() ) and not ( request.user.is_superuser or request.user.userprofile.user_in_banzhu_group()):
			return False
		else:
			return True
	def get_queryset(self, request):
		qs = super(UserProfileAdmin, self).get_queryset(request)
		if request.user.is_superuser or request.user.userprofile.user_in_banzhu_group():
			return qs
		else:
			return qs.filter(user=request.user)

	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if obj.id == request.user.userprofile.id or not request.user.is_superuser and not request.user.userprofile.user_in_banzhu_group():
			self.exclude = ['qqdisplay','payname','lock_sha256_first','sha256_first', 'lock_sha256_second','sha256_second', 'lock_scrypt_first','scrypt_first','minerid']
		else:
			self.exclude = ['minerid',]
		return super(UserProfileAdmin, self).get_form(request, obj, **kwargs)

	def save_model(self, request, obj, form, change):
		LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note=obj.changenote).save()
		obj.note = obj.changenote
		obj.save()
		obj.changenote = ''
		super(UserProfile,obj).save()

	def save_formset(self, request, form, formset, change):
		instances = formset.save()
		for obj in instances:
			if change:
				LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='用户选择矿工标识').save()

	def get_actions(self, request):
		actions = super(UserProfileAdmin, self).get_actions(request)
		if request.user.is_superuser or request.user.userprofile.user_in_banzhu_group():
			pass
		elif request.user.userprofile.user_in_miner_group():
			del actions['reset_password']
			del actions['add_newuser']
			del actions['confirm_scrypt_first']
			del actions['confirm_sha256_first']
			del actions['confirm_sha256_second']
			del actions['add_into_miners_group']
			del actions['remove_from_miners_group']
		else:
			del actions['reset_minerid']
			del actions['reset_password']
			del actions['add_newuser']
			del actions['confirm_scrypt_first']
			del actions['confirm_sha256_first']
			del actions['confirm_sha256_second']
			del actions['add_into_miners_group']
			del actions['remove_from_miners_group']
		return actions

	def add_newuser(self,request,queryset):
		from django.core.validators import RegexValidator
		class NewUsernameForm(forms.Form):
			qqnumber = forms.CharField(label=_('qqnumber'),required=True,max_length=15,min_length=3,help_text=_('suggest to use the QQ number as username'))
			groups = forms.ModelMultipleChoiceField(label=_('group belongs to'),widget=forms.CheckboxSelectMultiple,queryset=Group.objects.filter(id__lte=3))
		if request.POST.get('post'):
			cform = NewUsernameForm(request.POST)
			message = ""
			if cform.is_valid():
				qqnumber = cform.cleaned_data['qqnumber'].lower()
				groups = cform.cleaned_data['groups']
				str_obj = "( " + qqnumber
				for obj in queryset:
					pass
#				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='密码重置')
#				logrecord.save()
				user,created = User.objects.get_or_create(username=qqnumber)
				if not user.email:
					user.email = qqnumber + "@qq.com"
					user.save()
				try:
					userprofile = UserProfile.objects.get(user=user)
				except UserProfile.DoesNotExist:
					userprofile = UserProfile(user=user)
					userprofile.minerid = random.random() * 100000 + 102000
					userprofile.save()
					LogRecord(target=userprofile,updator=request.user,sha256_first=userprofile.sha256_first,sha256_second=userprofile.sha256_second,scrypt_first=userprofile.scrypt_first,note='新建用户').save()
					user.is_active = False
					user.is_staff = True
					user.save()
					self.message_user(request,"成功创建新用户")
					for g in groups:
						user.groups.add(g)
					self.message_user(request,"成功添加新用户到所选组中")
					return None
				else:
					for g in groups:
						user.groups.add(g)
					self.message_user(request,"你要创建的新用户已经存在")
					self.message_user(request,"成功添加新用户到所选组中")
			else:
				self.message_user(request,"用户名应该在3-15个字母或者数字之间")
		elif request.POST.get('pre'):
			self.message_user(request,"用户创建取消" )
			return None
		else:
			pass
		cform = NewUsernameForm()
		opts= self.model._meta
		context = {
			"title": _("Are you sure?"),
			"object_name": force_unicode(opts.verbose_name),
			'queryset': queryset,
			"opts": opts,
			"form": cform,
			'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
		}
		return render_to_response('add_user.html', context, context_instance=template.RequestContext(request))
	add_newuser.short_description = _("create new user and userprofile")

	def reset_password(self,request,queryset):
		if request.method == 'POST':
			str_obj = "( "
			message = ""
			for obj in queryset:
				user = obj.user
				str_obj += user.username + " " + obj.fullname + " " + obj.qqdisplay + ", "
				user.set_password('0.0T+0.0T')
				user.save()
				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='密码重置')
				logrecord.save()
			self.message_user(request,"password reseted to 0.0T+0.0T for " + str_obj + ')' )
		return None
	reset_password.short_description = _("reset password for selected users")

	def reset_minerid(self,request,queryset):
		if request.method == 'POST':
			str_obj = "( "
			message = ""
			for obj in queryset:
				user = obj.user
				userprofile = user.userprofile
				userprofile.minerid = random.random() * 100000 + 102000
				#userprofile.minerid = 10000
				userprofile.save()
				str_obj += user.username + " " + obj.fullname + " " + obj.qqdisplay + ", "
				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='矿工标识重置')
				logrecord.save()
			self.message_user(request,"矿工标识重置为缺省值10000" )
		return None
	reset_minerid.short_description = "重置矿工标识"

	def add_into_miners_group(self,request,queryset):
		if request.method == 'POST':
			for obj in queryset:
				user = obj.user
				if not Group.objects.get(id=3) in user.groups.all():
					user.groups.add(Group.objects.get(id=3))
					logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='矿工进群')
					logrecord.save()
			self.message_user(request,"选定用户已经加入矿工群")
		return None
	add_into_miners_group.short_description = "选定用户进矿工群"


	def remove_from_miners_group(self,request,queryset):
		if request.method == 'POST':
			for obj in queryset:
				user = obj.user
				if Group.objects.get(id=3) in user.groups.all():
					user.groups.remove(Group.objects.get(id=3))
					logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='矿工退群')
					logrecord.save()
			self.message_user(request,"选定用户已经从矿工群中移出")
		return None
	remove_from_miners_group.short_description = "选定用户退出矿工群"

	def confirm_sha256_first(self,request,queryset):
		if request.method == 'POST':
			str_obj = "( "
			message = ""
			for obj in queryset:
				user = obj.user
				str_obj += user.username + " " + obj.fullname + " " + obj.qqdisplay + ", "
				obj.lock_sha256_first = True
				obj.save()
				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='确认用户一期采购')
				logrecord.save()
			self.message_user(request,"确认用户的一期比特矿机数量正确" )
		return None
	confirm_sha256_first.short_description = _("confirm phase 1 sha256 purchase for selected users")

	def confirm_sha256_second(self,request,queryset):
		if request.method == 'POST':
			str_obj = "( "
			message = ""
			for obj in queryset:
				user = obj.user
				str_obj += user.username + " " + obj.fullname + " " + obj.qqdisplay + ", "
				obj.lock_sha256_second = True
				obj.save()
				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='确认用户二期采购')
				logrecord.save()
			self.message_user(request,"确认用户的二期比特矿机数量正确")
		return None
	confirm_sha256_second.short_description = _("confirm phase 2 sha256 purchase for selected users")

	def confirm_scrypt_first(self,request,queryset):
		if request.method == 'POST':
			str_obj = "( "
			message = ""
			for obj in queryset:
				user = obj.user
				str_obj += user.username + " " + obj.fullname + " " + obj.qqdisplay + ", "
				obj.lock_scrypt_first = True
				obj.save()
				logrecord = LogRecord(target=obj,updator=request.user,sha256_first=obj.sha256_first,sha256_second=obj.sha256_second,scrypt_first=obj.scrypt_first,note='确认莱特币矿机已付款')
				logrecord.save()
			self.message_user(request,"确认用户的一期莱特矿机已付款")
		return None
#	confirm_scrypt_first.short_description = _("confirm phase 1 scrypt purchase for selected users")
	confirm_scrypt_first.short_description = "确认选定用户一期莱特矿机已付款"

class OverseaInfoAdmin(admin.ModelAdmin):
	list_display = ('user','fullname','qqdisplay','location',)
	list_per_page = 20
	list_max_show_all = 3000
	search_fields = ['user__username','qqdisplay','fullname']
#	fields = ['user','fullname','qqdisplay','sha256_first', 'sha256_second', 'scrypt_first', 'changenote']
	readonly_fields = ('user',)
#	form = MyUserProfileForm
#	actions = ['reset_password','confirm_sha256_first','confirm_sha256_second','add_newuser','confirm_scrypt_first']
	list_editable = ('location',)
	readonly_fields = ('sha256_first','sha256_second','sha256_third','scrypt_first','lock_sha256_third','user','wellcoin','hitechfund','lock_sha256_first','lock_sha256_second','lock_scrypt_first','sha256_third','subscription','coinfund','btcwallet','ltcwallet',)

	def has_change_permission(self,request, obj=None):
#		if obj and not ( request.user.is_superuser or request.user.userprofile.user_in_banzhu_group()):
#			return False
#		else:
		return True
	def get_queryset(self, request):
		qs = super(OverseaInfoAdmin, self).get_queryset(request)
#		if request.user.is_superuser or request.user.userprofile.user_in_banzhu_group():
#			return qs
		return qs.filter(user=request.user)

admin.site.register(UserProfile,UserProfileAdmin)
#admin.site.register(UserProfile,OverseaInfoAdmin)
