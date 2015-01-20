# -*- coding: utf-8 -*-
from django.contrib import admin
from common.models import *
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django import http, template
import re

class JingtianWorkerAdmin(admin.ModelAdmin):
	list_display = ('ipaddress','wu','hr_5','pool_reject_ratio','wallet','asc0','asc1','asc2','asc3','asc4','details')
#	exclude = ['is_expired',]
	list_per_page = 50
	list_max_show_all = 3000
	list_filter = ('factory','wallet','is_expired')
	search_fields = ['name','ipaddress']
	readonly_fields = ['wu','hr_5','asc0','asc0_cores','asc0_temp','asc1','asc1_cores','asc1_temp','asc2','asc2_cores','asc2_temp','asc3','asc3_cores','asc3_temp','asc4','asc4_cores','asc4_temp']
	actions = [ 'show_api_data', ]
	ordering = ('hr_5',)

	def show_api_data(self,request,queryset):
		if request.method == 'POST':
			if queryset.count() < 11 and queryset.count() > 0:
				return render_to_response("apidata.html", {"user": request.user,'queryset':queryset },context_instance=template.RequestContext(request))
		return None
	show_api_data.short_description = "显示选定矿工的详细信息"


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
admin.site.register(CoinType)
admin.site.register(Wallet)
admin.site.register(MinerFactory,MinerFactoryAdmin)
admin.site.register(JintianWorker,JingtianWorkerAdmin)
