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
from django.forms import ModelForm, forms, ModelChoiceField
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
#from django.forms import ValidationError
from django.core.exceptions import ValidationError
from common.functions import superusers_set
from django.contrib.auth.decorators import login_required
import adminfunc
from django.db.models import Q

def message_user(request, message):
	messages.info(request, message)


class CoinfundForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('qqdisplay','coinfund')
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('email',)
class SelectUserForm(forms.Form):
    user = ModelChoiceField(label="select user",queryset=User.objects.filter(is_active=True).order_by('username'),empty_label=None)

class SelectPoolForm(forms.Form):
    pool = ModelChoiceField(label="select pool",queryset=MinerFactory.objects.all(),empty_label=None)

class SelectJingtianWorkerForm(forms.Form):
    jingtianworker = ModelChoiceField(label="select worker",queryset=JintianWorker.objects.filter(is_expired=False),empty_label=None)
#	def clean(self):
#		cleaned_data = super(UserForm,self).clean()
#		if not cleaned_data.get('first_name') or not cleaned_data['last_name']:
#		if self.instance and ( not self.instance.last_name or not self.instance.first_name ):
#			raise ValidationError(_('please input your first_name and last name'),code='required')
#			raise ValidationError('为了方便对帐,请留下姓名信息',code='required')
#		return cleaned_data

def home(request):
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
		if user.userprofile.minerid >= 10000:
			messages.add_message(request, messages.WARNING, '你还没有矿工标识(学号),选择一个并保存,先选先得!')
			return redirect("/django/admin/userprofiles/userprofile/%d/" % request.user.userprofile.id)
		else:
			ucs = UserProfile.objects.exclude(id=user.userprofile.id).filter(minerid=user.userprofile.minerid)
			if ucs:
				messages.add_message(request, messages.WARNING, '你的矿工标识(学号)和' + ucs[0].qqdisplay.encode('utf-8') + '冲突,选择一个或者解决冲突')
				return redirect("/django/admin/userprofiles/userprofile/%d/" % request.user.userprofile.id)
	return render_to_response("home.html", {"user": user, },context_instance=RequestContext(request))

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
			retstring =  "IP address updated"
		except JintianWorker.DoesNotExist:
			retstring = "I do not know you"
	elif ipaddress:
		try:
			worker = JintianWorker.objects.get(ipaddress=ipaddress)
			result,created = JingTianResult.objects.get_or_create(miner=worker)
			if not result.updated:
				result.updated = True
				result.save()
			retstring = "Status updated"
		except JintianWorker.DoesNotExist:
			retstring = "I do not know you"
	return render_to_response("reportback.html")

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

def reporting(request,rformat=None):
	user = User.objects.all()[0]
	try:
		user.userprofile
	except UserProfile.DoesNotExist:
		up = UserProfile(user = user)
		up.save()
	return render_to_response("reports.html", {"uuser":user,},context_instance=RequestContext(request))

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


