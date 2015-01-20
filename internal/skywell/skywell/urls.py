from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()
admin.site.disable_action('delete_selected')

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'skywell.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^$', 'skywell.views.reporting', name='home'),
	url(r'^reports/', 'skywell.views.reporting'),
	url(r'^reportback/', 'skywell.views.reportback'),
	url(r'^jtminer/', 'skywell.views.jtminer'),
	url(r'^trjtminer/', 'skywell.views.trjtminer'),
	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

