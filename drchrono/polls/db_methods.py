from models import PatientID
import datetime


def helper(patientID):
	patient_obj = None
	if not PatientID.objects.filter( id = patientID ).exists():
		patient_obj = PatientID.objects.create( id = patientID )

	return patient_obj or PatientID.objects.get(id=patientID)

def find_bp(systolic, diastolic):
	pass


def save_bp(systolic, diastolic, patientID):
	patient_obj = helper(patientID)
	bp = systolic + "/" + diastolic
	curr_date = datetime.datetime.now()
	status = "" #figure out how to get what bp is. normal, stage 1 etc

	obj = [curr_date, systolic, diastolic, status]
	patient_obj.bp.append(obj)
	


def get_bp(patientID):
	p = PatientID.objects.get(id=patientID)
	return p.bp


def save_sleep(sleep, patientID):
	patient_obj = helper(patientID)
	now = datetime.datetime.now()
	curr_date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
	
	patient_obj.sleep.append(int(sleep))
	patient_obj.sleep_dates.append(curr_date)
	patient_obj.save()


def get_sleep(patientID):
	p = PatientID.objects.get(id=patientID)

	obj = {
		"title": "Sleep Tracker",
		"xaxis": "Dates",
		"dates": p.sleep_dates,
		"yaxis": "Hours",
		"seriesName": "Hours slept",
		"data": p.sleep,
		"mx": 24
	}

	return obj

def save_weight(weight, patientID):
	patient_obj = helper(patientID)
	now = datetime.datetime.now()
	curr_date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
	
	patient_obj.weight.append(int(weight))
	patient_obj.weight_dates.append(curr_date)
	patient_obj.save()


def get_weight(patientID):
	p = PatientID.objects.get(id=patientID)

	obj = {
		"title": "Weight Tracker",
		"xaxis": "Dates",
		"dates": p.weight_dates,
		"yaxis": "Weight",
		"seriesName": "Weight",
		"data": p.weight
	}

	return obj


def save_hydrate(hydrate, patientID):
	pass


def get_hydrate(patientID):

	obj = {
		"title": "Hydrate Tracker",
		"xaxis": "Dates",
		"dates": dates,
		"yaxis": "Hydration",
		"seriesName": "Hydration Level",
		"data": data
	}

	return obj