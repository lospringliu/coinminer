# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import loader, RequestContext, Context
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from userprofiles.models import *
from common.functions import *
from common.models import *
from reports.models import *
from django.forms import ModelForm, forms, ModelChoiceField
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
#from django.forms import ValidationError
from django.core.exceptions import ValidationError
from common.functions import superusers_set
import adminfunc
import json
from issues.models import *
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse

def message_user(request, message):
	messages.info(request, message)

class ConfirmBtcFirstForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','lock_sha256_first','note')
	def clean_fullname(self):
		if not self.cleaned_data.has_key('fullname'):
			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
		return data
	def clean_lock_sha256_first(self):
		data = self.cleaned_data['lock_sha256_first']
		if data == True:
			pass
		elif data == False:
			pass
		else:
			raise ValidationError('请选择是或者否, yes or no; 如果选择否，请留下你的付款名称和二期采购数量',code='required')
		return data
#	def clean_lock_sha256_first(self):
#		data = self.cleaned_data['lock_sha256_first']
#		if data == True:
#			pass
#		elif data == False:
#			pass
#		else:
#			raise ValidationError('请选择是或者否, yes or no, true or false',code='required')
#		return data
#	def clean_note(self):
#		answer = self.cleaned_data['lock_sha256_first']
#		if not self.cleaned_data.has_key('fullname'):
#			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
#		if not self.cleaned_data.has_key('note'):
#			if answer == True:
#				pass
#			elif answer == False:
#				raise ValidationError('为了方便确认,请留下你的付款名称和一期采购数量',code='required')
#			else:
#				raise ValidationError('上面确认正确请选择是或者否',code='required')
#			return ''
#		else:
#			data = self.cleaned_data['note']
#			if answer == True:
#				pass
#			elif answer == False:
#				if len(data) < 3:
#					raise ValidationError('为了方便确认,请留下你的付款名称和一期采购数量',code='required')
#				else:
#					pass
#			else:
#				raise ValidationError('上面确认正确请选择是或者否',code='required')
#			return data

#	def clean_fullname(self):
#		data = self.cleaned_data['fullname']
#		if not data:
#			raise ValidationError('为了方便对帐,请留下姓名/网名信息',code='required')
#		return data
#	def clean(self):
#		cleaned_data = super(ConfirmBtcFirstForm,self).clean()
#		if self.instance and ( not self.instance.fullname or not self.instance.qqdisplay ):
#			raise ValidationError(_('Please leave your full name and nickname for verifications'),code='required')
#			raise ValidationError('为了方便对帐,请留下姓名/网名信息',code='required')
#		return cleaned_data

class ConfirmBtcSecondForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','lock_sha256_second','note')
	def clean_fullname(self):
#		if self.cleaned_data.has_key('fullname'):
#			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
#			return ''
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
		return data
	def clean_lock_sha256_second(self):
		data = self.cleaned_data['lock_sha256_second']
		if data == True:
			pass
		elif data == False:
			pass
		else:
			raise ValidationError('请选择是或者否, yes or no; 如果选择否，请留下你的付款名称和二期采购数量',code='required')
		return data
#	def clean_note(self):
#		answer = self.cleaned_data['lock_sha256_second']
#		data = self.cleaned_data['note']
#		if answer == True:
#			pass
#		if answer == False:
#		if data and len(data) < 3:
#			raise ValidationError('为了方便确认,请留下你的付款名称和二期采购数量',code='required')
#			else:
#				pass
#		else:
#			raise ValidationError('上面确认正确请选择是或者否',code='required')
#		return data

#	def clean_fullname(self):
#		data = self.cleaned_data['fullname']
#		if not data:
#			raise ValidationError('为了方便对帐,请留下姓名/网名信息',code='required')
#		return data
#	def clean(self):
#		cleaned_data = super(ConfirmBtcSecondForm,self).clean()
#		fullname = cleaned_data.get('fullname')
#		if not fullname:
#			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
#			return cleaned_data
#		answer = cleaned_data.get('lock_sha256_second')
#		note = cleaned_data.get('note')
#		if answer == True:
#			return cleaned_data
#		elif answer == False:
#			if not note:
#				raise ValidationError('为了方便确认,请留下你的付款名称和二期采购数量',code='required')
#				return cleaned_data
#			else:
#				if len(note) < 3:
#					raise ValidationError('为了方便确认,请留下你的付款名称和二期采购数量',code='required')
#				return cleaned_data
#		else:
#			raise ValidationError('确认正确请选择是或者否',code='required')
#			return cleaned_data

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','idtype','idnumber','phone','sha256_third_self','wellcoin_self','notewell')
	def clean_fullname(self):
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('井通实名,请留下姓名信息',code='required')
		return data
	def clean_idnumber(self):
		data = self.cleaned_data['idnumber']
		if len(data) < 6:
			raise ValidationError('井通实名,请留下身份信息',code='required')
		return data

class UserProfileFormAfundMiner(ModelForm):
	class Meta:
		model = UserProfile
#		fields = ('fullname','qqdisplay','idtype','idnumber','phone','sha256_third_self','wellcoinact','bitwell','notewell')
		fields = ('qqdisplay','sha256_third_self','wellcoinact','bitwell','swcwallet','notewell')
#	def clean_fullname(self):
#		data = self.cleaned_data['fullname']
#		if len(data) < 2:
#			raise ValidationError('井通实名,请留下姓名信息',code='required')
#		return data
#	def clean_idnumber(self):
#		data = self.cleaned_data['idnumber']
#		if len(data) < 6:
#			raise ValidationError('井通实名,请留下身份信息',code='required')
#		return data
class UserProfileFormAfund(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','idtype','idnumber','phone','sha256_third_self','wellcoinact','notewell')
	def clean_fullname(self):
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('井通实名,请留下姓名信息',code='required')
		return data
	def clean_idnumber(self):
		data = self.cleaned_data['idnumber']
		if len(data) < 6:
			raise ValidationError('井通实名,请留下身份信息',code='required')
		return data
class UserProfileFormMiner(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('qqdisplay','sha256_third_self','wellcoin_self','bitwell','swcwallet','notewell')
#		fields = ('fullname','qqdisplay','idtype','idnumber','phone','sha256_third_self','wellcoin_self','bitwell','notewell')
#	def clean_fullname(self):
#		data = self.cleaned_data['fullname']
#		if len(data) < 2:
#			raise ValidationError('井通实名,请留下姓名信息',code='required')
#		return data
#	def clean_idnumber(self):
#		data = self.cleaned_data['idnumber']
#		if len(data) < 6:
#			raise ValidationError('井通实名,请留下身份信息',code='required')
#		return data

class AstockFundForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','wellcoinact','hitechfundact','coinfundact')
	def clean_fullname(self):
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
		return data

class HitechFundForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fullname','qqdisplay','hitechfund')
	def clean_fullname(self):
		data = self.cleaned_data['fullname']
		if len(data) < 2:
			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
		return data

#	def clean(self):
#		cleaned_data = super(UserProfileForm,self).clean()
#		if self.instance and ( not self.instance.fullname or not self.instance.qqdisplay ):
#			raise ValidationError(_('Please leave your full name and nickname for verifications'),code='required')
##			raise ValidationError('为了方便对帐,请留下姓名/网名信息',code='required')
#		return cleaned_data

class CoinfundForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('qqdisplay','coinfund')
class QqUserForm(ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name')
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('email',)
class SelectUserForm(forms.Form):
    user = ModelChoiceField(label="select user",queryset=User.objects.filter(is_active=True).order_by('username'),empty_label=None)

class SelectPoolForm(forms.Form):
    pool = ModelChoiceField(label="select pool",queryset=MinerFactory.objects.all(),empty_label=None)

class SelectWorkerForm(forms.Form):
    worker = ModelChoiceField(label="select worker",queryset=MinerWorker.objects.filter(is_expired=False),empty_label=None)

class SelectJingtianWorkerForm(forms.Form):
    jingtianworker = ModelChoiceField(label="select worker",queryset=JintianWorker.objects.filter(is_expired=False),empty_label=None)
#	def clean(self):
#		cleaned_data = super(UserForm,self).clean()
#		if not cleaned_data.get('first_name') or not cleaned_data['last_name']:
#		if self.instance and ( not self.instance.last_name or not self.instance.first_name ):
#			raise ValidationError(_('please input your first_name and last name'),code='required')
#			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
#		return cleaned_data

def wallet(request):
	user = request.user
	qs = UserProfile.objects.exclude(swcwallet='').order_by('swcwallet')
	return render_to_response("wallets.html", {"user": user, 'qs':qs})

def wallets(request):
	response = HttpResponse(content_type='text/plain')
	wallets = []
	for up in UserProfile.objects.exclude(swcwallet='').order_by('swcwalletprocessed'):
		wallets.append({'qq':up.user.username, 'wallet':up.swcwallet, 'processed': up.swcwalletprocessed})
	response.write(json.dumps(wallets))
	return response

def home(request):
	user = request.user
#	userprofile = user.userprofile
	passwarn = False
	show_intention = False
	userform = None
	userprofileform = None
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
#	if user and not user.is_anonymous():
#		messages.add_message(request, messages.INFO, '你是周报用户,9月3号前享受井通内部采购价格')
#		if user.userprofile.user_in_miner_group():
#			messages.add_message(request, messages.INFO, '你是矿工群用户,享受矿机补贴和折扣')
#		if user.userprofile.user_in_astockfund_group():
#			messages.add_message(request, messages.INFO, '你是A股基金用户,享受投资补损')
	if request.method == 'GET':
		show_intention = request.GET.get('show_intention')
		if user.userprofile.user_in_miner_group() and user.userprofile.user_in_astockfund_group():
			userprofileform = UserProfileFormAfundMiner(instance=user.userprofile)
		elif user.userprofile.user_in_miner_group():
			userprofileform = UserProfileFormMiner(instance=user.userprofile)
		elif user.userprofile.user_in_astockfund_group():
			userprofileform = UserProfileFormAfund(instance=user.userprofile)
		else:
			userprofileform = UserProfileForm(instance=user.userprofile)
	if request.method == 'POST':
		if user.userprofile.user_in_miner_group() and user.userprofile.user_in_astockfund_group():
			userprofileform = UserProfileFormAfundMiner(request.POST, request.FILES, instance=user.userprofile)
		elif user.userprofile.user_in_miner_group():
			userprofileform = UserProfileFormMiner(request.POST, request.FILES, instance=user.userprofile)
		elif user.userprofile.user_in_astockfund_group():
			userprofileform = UserProfileFormAfund(request.POST, request.FILES, instance=user.userprofile)
		else:
			userprofileform = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
		if userprofileform.is_valid():
			userprofileform.save()
			return HttpResponseRedirect("/django/")
		else:
			show_intention = True
	return render_to_response("home.html", {"user": user, "show_intention": show_intention, "userprofileform":userprofileform, },context_instance=RequestContext(request))

def homeminer(request):
	user = request.user
	passwarn = False
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	if user and not user.is_anonymous() and user.userprofile.need_confirm_btcpurchase():
		if user.userprofile.lock_sha256_first == None:
			messages.add_message(request, messages.WARNING, '还没有确认你的一期比特矿机购买，现在就确认吧!如果数量不对，记得提供付款姓名和数量')
			return redirect("/django/confirm_btc_first/")
		if user.userprofile.lock_sha256_second == None:
			messages.add_message(request, messages.WARNING, '还没有确认你的二期比特矿机购买，现在就确认吧!如果数量不对，记得提供付款姓名和数量')
			return redirect("/django/confirm_btc_second/")
#		if user.userprofile.minerid >= 10000:
#			messages.add_message(request, messages.WARNING, '你还没有矿工标识(学号),选择一个并保存,先选先得!')
#			return redirect("/django/admin/userprofiles/userprofile/%d/" % request.user.userprofile.id)
#		else:
#			ucs = UserProfile.objects.exclude(id=user.userprofile.id).filter(minerid=user.userprofile.minerid)
#			if ucs:
#				messages.add_message(request, messages.WARNING, '你的矿工标识(学号)和' + ucs[0].qqdisplay.encode('utf-8') + '冲突,选择一个或者解决冲突')
#				return redirect("/django/admin/userprofiles/userprofile/%d/" % request.user.userprofile.id)
	return render_to_response("homeminer.html", {"user": user, },context_instance=RequestContext(request))

def reportback(request):
	ipaddress = request.GET.get('ipaddress')
	macaddress = request.GET.get('macaddress')
	worker = None
	if ipaddress and macaddress:
		try:
			worker = JintianWorker.objects.get(macaddress=macaddress)
			result,created = JingTianResult.objects.get_or_create(miner=worker)
			if not result.updated:
				result.updated = True
				result.save()
			if worker.ipaddress != ipaddress:
				worker.ipaddress = ipaddress
				worker.save()
			return "IP address updated"
		except JintianWorker.DoesNotExist:
			pass
	elif ipaddress:
		try:
			worker = JintianWorker.objects.get(ipaddress=ipaddress)
			result,created = JingTianResult.objects.get_or_create(miner=worker)
			if not result.updated:
				result.updated = True
				result.save()
			return "Status updated"
		except JintianWorker.DoesNotExist:
			pass
#	return render_to_response("reportback.html", { "worker":worker })

def trjtminer(request):
	user = request.user
	minerid = request.GET.get('minerid')
	if minerid:
		miner = JintianWorker.objects.get(id=int(minerid))
	return render_to_response("trjtminer.html", {"user": user, "miner":miner },context_instance=RequestContext(request))

def jtminer(request):
	user = request.user
	minerid = request.GET.get('minerid')
	if minerid:
		miner = JintianWorker.objects.get(id=int(minerid))
	return render_to_response("apidata.html", {"user": user, "miner":miner },context_instance=RequestContext(request))

def tutorial(request):
	user = request.user
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	return render_to_response("tutorial.html", {"user": user, },context_instance=RequestContext(request))

def controlpanel(request):
	user = request.user
	passwarn = False
	show_hitechfund_result = False
	show_ltc_result = False
	show_btcfirst_result = False
	show_btcsecond_result = False
	show_btcthird_result = False
	show_oversea_result = False
	switch_superuser = False
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	if request.method == 'GET':
		switch_superuser = request.GET.get('switch_superuser')
		show_hitechfund_result = request.GET.get('show_hitechfund_result')
		show_ltc_result = request.GET.get('show_ltc_result')
		show_btcfirst_result = request.GET.get('show_btcfirst_result')
		show_btcsecond_result = request.GET.get('show_btcsecond_result')
		show_btcthird_result = request.GET.get('show_btcthird_result')
		show_oversea_result = request.GET.get('show_oversea_result')
		if switch_superuser and user.username in superusers_set:
			if user.is_superuser:
				user.is_superuser = False
				user.save()
			else:
				user.is_superuser = True
				user.save()
	return render_to_response("controlpanel.html", {"user": user, "show_hitechfund_result":show_hitechfund_result,"switch_superuser":switch_superuser,"show_ltc_result":show_ltc_result,"show_btcfirst_result":show_btcfirst_result,"show_btcsecond_result":show_btcsecond_result,"show_btcthird_result":show_btcthird_result,"show_oversea_result":show_oversea_result},context_instance=RequestContext(request))

def htcbooking(request):
	user = request.user
	passwarn = False
	show_hitechfund_result = False
	switch_superuser = False
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	userform = UserForm(instance=user)
	userprofileform = HitechFundForm(instance=user.userprofile)
	if request.method == 'GET':
		switch_superuser = request.GET.get('switch_superuser')
		show_hitechfund_result = request.GET.get('show_hitechfund_result')
		if switch_superuser and user.username in superusers_set:
			if user.is_superuser:
				user.is_superuser = False
				user.save()
			else:
				user.is_superuser = True
				user.save()
	if request.method == 'POST':
		userform = UserForm(request.POST, request.FILES, instance=user)
		userprofileform = HitechFundForm(request.POST, request.FILES, instance=user.userprofile)
		if userform.is_valid() and userprofileform.is_valid():
#			userform.save()
			userprofileform.save()
			userprofile = user.userprofile
			userprofile.confirmed = True
			userprofile.save()
			return HttpResponseRedirect("/django/")
		else:
			show_intention_hitech = True
	return render_to_response("home.html", {"user": user, "show_intention_hitech":True,"userform":userform, "userprofileform":userprofileform,"switch_superuser":switch_superuser,"show_hitechfund_result":show_hitechfund_result,},context_instance=RequestContext(request))

def ltcbooking(request):
	user = request.user
	passwarn = False
	switch_superuser = False
	show_btcthird_result = False
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	userform = UserForm(instance=user)
	userprofileform = UserProfileForm(instance=user.userprofile)
	if request.method == 'GET':
		switch_superuser = request.GET.get('switch_superuser')
		show_btcthird_result = request.GET.get('show_btcthird_result')
		if switch_superuser and user.username in superusers_set:
			if user.is_superuser:
				user.is_superuser = False
				user.save()
			else:
				user.is_superuser = True
				user.save()
	if request.method == 'POST':
		userform = UserForm(request.POST, request.FILES, instance=user)
		userprofileform = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
		if userform.is_valid() and userprofileform.is_valid():
#			userform.save()
			userprofileform.save()
			return HttpResponseRedirect("/django/")
		else:
			show_intention = True
	return render_to_response("home.html", {"user": user, "show_intention":True,"userform":userform, "userprofileform":userprofileform,"switch_superuser":switch_superuser,"show_btcthird_result":show_btcthird_result,},context_instance=RequestContext(request))

def confirm_btc_first(request):
	user = request.user
	passwarn = False
	confirm_btc_first = True
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	userform = UserForm(instance=user)
	userprofileform = ConfirmBtcFirstForm(instance=user.userprofile)
	if request.method == 'GET':
		if user.userprofile.lock_sha256_first == False:
			message_user(request, "你已经确认过一期采购数目不正确,请耐心等候处理")
			return redirect("/django/")
	if request.method == 'POST':
		userform = UserForm(request.POST,instance=user)
		userprofileform = ConfirmBtcFirstForm(request.POST,instance=user.userprofile)
		if userform.is_valid() and userprofileform.is_valid():
#			userform.save()
			userprofileform.save()
			up = userprofileform.instance
			if up.lock_sha256_first == False:
				tl = TodoList(issuewith=user,issuetype=IssueType.objects.get(id=4),quantity=str(up.sha256_first),desc=up.note,note='用户确认有误')
				tl.save()
			return HttpResponseRedirect("/django/")
		else:
			confirm_btc_first = True
	return render_to_response("homeminer.html", {"user": user, "confirm_btc_first":True,"userbtcfirstform":userform, "userprofilebtcfirstform":userprofileform,},context_instance=RequestContext(request))

def confirm_btc_second(request):
	user = request.user
	passwarn = False
	confirm_btc_second = True
	if user and user.is_anonymous():
		return redirect("/django/accounts/login/")
	if user and not user.is_anonymous() and user.check_password("0.0T+0.0T"):
		messages.add_message(request, messages.WARNING, '请立刻修改你的密码,不要使用你的QQ密码!')
		return redirect("/django/accounts/password_change/")
	userform = UserForm(instance=user)
	userprofileform = ConfirmBtcSecondForm(instance=user.userprofile)
	if request.method == 'GET':
		if user.userprofile.lock_sha256_second == False:
			message_user(request, "你已经确认过二期采购数目不正确,请耐心等候处理")
			return redirect("/django/")
	if request.method == 'POST':
		userform = UserForm(request.POST,instance=user)
		userprofileform = ConfirmBtcSecondForm(request.POST,instance=user.userprofile)
		if userform.is_valid() and userprofileform.is_valid():
#			userform.save()
			userprofileform.save()
			up = userprofileform.instance
			if up.lock_sha256_second == False:
				tl = TodoList(issuewith=user,issuetype=IssueType.objects.get(id=5),quantity=str(up.sha256_second),desc=up.note,note='用户确认有误')
				tl.save()
			return HttpResponseRedirect("/django/")
		else:
			confirm_btc_second = True
	return render_to_response("homeminer.html", {"user": user, "confirm_btc_second":True,"userbtcsecondform":userform, "userprofilebtcsecondform":userprofileform,},context_instance=RequestContext(request))

@login_required()
def reporting(request,rformat=None):
	return render_to_response("reports.html", {"user":request.user,},context_instance=RequestContext(request))

@login_required()
def available_minerids(request):
	matrix = dict()
	changeline = [0,]
	MAXID = UserProfile.objects.filter(user__groups=Group.objects.get(id=3)).exclude(user__username__startswith='client').count() + 1
	for idind in range(1,MAXID):
		matrix[idind] = True
		if idind % 10 == 0:
			changeline.append(idind)
	for up in UserProfile.objects.filter(user__groups=Group.objects.get(id=3)).exclude(user__username__startswith='client').exclude(minerid__gte=10000):
		matrix[up.minerid] = False
	return render_to_response("minerids.html", {"user":request.user,'matrix':matrix,'changeline':changeline},context_instance=RequestContext(request))

@login_required()
def charts(request):
	from django.contrib.contenttypes.models import ContentType
	modelname = ""
	instancename = ""
	jqplots = []
	requestuser = request.user
	ct = None
	mmodel = None
	autocharts = None
	modelform = None
	if request.method == 'GET':
		modelname=request.GET.get('model')
		instancename=request.GET.get('name')
	elif request.method == 'POST':
		poolform = SelectPoolForm(request.POST)
		workerform = SelectWorkerForm(request.POST)
		jingtianworkerform = SelectJingtianWorkerForm(request.POST)
		userform = SelectUserForm(request.POST)
		if poolform.is_valid():
			modelname = 'MinerFactory'
			pool = poolform.cleaned_data['pool']
			jqplots = pool.gen_charts()
			modelform = SelectPoolForm()
		elif workerform.is_valid():
			modelname = 'MinerFactory'
			worker = workerform.cleaned_data['worker']
			jqplots = worker.gen_charts()
			modelform = SelectWorkerForm()
		elif jingtianworkerform.is_valid():
			modelname = 'JintianFactory'
			jingtianworker = jingtianworkerform.cleaned_data['jingtianworker']
			jqplots = jingtianworker.gen_charts()
			modelform = SelectJingtianWorkerForm()
		elif userform.is_valid():
			modelname = 'User'
			tuser = userform.cleaned_data['user']
			if tuser.userprofile:
				jqplots = tuser.userprofile.gen_charts()
			modelform = SelectUserForm()
		else:
			pass
		try:
			ct = ContentType.objects.get(model=modelname)
			mmodel = ct.model_class()
		except ContentType.DoesNotExist:
			pass
		return render_to_response("charts.html", {"user":requestuser, "model": mmodel, 'contenttype': ct, 'jqplots': jqplots, 'modelform': modelform, }, context_instance=RequestContext(request))
	try:
		ct = ContentType.objects.get(model=modelname)
		mmodel = ct.model_class()
		if mmodel == MinerFactory:
			modelform = SelectPoolForm()
			jqplots = requestuser.userprofile.gen_pool_charts()
		elif mmodel == MinerWorker:
			modelform = SelectWorkerForm()
			jqplots = requestuser.userprofile.gen_bad_workers_charts()
		elif mmodel == JintianWorker:
			modelform = SelectJingtianWorkerForm()
			jqplots = requestuser.userprofile.gen_bad_jtworkers_charts()
		elif mmodel == BitStamp:
			jqplots = requestuser.userprofile.gen_bitstamp_charts()
		elif mmodel == User:
			modelform = SelectUserForm()
			jqplots = requestuser.userprofile.gen_user_charts()
	except ContentType.DoesNotExist:
		pass
	if modelname == 'MinerWorker':
		if instancename:
			instance = MinerWorker.objects.get(name=instancename)
			jqplots = instance.gen_charts()
	if modelname == 'JintianWorker':
		if instancename:
			instance = JintianWorker.objects.get(name=instancename)
			jqplots = instance.gen_charts()
	if modelname == 'MinerFactory':
		if instancename:
			instance = MinerFactory.objects.get(name=instancename)
			jqplots = instance.gen_charts()
	if not requestuser.is_anonymous() and requestuser.userprofile:
		return render_to_response("charts.html", {"user":requestuser, "model": mmodel, 'contenttype': ct, 'jqplots': jqplots, 'modelform': modelform, }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/django/charts/")


def gen_btc_result(request):
	response = HttpResponse(content_type='text/plain;charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename="btc_purchase_result.tabseprated"'
	user = request.user
	if not Group.objects.get(id=6) in user.groups.all() and not user.username in superusers_set:
		return HttpResponse(content="只有版主和超级用户可以下载账本",content_type='text/plain;charset=utf-8')
	for up in UserProfile.objects.filter(user__groups=Group.objects.get(id=3)).filter(Q(sha256_first__gt=Decimal('0.00')) | Q(sha256_second__gt=Decimal('0.0'))).order_by('payname'):
		response.content += up.user.username.encode('utf-8') + '\t' + up.payname.encode('utf-8') + '\t' + up.qqdisplay.encode('utf-8') + '\t' + re.sub('E\+1','0',str(up.sha256_first.normalize())) + '\t' + re.sub('E\+1','0',str(up.sha256_second.normalize())) + '\t' + re.sub('E\+1','0',str((up.sha256_first + up.sha256_second).normalize())) + '\n'
	return response


def afundinvest(request):
	user = request.user
	show_invest_result = False
	show_intention = False
	userform = None
	userprofileform = None
	summs = UserProfile.objects.all()[0].get_sum_queryset_astockfund()
	if user and user.is_anonymous():
		loggedin = False
		return redirect("/django/accounts/login/?next=/django/afundinvest/")
	else:
		loggedin = True
		userprofileform = AstockFundForm(instance=user.userprofile)
	if request.method == 'GET':
		show_intention = request.GET.get('show_intention')
		show_invest_result = request.GET.get('show_invest_result')
	if request.method == 'POST':
		userprofileform = AstockFundForm(request.POST, request.FILES, instance=user.userprofile)
		if userprofileform.is_valid():
			userprofileform.save()
			return HttpResponseRedirect("/django/afundinvest/?show_invest_result=True")
		else:
			show_intention = True
	if not user.userprofile.wellcoinact:
		show_intention = True
	return render_to_response("afund.html", {"loggedin": loggedin, "user": user, "show_intention":show_intention, "userprofileform":userprofileform,"show_invest_result":show_invest_result,'astockfund':summs['astockfund__sum'],'astockvalue':summs['astockvalue__sum'],'astockcredit':summs['astockcredit__sum']},context_instance=RequestContext(request))
def afundresult(request):
	user = request.user
	summs = UserProfile.objects.all()[0].get_sum_queryset_astockfund()
	if user and user.is_anonymous():
		loggedin = False
		return redirect("/django/accounts/login/?next=/django/afundresult/")
	else:
		loggedin = True
		userprofileform = AstockFundForm(instance=user.userprofile)
	return render_to_response("afundresult.html", {"loggedin": loggedin, "user": user, 'astockfund':summs['astockfund__sum'],'wellcoin':summs['wellcoin__sum'],'hitechfund':summs['hitechfund__sum'],'coinfund':summs['coinfund__sum'],'astockvalue':summs['astockvalue__sum'],'astockcredit':summs['astockcredit__sum'],'wellcoinact':summs['wellcoinact__sum'],'hitechfundact':summs['hitechfundact__sum'],'coinfundact':summs['coinfundact__sum'],},context_instance=RequestContext(request))

def qqhome(request):
	user = request.user
	if user and user.is_anonymous():
		return redirect(reverse('denglu'))
	if request.method == 'GET':
		userform = QqUserForm(instance=user)
	if request.method == 'POST':
		userform = QqUserForm(request.POST,instance=user)
		if userform.is_valid():
			userform.save()
	return render_to_response("thirdauth/home.html", {"user": user, "form":userform, },context_instance=RequestContext(request))

def denglu(request):
	user = request.user
	if request.method == 'POST':
		authform = AuthenticationForm(request, data=request.POST)
		if authform.is_valid():
			auth_login(request, authform.get_user())
			return redirect(reverse('qqhome'))
	else:
		authform = AuthenticationForm(request)
	return render_to_response("thirdauth/denglu.html", {"user": user , "form": authform, },context_instance=RequestContext(request))

