# Create your views here.
from django.shortcuts import render_to_response
from qqapi.openapi_v3 import OpenAPIV3

def index(request):
	ret = {'hello': 'I am qq_open test.'}
	appid = '1101325568'
	appkey = '5dZxDBFErz0sj3US'
	iplist = ('54.213.74.78',)

	# openid = '0000000000000000000000000039811C'
	# openkey = 'EC88754BBE1ADC64A93EB4432514B84B0CC019F3A2759C8C8'
	openid = request.GET.get('openid')
	openkey = request.GET.get('openkey')

	pf = 'qzone'

	api = OpenAPIV3(appid, appkey, iplist)

	jdata = api.call('/v3/user/get_info', {
		'pf': pf,
		'openid': openid,
		'openkey': openkey
	})
	ret.update({'data': jdata})
	return render_to_response('qq_open/index.html', ret)
