# -*- coding: utf-8 -*-
from django.contrib import admin
from common.models import *
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django import http, template
import re

class LocationAdmin(admin.ModelAdmin):
	readonly_fields = ('parent',)

class JingtianWorkerAdmin(admin.ModelAdmin):
	list_display = ('ipaddress','hr_5','pool_reject_ratio','device_reject_ratio','asc0','asc1','asc2','asc3','asc4','details')
#	exclude = ['is_expired',]
	list_per_page = 50
	list_max_show_all = 3000
	list_filter = ('factory','is_expired')
	search_fields = ['name','ipaddress']
	readonly_fields = ['wu','hr_5','asc0','asc0_cores','asc0_temp','asc1','asc1_cores','asc1_temp','asc2','asc2_cores','asc2_temp','asc3','asc3_cores','asc3_temp','asc4','asc4_cores','asc4_temp']
	actions = [ 'show_api_data', ]
	ordering = ('hr_5',)

	def has_change_permission(self,request, obj=None):
		if obj and not ( request.user.is_superuser or request.user.userprofile.user_in_banzhu_group()):
			return False
		elif not request.user.userprofile.user_in_miner_group() and not request.user.userprofile.user_in_pool_admin_group():
			return False
		else:
			return True
	def show_api_data(self,request,queryset):
		if request.method == 'POST':
			if queryset.count() < 11 and queryset.count() > 0:
				return render_to_response("apidata.html", {"user": request.user,'queryset':queryset },context_instance=template.RequestContext(request))
		return None
	show_api_data.short_description = "显示选定矿工的详细信息"


class MinerWorkerAdmin(admin.ModelAdmin):
	list_display = ('name','factory','hr_225','hr_300','hr_120','history','visualize')
	list_per_page = 500
	list_max_show_all = 3000
	list_filter = ('factory',)
	search_fields = ['name',]

class ShareResourceAdmin(admin.ModelAdmin):
	list_display = ('name','resourcetype','link_in_web','provider','description')
	list_per_page = 500
	list_max_show_all = 3000
	list_filter = ('resourcetype',)
	search_fields = ['name','provider__username','provider__userprofile__qqdisplay']
	readonly_fields = ['provider',]

	def has_change_permission(self,request, obj=None):
		if request.user.is_superuser:
			return True
		elif not obj:
			return True
		else:
			if obj.provider == request.user:
				return True
			else:
				return False
	def save_model(self,request,obj,form,change):
		user = request.user
		obj.provider = user
		obj.save()
class MinerFactoryAdmin(admin.ModelAdmin):
	list_display = ('name','blocks','coins','coinspending','hr_128','hr_256','hr_225','history','visualize')
	list_per_page = 500
	list_max_show_all = 3000
	search_fields = ['name',]

#	def get_queryset(self, request):
#		qs = super(UserProfileAdmin, self).get_queryset(request)
#		if request.user.is_superuser:
#			return qs
#		return qs.filter(user=request.user)
# Register your models here.
admin.site.register(Country)
admin.site.register(IssueType)
admin.site.register(IdType)
admin.site.register(ResourceType)
admin.site.register(CoinType)
admin.site.register(Province)
admin.site.register(BtcFund)
admin.site.register(Location,LocationAdmin)
admin.site.register(Subscription)
admin.site.register(TransferContent)
admin.site.register(MinerFactory,MinerFactoryAdmin)
admin.site.register(JintianWorker,JingtianWorkerAdmin)
admin.site.register(MinerWorker,MinerWorkerAdmin)
admin.site.register(ShareResource,ShareResourceAdmin)
