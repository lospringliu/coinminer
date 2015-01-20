 #!/usr/bin/python
# -*- coding: utf-8 -*-

'''
#=============================================================================
#
#     FileName: openapi_v3.py
#         Desc: OpenAPI V3的API
#
#       Author: open.qq.com
#
#      Created: 2011-10-19 09:53:33
#      Version: 3.0.0
#      History:
#               3.0.0 | dantezhu | 2011-10-19 09:53:33 | initialization
#
#=============================================================================
'''

import copy
import json

from sns_network import SNSNetwork

OPEN_HTTP_TRANSLATE_ERROR = 2001

class OpenAPIV3(object):
    _appid = 0
    _appkey = ''
    _api = None

    def __init__(self, appid, appkey, iplist):
        super(OpenAPIV3, self).__init__()
        self._appid = appid
        self._appkey = appkey

        secret = '%s&' % self._appkey
        self._api = SNSNetwork(secret, iplist)

    def call(self, url_path, params, method='post', protocol='http'):
        '''
        调用接口，并将数据格式转化成json
        只需要传入pf, openid, openkey等参数即可，不需要传入sig
        format即使传xml也没有用，会被强制改为json
        '''
        cp_params = copy.deepcopy(params)
        cp_params.update(
            {
                'appid': self._appid,
                'format': 'json'
            }
            )

        try:
            data = self._api.open(method, url_path, cp_params, protocol)
        except Exception, e:
            msg = 'exception occur.msg[%s], traceback[%s]' % (str(e), __import__('traceback').format_exc())
            return {'ret':OPEN_HTTP_TRANSLATE_ERROR, 'msg':msg}
        else:
            return json.loads(data)


def main():
    appid = 600
    appkey = 'your appkey'
    iplist = ('172.27.0.91',)

    openid = '0000000000000000000000000039811C'
    openkey = 'EC88754BBE1ADC64A93EB4432514B84B0CC019F3A2759C8C8'

    pf = 'qzone'

    api = OpenAPIV3(appid, appkey, iplist)

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    print jdata


if __name__ == '__main__':
    main()
