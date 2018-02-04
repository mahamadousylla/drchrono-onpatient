# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from models import Patient, PatientID
import requests, datetime, pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

URL_CHRONO = "https://drchrono.com/"
URL_ONPATIENT = "https://onpatient.com/"
CLIENT_ID = "YBWQ0HSOpwpumbLjqj83J6UMFqVsyqrG9uJ4Yrpz"
CLIENT_SECRET = "RGocYqR3RWZXoc5C8FUf788boz3ZoBWpmudkoiHBCS4VR9c3LfoZ6BufBx5ZW7OkN889rVLhBy8jAIsuDfnTGYnquB7b9jH8CaKBsh5QvJo2OmmkugVFesrjBUyzWj9d"
patient = None
username = ""

#helper methods
def get_token(code):
	'''takes in code and returns new patient'''
	authorization = {
		'code' : code,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://127.0.0.1:8000/home',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
  }

	response = requests.post(URL_ONPATIENT + "o/token/", data=authorization)
	response.raise_for_status()
	data = response.json()
 
	# Save these in your database associated with the user
	access_token = data['access_token']
	refresh_token = data['refresh_token']
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

	patient = Patient(code, access_token, refresh_token, expires_timestamp)
	return patient

def refresh_token(patient):
	'''refreshes patient token'''
	response = requests.post(URL_ONPATIENT + 'o/token/', data={
	  'refresh_token': patient.get_refresh_token(),
	  'grant_type': 'refresh_token',
	  'client_id': CLIENT_ID,
	  'client_secret': CLIENT_SECRET,
	})


def get_patient_data(patient):
	response = requests.get(URL_CHRONO + 'onpatient_api/fhir/Patient', headers= {
  	'Authorization': 'Bearer %s' % patient.get_access_token(),
	})

	response.raise_for_status()
	data = response.json()
	return data

def set_patient_data(data, patient):
	data = data['results'][0]
	for k, v in data.items():
		print(k, v, "\n")

	if not PatientID.objects.filter( id = data["identifier"] ).exists():
		patient_obj = PatientID.objects.create( id = data["identifier"] )
		patient_obj.save()

	patient_data = []
	patient_contact = []
	name_dict = data["name"][0]
	name =  " ".join(name_dict["family"]) + ", " + " ".join(name_dict["given"])
	patient.name = " ".join(name_dict["given"])
	# teleCom = data["telecom"]

	patient_data.append( ("Name", name) )
	patient_data.append( ("ID", data["identifier"]) )
	patient_data.append( ("DOB", data["birthDate"]) )
	patient_data.append( ("Gender", data["gender"]) )

	for d in data["telecom"]:
		print("d: ", d)
		if d['system'] == 'email':
			patient_data.append( ('Email', d['value']) )
		elif d['use'] == 'home':
			patient_data.append( ('Home Phone', d['value']) )
		elif d['use'] == 'mobile':
			patient_data.append( ('Cell Phone', d['value']) )
	

	for k, v in sorted(data["address"][0].items(), key = lambda p: p[0]):
		if k == "line": patient_data.append( ("Street", " ".join(v)) )
		elif k == "city": patient_data.append( ("City", v) )
		elif k == "state": patient_data.append( ("State", v) )
		elif k == "postalCode": patient_data.append( ("Zip Code", v) )

	patient_data.append( ("Status", data["active"]) )

	return patient_data

#end of helper methods


#start of views.
def welcome(request):
	return render(request, 'welcome.html')

def home(request):
	global patient

	if not patient:
		code = request.GET.get('code')
		error = request.GET.get('error')
		print(code, error, patient)

		if error: 
			return render(request, 'error.html')

		patient = get_token(code)
		data = get_patient_data(patient)
		patient.patient_data = set_patient_data(data, patient)
		print("patient: ", patient.patient_data)
			

	return render(request, 'home.html', {'username': username, 'patients': patient.patient_data})

def bp(request):
	return render(request, 'bp.html', {'username': username})

def sleep(request):
	return render(request, 'sleep.html', {'username': username})

def weight(request):
	return render(request, 'weight.html', {'username': username})

def hydrate(request):
	return render(request, 'hydrate.html', {'username': username})

def logout(request):
	global patient
	patient = None
	return render(request, 'welcome.html')