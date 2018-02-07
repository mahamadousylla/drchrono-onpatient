# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
import api_methods
import db_methods

patient = None
username = ""
patientID = -1

#start of views.
def welcome(request):
	return render(request, 'welcome.html')

def home(request):
	global patient, username, patientID

	if not patient:
		code = request.GET.get('code')
		error = request.GET.get('error')

		if error: 
			return render(request, 'error.html')

		patient = api_methods.get_token(code)
		data = api_methods.get_patient_data(patient)
		patient.patient_data, username, patientID = api_methods.set_patient_data(data, patient)

		api_methods.get_observation(patient)
	return render(request, 'home.html', {'username': username, 'patients': patient.patient_data})


def bp(request):
	return render(request, 'bp.html', {'username': username})

def chart_bp(request):
	systolic = request.GET.get("systolic")
	diastolic = request.GET.get("diastolic")
	if systolic is None or diastolic is None:
		return redirect("/bp.html")

	db_methods.save_bp(systolic, diastolic, patientID)
	obj = db_methods.get_bp(patientID)
	return render(request, 'chart_bp.html', {'username': username, 'bp': obj})	


def sleep(request):
	return render(request, 'sleep.html', {'username': username})

def chart_sleep(request):
	sleep = request.GET.get("sleep")
	if sleep is None:
		return redirect("/sleep.html")

	db_methods.save_sleep(sleep, patientID)
	obj = db_methods.get_sleep(patientID)
	obj["username"] = username
	return render(request, 'chart_sleep.html', obj)


def weight(request):
	return render(request, 'weight.html', {'username': username})

def chart_weight(request):
	print("hereeeee")
	weight = request.GET.get("weight")
	print("weight: ", weight)
	if weight is None:
		return redirect("/weight.html")

	db_methods.save_weight(weight, patientID)
	obj = db_methods.get_weight(patientID)
	obj["username"] = username
	return render(request, 'chart_weight.html', obj)


def hydrate(request):
	return render(request, 'hydrate.html', {'username': username})

def chart_hydrate(request):
	hydrate = request.GET.get("hydrate")
	if hydrate is None:
		return redirect("/hydrate.html")

	db_methods.save_hydrate(hydrate, patientID)
	obj = db_methods.get_hydrate(patientID)
	return render(request, 'chart_hydrate.html', {'username': username})


def logout(request):
	global patient
	patient = None
	return render(request, 'welcome.html')