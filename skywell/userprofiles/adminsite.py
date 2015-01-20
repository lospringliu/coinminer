from django.contrib import admin
from django.contrib.auth.models import User
from userprofiles.models import UserProfile
from django.conf import settings
from social.utils import setting_name
from social.apps.django_app.default.models import UserSocialAuth

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','swcwallet','swcwalletprocessed','qqdisplay')
	list_editable = ('swcwalletprocessed',)
	save_on_top = True
	def queryset(self,request):
		return super(UserProfileAdmin,self).queryset(request).exclude(swcwallet='')
	def has_change_permission(self,request,obj=None):
		if obj:
			return False
		if request.user.is_superuser or request.user.username == '15089476' or request.user.username == '369810162':
			return True
		else:
			return False
	def has_delete_permission(self, request,obj=None):
		return False
	def has_add_permission(self, request,obj=None):
		return False

class UserSocialAuthOption(admin.ModelAdmin):
	list_display = ('id', 'user', 'provider', 'uid')
	raw_id_fields = ('user',)
	readonly_fields = ('id','user','provider', 'uid','extra_data')
	list_select_related = True
	def queryset(self,request):
		return super(UserSocialAuthOption,self).queryset(request).filter(user=request.user)
	def has_change_permission(self,request,obj=None):
		return True
	def has_delete_permission(self, request,obj=None):
		return True
	def has_add_permission(self, request,obj=None):
		return False

class UserProfileAdminSite(admin.sites.AdminSite):
	pass
	def has_permission(self, request):
		"""
		Returns True if the given HttpRequest has permission to view
		*at least one* page in the admin site.
		"""
		return request.user.is_active
