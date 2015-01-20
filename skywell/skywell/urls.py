from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.list import ListView
from userprofiles.models import UserProfile
from social.apps.django_app.default.models import UserSocialAuth

from django.contrib import admin
admin.autodiscover()
admin.site.disable_action('delete_selected')

from userprofiles.adminsite import UserSocialAuthOption, UserProfileAdminSite, UserProfileAdmin
userprofileadminsite = UserProfileAdminSite(name='userprofileadminsite')
userprofileadminsite.disable_action('delete_selected')
userprofileadminsite.register(UserProfile,UserProfileAdmin)
userprofileadminsite.register(UserSocialAuth,UserSocialAuthOption)
#from social.apps.django_app.default.models import UserSocialAuth
#from social.apps.django_app.default.admin import UserSocialAuthAdmin

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'skywell.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^$', 'skywell.views.home', name='home'),
	url (r'^wallet', 'skywell.views.wallet', name="wallet"),
	url (r'^wallets', 'skywell.views.wallets', name="wallets"),
	url(r'^homeminer/', 'skywell.views.homeminer', name='homeminer'),
#	url(r'^htcbooking/', 'skywell.views.htcbooking'),
#	url(r'^ltcbooking/', 'skywell.views.ltcbooking'),
	url(r'^confirm_btc_first/', 'skywell.views.confirm_btc_first',name='confirm_btc_first'),
	url(r'^confirm_btc_second/', 'skywell.views.confirm_btc_second',name='confirm_btc_second'),
	url(r'^gen_btc_result/', 'skywell.views.gen_btc_result',name='gen_btc_result'),
	url(r'^reports/', 'skywell.views.reporting',name='reports'),
	url(r'^reportback/', 'skywell.views.reportback'),
	url(r'^availableminerids/', 'skywell.views.available_minerids', name='minerid'),
	url(r'^charts/', 'skywell.views.charts', name='charts'),
	url(r'^controlpanel/', 'skywell.views.controlpanel',name='controlpanel'),
	url(r'^afundinvest/', 'skywell.views.afundinvest',name='homeafund'),
	url(r'^afundresult/', 'skywell.views.afundresult',name='afuncresult'),
	url(r'^tutorial/', 'skywell.views.tutorial',name='tutorial'),
#	url(r'^jtminer/', 'skywell.views.jtminer'),
#	url(r'^trjtminer/', 'skywell.views.trjtminer'),
	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^qq_open/', include('qq_open.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adminup/', include(userprofileadminsite.urls)),
	url(r'^socialhome/', 'authextension.views.home', name='socialhome'),
	url(r'^sociallogout/$', 'authextension.views.logout',name='sociallogout'),
	url(r'^socialdone/$', 'authextension.views.done',name='socialdone'),
	url(r'^require_info/$', 'authextension.views.require_info', name='require_info'),
	url(r'^email-sent/', 'authextension.views.validation_sent',name='validation_sent'),
	url(r'^denglu/', 'skywell.views.denglu', name='denglu'),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('django.contrib.auth.urls', namespace='qqauth')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

