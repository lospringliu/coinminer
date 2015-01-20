#-*- coding: utf-8 -*-
__author__ = 'Xinchun Liu'

from django.conf.urls import url,patterns

urlpatterns = patterns('qq_open.views',
    url(r'^$', 'index'),
	)
