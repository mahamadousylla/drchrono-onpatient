# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from User import User
import requests, datetime, pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

BASE_URL = "https://drchrono.com/"
user = None
username = ""

#helper methods
def get_token(code):
	'''takes in code and returns new user'''
	authorization = {
		'code' : code,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://127.0.0.1:8000/home',
    'client_id': 'YmHIOm9TT85ssvANTmxjX0mAqSfbCUX5mQ8tPumW',
    'client_secret': 'T7dLCdvXXvGdvDHMqbIeS8jtuzvyeuvpx72WY4rUK3zs28tpnDahk4RPtQfdNBXK0Gn1fLXer93WFsUBg6TpcROLW7DHl74GqIVfAFlNa5m5myEuhZmhwsAFEVwOrT05',
  }

  # if user:
  # 	code = user.get_code()

  # authorization = {
		# 'code' : code,
  #   'grant_type': 'refresh_token',
  #   'client_id': 'YmHIOm9TT85ssvANTmxjX0mAqSfbCUX5mQ8tPumW',
  #   'client_secret': 'T7dLCdvXXvGdvDHMqbIeS8jtuzvyeuvpx72WY4rUK3zs28tpnDahk4RPtQfdNBXK0Gn1fLXer93WFsUBg6TpcROLW7DHl74GqIVfAFlNa5m5myEuhZmhwsAFEVwOrT05',
  # }
	response = requests.post(BASE_URL + "o/token/", data=authorization)
	response.raise_for_status()
	data = response.json()
 
	# Save these in your database associated with the user
	access_token = data['access_token']
	refresh_token = data['refresh_token']
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

	user = User(code, access_token, refresh_token, expires_timestamp)
	return user

def get_username(user):
	response = requests.get(BASE_URL + 'api/users/current', headers= {
    'Authorization': 'Bearer %s' % user.get_access_token(),
	})

	response.raise_for_status()
	data = response.json()
	return data

def get_patient_data(user):
	headers= {
    'Authorization': 'Bearer ' + user.get_access_token(),
	}

	patients = []
	patients_url = 'https://drchrono.com/api/patients'
	while patients_url:
		data = requests.get(patients_url, headers=headers).json()
		patients.extend(data['results'])
		patients_url = data['next'] # A JSON null on the last page
	return patients


#end of helper methods

#start of views.
def welcome(request):
	return render(request, 'welcome.html')

def home(request):
	global user

	if not user:
		code = request.GET.get('code')
		error = request.GET.get('error')
		print(code, error, user)

		if error: 
			return render(request, 'error.html')

		user = get_token(code)
		data = get_username(user)
		username = data['username']
		user.username = username
		patient_data = sorted(get_patient_data(user), key = lambda d: d["last_name"])
		p_data = Paginator(patient_data, 10)
		
		# page = request.GET.get('page')
		patient_data = p_data.page(1)
		user.patient_data = patient_data
		
		for d in patient_data:
			for k, v in d.items():
				print(k, v)
			print()

	return render(request, 'home.html', {'username': user.username, 'patients': user.patient_data})

def bp(request):
	return render(request, 'bp.html', {'username': username})

def sleep(request):
	return render(request, 'sleep.html', {'username': username})

def weight(request):
	return render(request, 'weight.html', {'username': username})

def hydrate(request):
	return render(request, 'hydrate.html', {'username': username})

def logout(request):
	global user
	user = None
	return render(request, 'index.html', {'username': username})