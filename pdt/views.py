from django.shortcuts import render, render_to_response
fron django.template import RequestContext,loader
from django.http import HttpResponse
from django.utils import timezone
from . import SLOCSesson,DefectSession,Defect,ManageSession
# Create your views here.
def index(request):
	return render_to_response("login.html")
def beginDevelopeSession(request):
	s = SLOCSesson(start_data=timezone.now(),SLOC = 0, sessionlast = 0)
	s.interation = int(request.session['iteration'])
	s.developer = int(request.session['user'])
	s.save()
	return render_to_response("sloc.html")

def endDevelopeSession(request):
	s = SLOCSesson.objects.get(id = request.id)
	s.sessionlast = request.POST['time']
	s.SLOC = request.POST['SLOC']
	s.save()
	return render_to_response('index.html')

def beginDefectSession(request):
	s = DefectSession(start_data = timezone.now(),defectno = 0,sessionlast = 0)
	s.interation = int(request.session['iteration'])
	s.developer = int(request.session['user'])
	s.save()
	return render_to_response("defectsession.html")

def addDefect(request):
	s = DefectSession.objects.get(id = request.POST['id'])
	d = Defect(session = s.id,type = int(request.POST['type']),desc = request.POST['desc'])
	d.iterationInjected = request.POST['injected']
	d.iterationRemoved = DefectSession.objects.get(id = s.iteration).id
	d.status = int(request.POST['status'])
	s.defectno = s.defectno+1
	s.save()
	d.save()
	return render_to_response("defectsession.html")

def endDefectSession(request):
	s = DefectSession.objects.get(id = request.POST['id'])
	s.time = int(request.POST['time'])
	return render_to_response("index.html")

def beginManageSession(request):
	s = ManageSession(start_data = timezone.now(),sessionlast = 0)
	s.interation = int(request.session['iteration'])
	s.developer = int(request.session['user'])
	s.save()
	return render_to_response("manage.html")

def endManageSession(request):
	s = ManageSession.objects.get(id = int(request.POST['id']))
	s.time = int(request.POST['time'])
	s.save()
	return render_to_response("index.html")

def getAllSessionOfAIterationOnSLOC(request):
	iid = int(request.POST['iteration'])
	session_set = SLOCSesson.objects.get(iteration = iid)
	return render_to_response("slocmanageiter.html")

def getAllSessionOfAIterationOnDefect(request):
	iid = int(request.POST['iteration'])
	session_set = DefectSession.objects.get(iteration = iid)
	return render_to_response("defectmanageiter.html")

def getAllSessionOfAUserOnSLOC(request):
	 uid = int(request.POST['developer'])
	 session_set = SLOCSession.objects.get(developer = uid)
	 return render_to_response("slocmanagedev.html")

def getAllSessionOfAUserOnDefect(request):
	 uid = int(request.POST['developer'])
	 session_set = DefectSession.objects.get(developer = uid)
	 return render_to_response("defectmanagedev.html")









