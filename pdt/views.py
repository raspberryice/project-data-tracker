from django.shortcuts import render, render_to_response
from django.template import RequestContext,loader,Context
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from .models import SLOCSession,ManageSession,Participate,Phase,Iteration,Project
# Create your views here.
USER_DEVELOPER = 1
USER_MANAGER = 2

def index(request):
	if request.user.is_authenticated():
		return HttpResponse("uid %d" % request.user.id)
		if request.user.Profile.role == USER_DEVELOPER:
			return HttpResponse("Haha")
			return HttpResponseRedirect("/developer/dashboard/")
		elif request.user.profile.role == USER_MANAGER:
			return HttpResponseRedirect("/manager/dashboard/")
		else:
			raise Http404("Not a valid user.")
	else:
		return HttpResponseRedirect("/auth/login/")

def login(request):
	return render_to_response("login.html")

def verify(request):
	if request.POST:
		user = auth.authenticate(username = request.POST['username'],password = request.POST['password'])
		if user is not None:
			auth.login(request,user)
			#return HttpResponse("uid %d" % request.user.id)
			if request.user.profile.role == USER_DEVELOPER:
				return HttpResponseRedirect("/developer/dashboard/")
			elif request.user.profile.role == USER_MANAGER:
				return HttpResponseRedirect("/manager/dashboard/")
			else:
				raise Http404("Not a valid user.")
		else:
			return render_to_response("login.html",{'failed':True})
	else:
		pass

def logout(req):
	log_out(req)
	return HttpResponseRedirect("/auth/login/?prev=/auth/logout/")

@login_required
def devdashboard(request):
	if request.user.profile.role == USER_DEVELOPER:
		p = Participate.objects.filter(developer_id = request.user.id).all()
		project = list()
		itera = list()
		phase = list()
		for item in p:
			pid = item.project.id
			project.append(item.project)
			ph = Phase.objects.get(project_id = pid)
			i = Iteration.objects.get(phase = ph)
			itera.append(i)
			phase.append(ph)
		#return HttpResponse("uid %d" % request.user.id)

		c = Context({
			'user':request.user,
			'prjlist':itera,
			'totprjcnt':len(project),
			'justcompleted':(request.GET.get('prev','')=='/developer/enddev')
			})
		return render_to_response("devdashboard.html",c)
	else:
		raise Http404("User is not a developer.")

@login_required
def mandashboard(request):
	if request.user.profile.role == USER_DEVELOPER:
		p = Project.objects.all()
		itera = list()
		for item in p:
			ph = Phase.objects.get(project_id = item.id)
			itera.append(Iteration.objects.get(phase_id = ph.id))
		c = Context({
			'user':request.user,
			'prjlist':itera,
			'totprjcnt':len(p),
			})
		return render_to_response("mandashboard.html",c)
	else:
		return HttpResponseRedirect("/")

@login_required
def beginDevelopeSession(request):
	#return HttpResponse("hahh")
	s = SLOCSession(start_date=timezone.now())
	project = Project.objects.get(id = int(request.POST['prjid']))
	phase = Phase.objects.get(project_id = project.id)
	iteration = Iteration.objects.get(phase_id = phase.id)
	#return HttpResponse(iteration.id)
	s.iteration_id = iteration.id
	s.developer_id = request.user.id
	s.SLOC = 0
	s.sessionlast = 0
	s.save()
	#return HttpResponse("%d   %d"%(s.id,int(request.session['Session'])))
	c = Context({'prj':project,'phase':phase,'itrno':iteration.id,'user':request.user,'sid':s.id})
	return render_to_response("devaction.html",c)

@login_required
def endDevelopeSession(request):
	s = SLOCSession.objects.get(id = int(request.POST['sid']))
	t = str(request.POST['time'])
	ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
	s.sessionlast = ts
	s.SLOC = int(request.POST['sloc'])
	s.save()
	return HttpResponseRedirect('/developer/dashboard/?prev=/developer/enddev/')

def beginDefectSession(request):
	s = DefectSession(start_data = timezone.now(),defectno = 0,sessionlast = 0)
	s.interation = int(request.session['iteration'])
	s.developer = int(request.session['user'])
	s.save()
	return render_to_response("defectsession.html")

# def addDefect(request):
# 	s = DefectSession.objects.get(id = request.POST['id'])
# 	d = Defect(session = s.id,type = int(request.POST['type']),desc = request.POST['desc'])
# 	d.iterationInjected = request.POST['injected']
# 	d.iterationRemoved = DefectSession.objects.get(id = s.iteration).id
# 	d.status = int(request.POST['status'])
# 	s.defectno = s.defectno+1
# 	s.save()
# 	d.save()
# 	return render_to_response("defectsession.html")

# def endDefectSession(request):
# 	s = DefectSession.objects.get(id = request.POST['id'])
# 	s.time = int(request.POST['time'])
# 	return render_to_response("index.html")

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

# def getAllSessionOfAIterationOnDefect(request):
# 	iid = int(request.POST['iteration'])
# 	session_set = DefectSession.objects.get(iteration = iid)
# 	return render_to_response("defectmanageiter.html")

def getAllSessionOfAUserOnSLOC(request):
	 uid = int(request.POST['developer'])
	 session_set = SLOCSession.objects.get(developer = uid)
	 return render_to_response("slocmanagedev.html")

# def getAllSessionOfAUserOnDefect(request):
# 	 uid = int(request.POST['developer'])
# 	 session_set = DefectSession.objects.get(developer = uid)
# 	 return render_to_response("defectmanagedev.html")

@login_required
def manReport(request,pid):
	if request.user.profile.role == USER_DEVELOPER:
		p = Project.objects.get(id = int(pid))
		iters = []
		sloc = 0
		time = 0
		pha = []
		qphase = request.GET.get('phase','Overall')
		totph = len(Phase.objects.filter(project_id = p.id).all())
		qiter = request.GET.get('iteration','Overall')
		totsloc = 0
		tottime = 0
		totit = 0
		if qphase == 'Overall':
			phases = Phase.objects.filter(project_id = p.id).all()
		else:
			phases = Phase.objects.filter(project_id = p.id,no = int(qphase)+1).all()
		for p1 in phases:
			totit = len(Iteration.objects.filter(phase_id = p1.id).all())
			if qphase=='Overall':
				totit = 0
			if qiter=='Overall':
				iteration = Iteration.objects.filter(phase_id = p1.id).all()
			else:
				iteration = Iteration.objects.filter(phase_id = p1.id,no = int(qiter)-1).all()
			for i in iteration:
				sloc = 0
				time = 0
				iters.append(i)
				session = SLOCSession.objects.filter(iteration_id = i.id).all()
				for s in session:
					sloc = sloc + int(s.SLOC)
					time = time + int(s.sessionlast)
				i.totalSLOC = sloc
				i.totalTime = time
				i.save()
				totsloc = totsloc+sloc
				tottime = tottime+time
		c = Context({'project':p, 'totph':totph ,'curphase':qphase,'curitr':qiter,'totitr':totit,'time':time,'totsloc':totsloc,'user':request.user})
		return render_to_response('manreport.html',c)
	else:
		return HttpResponseRedirect('/')

@login_required
def manProject(request,pid):
	if request.user.profile.role == USER_DEVELOPER:
		p = Project.objects.get(id = int(pid))
		iters = []
		sloc = 0
		time = 0
		pha = []
		qphase = request.GET.get('phase','Overall')
		totph = len(Phase.objects.filter(project_id = p.id).all())
		qiter = request.GET.get('iteration','Overall')
		totsloc = 0
		tottime = 0
		totit = 0
		if qphase == 'Overall':
			phases = Phase.objects.filter(project_id = p.id).all()
		else:
			phases = Phase.objects.filter(project_id = p.id,no = int(qphase)+1).all()

		for p1 in phases:
			totit = len(Iteration.objects.filter(phase_id = p1.id).all())
			if qphase=='Overall':
				totit = 0
			if qiter=='Overall':
				iteration = Iteration.objects.filter(phase_id = p1.id).all()
			else:
				iteration = Iteration.objects.filter(phase_id = p1.id,no = int(qiter)-1).all()
			for i in iteration:
				sloc = 0
				time = 0
				iters.append(i)
				session = SLOCSession.objects.filter(iteration_id = i.id).all()
				for s in session:
					sloc = sloc + int(s.SLOC)
					time = time + int(s.sessionlast)
				i.totalSLOC = sloc
				i.totalTime = time
				i.save()
				totsloc = totsloc+sloc
				tottime = tottime+time

		c = Context({'project':p, 'totph':totph ,'curphase':qphase,'curitr':qiter,'totitr':totit,'time':time,'totsloc':totsloc,'user':request.user})
		return render_to_response('manproject.html',c)
	else:
		return HttpResponseRedirect('/')
