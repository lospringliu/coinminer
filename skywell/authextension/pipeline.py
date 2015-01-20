from django.shortcuts import redirect
from django.contrib.auth.models import User

from social.pipeline.partial import partial
import re


@partial
def require_info(strategy, details, user=None, is_new=False, *args, **kwargs):
	if user and user.email and ( user.username == 'guest' or re.match(r'^[1-9][0-9]+@qq.com$',user.email)):
		details['email'] = user.email
		username = user.username
		return {'details': details, 'username': username}
	elif details.get('email') and  re.match(r'^[1-9][0-9]+@qq.com$',details['email']):
		username =  re.sub(r'\@.*','',details['email'])
		if not User.objects.filter(username=username):
			username = 'guest'
		return {'details': details, 'username': username}
	else:
		pass
	email = strategy.request_data().get('email')
	if email and re.match(r'^[1-9][0-9]+@qq.com$',email):
		details['email'] = email
		username =  re.sub(r'\@.*','',email)
		if not User.objects.filter(username=username):
			username = 'guest'
		return {'details': details, 'username': username}
	else:
		return redirect('require_info')

@partial
def user_by_email(backend, details, *args, **kwargs):
	request_data = backend.strategy.request_data()
	if request_data.get('verification_code') and details.get('email'):
		try:
			user = User.objects.get(email=details['email'])
			return {'user': user}
		except User.DoesNotExist:
			username = 'guest'
#			details['email'] = 'guest@qq.com'
			user,created = User.objects.get_or_create(username=username)
			return {'user': user,'details': details, 'username': username}
	else:
		try:
			user = User.objects.get(email=details['email'])
			return {'user': user}
		except User.DoesNotExist:
			username = 'guest'
#			details['email'] = 'guest@qq.com'
			user,created = User.objects.get_or_create(username=username)
			return {'user': user,'details': details, 'username': username}
