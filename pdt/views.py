from django.shortcuts import render, render_to_response
from django.template import RequestContext,loader,Context
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from models import *
# Create your views here.
USER_DEVELOPER = 1
USER_MANAGER = 2

def index(request):
	if request.user.is_authenticated():
		if request.user.is_staff:
			return HttpResponseRedirect("/admin")
		if request.user.profile.role == USER_DEVELOPER:
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
			if not item.project.status:
				continue;
			pid = item.project.id 
			project.append(item.project)
			ph = Phase.objects.get(project_id = pid,status = True)
			i = Iteration.objects.get(phase = ph,status = True)
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
	if request.user.profile.role == USER_MANAGER:
		p = Project.objects.all()
		itera = list()
		for item in p:
			if not item.status: #ongoing project
				continue
			ph = Phase.objects.get(project_id = item.id,status = True)
			itera.append(Iteration.objects.get(phase_id = ph.id,status = True))
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
	phase = Phase.objects.get(project_id = project.id,status = True)
	iteration = Iteration.objects.get(phase_id = phase.id,status = True)
	#return HttpResponse(iteration.id)
	s.iteration_id = iteration.id
	s.developer_id = request.user.id
	s.SLOC = 0
	s.sessionlast = 0
	s.save()
	#return HttpResponse("%d   %d"%(s.id,int(request.session['Session'])))
	c = Context({'prj':project,'phase':phase,'itrno':iteration.no,'user':request.user,'sid':s.id})
	return render_to_response("devaction.html",c)

@login_required
def endDevelopeSession(request):
	s = SLOCSession.objects.get(id = int(request.POST['sid']))
	t = str(request.POST['time'])
	ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
	s.sessionlast = ts
	i = Iteration.objects.get(id = s.iteration_id)
	p = Phase.objects.get(id = i.phase_id)
	pj = Project.objects.get(id = p.project_id)
	i.totalTime = i.totalTime + ts
	i.totalSLOC = i.totalSLOC + int(request.POST['sloc'])
	p.totalTime = p.totalTime + ts
	p.totalSLOC = p.totalSLOC + int(request.POST['sloc'])
	pj.totalTime = pj.totalTime + ts
	pj.totalSLOC = pj.totalSLOC + int(request.POST['sloc'])  
	s.SLOC = int(request.POST['sloc'])
	request.session['ds'] = s.id
	s.save()
	i.save()
	p.save()
	pj.save()
	return HttpResponseRedirect('/developer/dashboard/?prev=/developer/enddev/')

def beginDefectSession(request):
 	s = DefectSession(start_date = timezone.now(),defectno = 0,sessionlast = 0)
 	if request.POST.get('prjid',"") == "":
 		project = Project.objects.get(id = int(request.session['prjid']))
 	else:
 		project = Project.objects.get(id = int(request.POST['prjid']))
 		request.session['prjid'] = request.POST['prjid']
	phase = Phase.objects.get(project_id = project.id,status = True)
	iteration = Iteration.objects.get(phase_id = phase.id,status = True)
	phases = Phase.objects.filter(project_id = project.id)
	iterations = []
	for ph in phases:
		ites = Iteration.objects.filter(phase_id = ph.id)
		for i in ites:
			iterations.append(i)
	s.iteration = iteration
 	s.developer = request.user
 	iters = [0 for x in range(4)]
 	for x in range(4):
 		if x<phase.no:
 			iters[x] = len(Iteration.objects.filter(phase = (Phase.objects.get(project_id = project.id,no = x+1))).all())
	s.save()
	request.session['sid'] = s.id
	print len(iterations)
	iterno = iters[0]+iters[1]+iters[2]+iters[3]
	c = Context({'sid':s.id,'iters':iterations,'phaseno':phase.no,'phase1':iters[0],'phase2':iters[1],'phase3':iters[2],'phase4':iters[3]})
 	return render_to_response("dev-defect.html",c)

def addDefect(request):
 	s = DefectSession.objects.get(id = int(request.session['sid']))
 	d = Defects(session_id = s.id,name = request.POST['name'],typed = int(request.POST['type']),desc = request.POST['desc'])
 	#d.iterationInjected = request.POST['iterationInjected']
 	iters = [0 for x in range(4)]
 	for x in range(4):
 		if x<s.iteration.phase.no:
 			iters[x] = len(Iteration.objects.filter(phase = (Phase.objects.get(project_id = s.iteration.phase.project.id,no = x+1))).all())
 	iternum = int(request.POST['iterationInjected'])
 	m  = 0
 	while(1):
 		if iternum - iters[m]>0:
 			iternum -=iters[m]
 			m+=1
 		else:
 			break
 	d.iterationInjected = Iteration.objects.get(phase_id = (Phase.objects.get(project_id = s.iteration.phase.project.id,no = m+1).id),no = iternum)

 	d.iterationRemoved = s.iteration
 	s.defectno = s.defectno+1
 	s.save()
 	d.save()
 	return HttpResponse("")

def endDefectSession(request):
 	s = DefectSession.objects.get(id = int(request.session['sid']))
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

# def getAllSessionOfAIterationOnDefect(request):
# 	iid = int(request.POST['iteration'])
# 	session_set = DefectSession.objects.get(iteration = iid)
# 	return render_to_response("defectmanageiter.html")
# def getAllSessionOfAUserOnDefect(request):
# 	 uid = int(request.POST['developer'])
# 	 session_set = DefectSession.objects.get(developer = uid)
# 	 return render_to_response("defectmanagedev.html")

@login_required
def manReport(request,pid):
	if request.user.profile.role == USER_MANAGER:
		p = Project.objects.get(id = int(pid))
		qphase = request.GET.get('phase','Overall')
		totph = len(Phase.objects.filter(project_id = p.id).all())
		qiter = request.GET.get('iteration','Overall')
		totit = 0
		if qphase == 'Overall':
			phases = Phase.objects.filter(project_id = p.id).all()
			totsloc = p.totalSLOC
			time = p.totalTime
		else:
			oldphase = Phase.objects.filter(project_id = p.id,no__lt = int(qphase)).all()
			totsloc = 0
			time = 0
			for ph in oldphase:
				totsloc += ph.totalSLOC
				time += ph.totalTime
			nowphase = Phase.objects.get(project_id = p.id,no = int(qphase))
			totit = len(Iteration.objects.filter(phase_id = nowphase.id))
			if qiter== 'Overall':
				totsloc += nowphase.totalSLOC
				time += nowphase.totalTime
			else:
				iteration_list = Iteration.objects.filter(phase_id = nowphase.id,no__lt = int(qiter)).all()
				for itera in iteration_list:
					totsloc += itera.totalSLOC
					time += itera.totalTime
		c = Context({'prhname':p.name, 'totph':totph ,'curphase':qphase,'curitr':qiter,'totitr':totit,'time':time,'totsloc':totsloc,'user':request.user})
		return render_to_response('manreport.html',c)
	else:
		return HttpResponseRedirect('/')

@login_required
def manProject(request,pid):
	if request.user.profile.role == USER_MANAGER:
		p = Project.objects.get(id = int(pid))
		curphase = Phase.objects.get(project_id  =p.id,status = True)
		curitr = Iteration.objects.get(phase_id = curphase.id,status = True)
		phase_list = Phase.objects.filter(project_id = p.id).all()
		totph = len(phase_list)
		totit = 0
		for ph in phase_list:
			totit = totit + len(Iteration.objects.filter(phase_id = ph.id).all())
		time = p.totalTime
		totsloc  = p.totalSLOC
		slocestimate = totsloc/p.slocestimate
		c = Context({'prjname':p.name, 'totph':totph ,'slocestimate':slocestimate,'curphase':curphase.no,'curitr':curitr.no,'totitr':totit,'time':time,'totsloc':totsloc,'user':request.user})
		return render_to_response('manproject.html',c)
	else:
		return HttpResponseRedirect('/')








