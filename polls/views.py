# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
import api_methods

patient = None
username = ""


#start of views.
def welcome(request):
	return render(request, 'welcome.html')

def home(request):
	global patient, username

	if not patient:
		code = request.GET.get('code')
		error = request.GET.get('error')
		print(code, error, patient)

		if error: 
			return render(request, 'error.html')

		patient = api_methods.get_token(code)
		data = api_methods.get_patient_data(patient)
		patient.patient_data, username = api_methods.set_patient_data(data, patient)
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