from django.contrib import admin
from userprofiles.models import *
from issues.models import *
#from userprofiles.models import UserProfile as PersonalInfo

# Register your models here.
class JingTianResultAdmin(admin.ModelAdmin):
	list_display = ('miner','timestamp','updated')
	list_per_page = 100
	list_max_show_all = 3000
	list_filter = ('updated',)

class TodoListAdmin(admin.ModelAdmin):
	list_display = ('issuetype','issuewith','fullname','issuesolveby','quantity', 'solved','desc','note')
	list_per_page = 100
	list_max_show_all = 3000
	list_editable = ('note','solved')
	list_filter = ('solved','issuetype',)
	search_fields = ['desc','issuewith__username','issuewith__userprofile__qqdisplay','issuewith__userprofile__fullname']
#	readonly_fields = ('user','wellcoin','hitechfund','scrypt_first','sha256_first','sha256_second','sha256_third','subscription','coinfund')

#	def has_change_permission(self,request, obj=None):
#		if not request.user.is_superuser and obj:
#			return False
#		else:
#			return True
#	def get_queryset(self, request):
#		qs = super(UserProfileAdmin, self).get_queryset(request)
#		if request.user.is_superuser:
#			return qs
#		return qs.filter(user=request.user)
	def save_model(self,request,obj,form,change):
		obj.issuesolveby = request.user
		obj.save()

class LogRecordAdmin(admin.ModelAdmin):
	list_display = ('target','fullname','updator','sha256_first','sha256_second', 'scrypt_first','timestamp','note')
	list_per_page = 100
	list_max_show_all = 3000
	search_fields = ['target__user__username','target__fullname','target__qqdisplay']


admin.site.register(TodoList,TodoListAdmin)
admin.site.register(LogRecord,LogRecordAdmin)
admin.site.register(JingTianResult,JingTianResultAdmin)


# Register your models here.
