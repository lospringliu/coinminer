from django.contrib import admin
from reports.models import *
from common.models import *

# Register your models here.
class ReportByFactoryAdmin(admin.ModelAdmin):
	date_hierarchy = 'reportdate'
	list_display = ('factory','reporttime','blocks','coins','coinspending','hr_128','hr_256','hr_225',)
	list_per_page = 100
	list_filter = ('factory',)
	list_max_show_all = 3000
	search_fields = ['factory__name',]

	def has_change_permission(self,request, obj=None):
		if not request.user.is_superuser and obj:
			return False
		else:
			return True
class ReportByWorkerAdmin(admin.ModelAdmin):
	date_hierarchy = 'reportdate'
	list_display = ('worker','reporttime','hr_225','hr_300','hr_120',)
	list_per_page = MinerWorker.objects.all().count()
	list_filter = ('worker__factory','worker')
	list_max_show_all = 3000
	search_fields = ['worker__name',]

	def has_change_permission(self,request, obj=None):
		if not request.user.is_superuser and obj:
			return False
		else:
			return True
#	def get_queryset(self, request):
#		qs = super(UserProfileAdmin, self).get_queryset(request)
#		if request.user.is_superuser:
#			return qs
#		return qs.filter(user=request.user)
admin.site.register(ReportByWorker,ReportByWorkerAdmin)
admin.site.register(ReportByFactory,ReportByFactoryAdmin)
