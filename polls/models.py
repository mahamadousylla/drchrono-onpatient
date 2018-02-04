# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Patient:
	def __init__(self, code, access_token, refresh_token, expires_timestamp):
		self.code = code
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.expires_timestamp = expires_timestamp

	def get_code(self):
		return self.code

	def get_access_token(self):
		return self.access_token

	def get_refresh_token(self):
		return self.refresh_token

	def get_expires_timestamp(self):
		return self.expires_timestamp

	def set_code(self, code):
		self.code = code


class PatientID(models.Model):
	app_label = "patient"
	id = models.IntegerField(primary_key=True)