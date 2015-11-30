from django.shortcuts import render, render_to_response
from django.template import RequestContext,loader,Context
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from pdt.models import *
from pdt.utility import *
import json
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
            if request.user.is_staff:
                return HttpResponseRedirect("/admin/")
            elif request.user.profile.role == USER_DEVELOPER:
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
                continue
            pid = item.project.id
            project.append(item.project)
            ph = Phase.objects.get(project_id = pid,status = True)
            i = Iteration.objects.get(phase = ph,status = True)
            itera.append(i)
            phase.append(ph)
        #return HttpResponse("uid %d" % request.user.id)
        print (request.GET.get('prev','')=='/developer/enddev/')
        c = Context({
            'user':request.user,
            'prjlist':itera,
            'totprjcnt':len(p),
            'justcompleteddev':(request.GET.get('prev','')=='/developer/enddev/'),
            'justcompleteddef':(request.GET.get('prev','')=='/developer/enddef/'),
            'justcompletedman':(request.GET.get('prev','')=='/developer/endman/'),
            })
        return render_to_response("dev-dashboard.html",c)
    else:
        raise Http404("User is not a developer.")


@login_required
def devAllProjects(request):
    if request.user.profile.role == USER_DEVELOPER:
        p = Participate.objects.filter(developer_id = request.user.id).all()
        project = list()
        itera = list()
        phase = list()
        closed = []
        for item in p:
            if not item.project.status:
                closed.append(item.project)
            if not item.project.status:
                continue
            pid = item.project.id
            project.append(item.project)
            ph = Phase.objects.get(project_id = pid,status = True)
            i = Iteration.objects.get(phase = ph,status = True)
            itera.append(i)
            phase.append(ph)
        c = Context({
            'user': request.user,
            'prjlist': itera,
            'closed': closed,
            'totopenprj': len(itera),
            'totprj': len(itera) + len(closed),
        })
        return render_to_response("dev-allprojects.html", c)
    else:
        return HttpResponseRedirect("/")



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
        return render_to_response("man-dashboard.html",c)
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
    return render_to_response("dev-action.html",c)

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
    print (len(iterations))
    iterno = iters[0]+iters[1]+iters[2]+iters[3]
    c = Context({
        'user': request.user,
        'sid':s.id,
        'iters':iterations,
        'phaseno':phase.no,
        'phase1':iters[0],
        'phase2':iters[1],
        'phase3':iters[2],
        'phase4':iters[3]
    })
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
@login_required
def endDefectSession(request):
    s = DefectSession.objects.get(id = int(request.session['sid']))
    t = str(request.POST['time'])
    ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
    s.sessionlast = ts
    s.save()
    i = Iteration.objects.get(id = s.iteration_id)
    p = Phase.objects.get(id = i.phase_id)
    pj = Project.objects.get(id = p.project_id)
    i.totalTime = i.totalTime + ts
    p.totalTime = p.totalTime + ts
    pj.totalTime = pj.totalTime + ts
    i.save()
    p.save()
    pj.save()
    return HttpResponseRedirect("/developer/dashboard/?prev=/developer/enddef/")


@login_required
def devProject(req, pid):
    if req.user.profile.role == 1:
        # get data of project(id = pid)

        c = Context({
            'user': req.user,
            'prjname': "Project 3",
            'curphase': 2,
            'curphasename': 'Elaboration',
            'nextphasename': 'Construction',
            'curitr': 3,
            'startdate': "9/20/2015",
            'enddate': "today",
            'totsloc': 2345,
            'totslocesti': 35,  # stands for 35%
            'personmonths': 20,
            'pmesti': 30,
            'avesloc': 117,
            'closed': False, # whether the project has been closed
        })
        return render_to_response("dev-project.html", c)
    else:
        return HttpResponseRedirect("/")

@login_required
def devReport(req, pid):
    if req.user.profile.role == 1:
        # projectid == pid
        queryphase = req.GET.get('phase', 'Overall')
        queryitr = req.GET.get('iteration', 'Overall')
        c = Context({
            'user': req.user,
            'prjname': "Project 3",
            'curphase': queryphase,
            'curitr': queryitr,
            'totphase': 2,
            'totitr': 0 if queryphase == 'Overall' else (1 if queryphase == '1' else 2),
            'totsloc': 2345,
            'totslocesti': 35,  # stands for 35%
            'personmonths': 20,
            'pmesti': 30,
            'avesloc': 117,
        })
        return render_to_response("dev-report.html", c)
    else:
        return HttpResponseRedirect("/")

   
@login_required
def beginManageSession(request):
    s = ManageSession(start_date = timezone.now(),sessionlast = 0)
    s.manager = request.user
    project = Project.objects.get(id = int(request.POST['prjid']))
    phase = Phase.objects.get(project_id = project.id,status = True)
    iteration = Iteration.objects.get(phase_id = phase.id,status = True)
    s.iteration = iteration
    iters = Iteration.objects.filter(phase__project=project)
    developsessions = []
    managesessions = []
    defectsessions = []
    defectlist = []
    s.end_date = timezone.now()
    for ph in Phase.objects.filter(project_id = project.id).all():
        for i in Iteration.objects.filter(phase_id = ph.id).all():
            for ses in SLOCSession.objects.filter(developer = s.manager,iteration = i).all():
                developsessions.append(ses)
            for ses in ManageSession.objects.filter(manager = s.manager,iteration = i).all():
                managesessions.append(ses)
            for ses in DefectSession.objects.filter(developer = s.manager,iteration = i).all():
                defectsessions.append(ses)
                for de in Defects.objects.filter(session = ses).all():
                    defectlist.append(de)
    print (len(developsessions),len(managesessions),len(defectlist),len(defectsessions))
    c = Context({
        'user': request.user,
        'developsessions':developsessions,
        'managesessions':managesessions,
        'defectsessions':defectsessions,
        'defect_list':defectlist,
        'iters':iters,
    })
    s.save()
    request.session['sid'] = s.id
    return render_to_response("dev-manage.html",c)

def endManageSession(request):
    s = ManageSession.objects.get(id = int(request.session['sid']))
    t = str(request.POST['time'])
    ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
    s.sessionlast = ts
    s.save()
    i = Iteration.objects.get(id = s.iteration_id)
    p = Phase.objects.get(id = i.phase_id)
    pj = Project.objects.get(id = p.project_id)
    i.totalTime = i.totalTime + ts
    p.totalTime = p.totalTime + ts
    pj.totalTime = pj.totalTime + ts
    i.save()
    p.save()
    pj.save()
    return HttpResponseRedirect("/developer/dashboard/?prev=/developer/endman/")


@login_required
def manReport(request,pid):
    if request.user.profile.role == USER_MANAGER:
        p = Project.objects.get(id = int(pid))
        qphase = request.GET.get('phase','Overall')
        qiter = request.GET.get('iteration','Overall')
        phases = Phase.objects.filter(project_id = p.id,status = False).all()
        totph = len(phases)
        if p.status:
            curphas = Phase.objects.get(project_id = p.id,status = True)
            if not Iteration.objects.get(phase_id = curphas.id,no=1).status:
                totph +=1
        curphaseno = 0
        time = 0
        totsloc = 0
        currentsloc = 0
        totaldefects = 0
        phaseclosed = False
        yieldrate = ""
        density = ""
        injectionrate = ""
        injected = ""
        projectclosed = False
        if qphase == 'Overall':
            totit = 0
            for ph in phases:
                totsloc += ph.totalSLOC
                currentsloc+=ph.totalSLOC
                time += ph.totalTime
                for itera in Iteration.objects.filter(phase_id = ph.id).all():
                    for ses in DefectSession.objects.filter(iteration_id = itera.id).all():
                        totaldefects +=ses.defectno
            if totph > len(phases):
                for itera in Iteration.objects.filter(phase_id = curphas.id,status = False).all():
                    totsloc += itera.totalSLOC
                    currentsloc += itera.totalSLOC
                    time += itera.totalTime
                    for ses in DefectSession.objects.filter(iteration_id = itera.id).all():
                        totaldefects += ses.defectno
        else:
            curphaseno = int(qphase)
            ph = Phase.objects.get(project_id = p.id,no = curphaseno)
            phaseclosed = not ph.status
            iters = Iteration.objects.filter(phase_id = ph.id,status = False)
            totit = len(iters)

            if qiter == 'Overall':
                oldphases = Phase.objects.filter(project_id = p.id,no__lt = ph.no).all()
                for pha in oldphases:
                    totsloc+=pha.totalSLOC
                for itera in iters:
                    totsloc += itera.totalSLOC
                    currentsloc += itera.totalSLOC
                    time += itera.totalTime
                    for ses in DefectSession.objects.filter(iteration_id = itera.id).all():
                        totaldefects+=ses.defectno
            else:
                oldphases = Phase.objects.filter(project_id = p.id,no__lt = ph.no).all()
                queryiter = Iteration.objects.get(phase_id = ph.id,no = int(qiter))
                time = queryiter.totalTime
                currentsloc += queryiter.totalSLOC
                totsloc+=queryiter.totalSLOC
                for pha in oldphases:
                    totsloc+=pha.totalSLOC
                olditers = Iteration.objects.filter(phase_id = ph.id,no__lt = int(qiter)).all()
                for ite in olditers:
                    totsloc+=ite.totalSLOC
                for ses in DefectSession.objects.filter(iteration_id = queryiter.id).all():
                    totaldefects += ses.defectno
        if not p.status:
            projectclosed = True
            phases = Phase.objects.filter(project_id = p.id).all()
            lastphase = Phase.objects.get(project_id = p.id,no = len(phases))
            iters = Iteration.objects.filter(phase_id = lastphase.id).all()
            lastiter = Iteration.objects.get(phase_id = lastphase.id,no = len(iters))
            lastremove = 0
            lastnowremove = 0
            evolve = []
            if qphase == "Overall":
                for ph in phases:
                    for ite in Iteration.objects.filter(phase_id=ph.id).all():
                        evolve.append(ite)
            else:
                if qiter =="Overall":
                    phs = Phase.objects.filter(project_id = p.id,no__lte = int(qphase)).all()
                    for ph in phs:
                        for ite in Iteration.objects.filter(phase_id = ph.id).all():
                            evolve.append(ite)
                else:
                    phs = Phase.objects.filter(project_id = p.id,no__lt = int(qphase)).all()
                    for ph in phs:
                        for ite in Iteration.objects.filter(phase_id = ph.id).all():
                            evolve.append(ite)
                    nowphas = Phase.objects.get(project_id = p.id,no = int(qphase))
                    for iters in Iteration.objects.filter(phase_id = nowphas.id,no__lte = int(qiter)):
                        evolve.append(iters)
            now =[]
            if qphase != "Overall":
                if qiter == "Overall":
                    nowphas = Phase.objects.get(project_id = p.id,no = int(qphase))
                    for iters in Iteration.objects.filter(phase_id = nowphas.id).all():
                        now.append(iters)
                else:
                    nowphas = Phase.objects.get(project_id = p.id,no = int(qphase))
                    nowite = Iteration.objects.get(phase_id = nowphas.id,no = int(qiter))
                    now.append(nowite)
            for d in Defects.objects.filter(iterationRemoved = lastiter).all():
                if d.iterationInjected in evolve:
                    lastremove+=1
                if qphase == "Overall":
                    lastnowremove+=1
                elif d.iterationInjected in now:
                    lastnowremove+=1

            alldefectnow = 0
            for d in Defects.objects.all():
                if d.iterationInjected in evolve:
                    alldefectnow+=1
            alldefectremovebefore = 0
            if qphase!="Overall":
                before = []
                for ph in Phase.objects.filter(project_id = p.id,no__lt = int(qphase)).all():
                    for iters in Iteration.objects.filter(phase_id = ph.id).all():
                        before.append(iters)
                if qiter!="Overall":
                    nowphas = Phase.objects.get(project_id = p.id,no = int(qphase))
                    for its in Iteration.objects.filter(phase_id = nowphas.id,no__lt=int(qiter)):
                        before.append(its)
                for d in Defects.objects.all():
                    if d.iterationRemoved in before:
                        alldefectremovebefore+=1
            injected = totaldefects+lastnowremove*1.0/p.yieldrate*(1-p.yieldrate)
            injectionrate = injected /(len(Participate.objects.filter(project_id = p.id).all())*1.0*time/3600) if (len(Participate.objects.filter(project_id = p.id).all())*1.0*time/3600) != 0 else  "error"
            yieldrate = totaldefects*1.0/(1.0*(alldefectnow+lastremove/p.yieldrate*(1-p.yieldrate)-alldefectremovebefore)) if (alldefectnow+lastremove/p.yieldrate*(1-p.yieldrate)-alldefectremovebefore)!= 0 else "error"
            density = injected/(1.0*currentsloc/1000) if (1.0*currentsloc/1000) != 0 else "error"
        personhourrate = '%.2f' % (totaldefects*1.0/(len(Participate.objects.filter(project_id = p.id).all())*p.totalTime/3600.0)) if len(Participate.objects.filter(project_id = p.id).all())!= 0 and p.totalTime > 0 else "error"
        day = (timezone.now() - p.start_date).days
        pm  = len(Participate.objects.filter(project_id = p.id))*day/30.0
        personmonth = currentsloc/pm if pm !=0 else  "error"
        c = Context({
                'pid':pid,
                'projectclosed': projectclosed,
                'phaseclosed': phaseclosed,
                'prhname':p.name,
                'personmonths':pm,
                'avesloc':personmonth,
                'epm':pm/p.effortestimate,
                'esloc':totsloc/p.slocestimate,
                'removed':totaldefects,
                'removalrate':personhourrate,
                'totphase':totph ,
                'curphase':qphase,
                'curitr':qiter,
                'totitr':totit,
                'time':time,
                'injected' :injected,
                'injectionrate':injectionrate,
                'density':density,
                'totsloc':totsloc,
                'yield':yieldrate,
                'user':request.user})
        return render_to_response('man-report.html',c)
    else:
        return HttpResponseRedirect("/")

##view defects
@login_required
def manDefect(request, pid):
    if request.user.profile.role == 2:
        # projectid == pid
        project = Project.objects.get(id = int(request.session['pid']))
        defectlist = []
        for ph in Phase.objects.filter(project_id = project.id).all():
            for i in Iteration.objects.filter(phase_id = ph.id).all():
                for ses in DefectSession.objects.filter(iteration = i).all():
                    for de in Defects.objects.filter(session = ses).all():
                        defectlist.append(de)
        c = Context({
            'pid':pid,
            'user':request.user,
            'defect_list':defectlist
        })
        return render_to_response("man-defect.html", c)
    else:
        return HttpResponseRedirect("/")

##view defects
@login_required
def manActivity(request, pid):
    if request.user.profile.role == 2:
        project = Project.objects.get(id = int(request.session['pid']))
        developsessions = []
        managesessions = []
        defectsessions = []
        defectlist = []
        for ph in Phase.objects.filter(project_id = project.id).all():
            for i in Iteration.objects.filter(phase_id = ph.id).all():
                for ses in SLOCSession.objects.filter(iteration = i).all():
                    developsessions.append(ses)
                for ses in ManageSession.objects.filter(iteration = i).all():
                    managesessions.append(ses)
                for ses in DefectSession.objects.filter(iteration = i).all():
                    defectsessions.append(ses)
        c = Context({
            'pid':pid,
            'user':request.user,
            'developsessions':developsessions,
            'managesessions':managesessions,
            'defectsessions':defectsessions
        })
        return render_to_response("man-activity.html", c)
    else:
        return HttpResponseRedirect("/")



@login_required
def manProject(request,pid):
    if request.user.profile.role == USER_MANAGER:
        p = Project.objects.get(id = int(pid))
        request.session['pid'] = p.id
        totaldefects = 0
        if p.status:
            curphase = Phase.objects.get(project_id  =p.id,status = True)
            curitr = Iteration.objects.get(phase_id = curphase.id,status = True)
        phase_list = Phase.objects.filter(project_id = p.id).all()
        for ph in phase_list:
            for itera in Iteration.objects.filter(phase_id = ph.id).all():
                for ses in DefectSession.objects.filter(iteration_id = itera.id).all():
                    totaldefects += ses.defectno
        totph = len(phase_list)
        totit = 0
        yieldrate = ""
        density = ""
        injectionrate = ""
        injected = ""
        personhourrate = '%.2f' % (totaldefects*1.0/(len(Participate.objects.filter(project_id = p.id))*p.totalTime/3600.0)) if p.totalTime > 0 and len(Participate.objects.filter(project_id = p.id).all())!=0 else "error"
        for ph in phase_list:
            totit = totit + len(Iteration.objects.filter(phase_id = ph.id).all())
        time = p.totalTime
        totsloc  = p.totalSLOC
        slocestimate = totsloc/p.slocestimate
        day = (timezone.now() - p.start_date).days
        pm  = len(Participate.objects.filter(project_id = p.id))*day/30.0 if day!=0 else "error"
        if pm == "error":
            personmonth = "error"
        else:
            personmonth = p.totalSLOC/pm
        convertdate = lambda d: str(d.month)+'/'+str(d.day)+'/'+str(d.year)
        devsession_list = SLOCSession.objects.filter(iteration__phase__project=p)
        remsession_list = DefectSession.objects.filter(iteration__phase__project=p)
        graph_data = render_graph(devsession_list,remsession_list)
        if not p.status:
            phases = Phase.objects.filter(project_id = p.id).all()
            lastphase = Phase.objects.get(project_id = p.id,no = len(phases))
            iters = Iteration.objects.filter(phase_id = lastphase.id).all()
            lastiter = Iteration.objects.get(phase_id = lastphase.id,no = len(iters))
            curphase = lastphase
            curitr = lastiter
            lastremove = 0
            for session in DefectSession.objects.filter(iteration_id = lastiter.id).all():
                lastremove+=session.defectno
            injected = totaldefects+lastremove/p.yieldrate*(1-p.yieldrate)
            if injected!= 0:
                yieldrate = '%.2f' %(totaldefects*1.0/injected)
            else:
                yieldrate = "error"
            if p.totalSLOC!= 0:
                density = '%.2f' %(injected*1.0/(p.totalSLOC*1.0/1000))
            else:
                density = "error"
            if p.totalTime!=0 and len(Participate.objects.filter(project_id = p.id).all())!=0:
                injectionrate = '%.2f' % (injected*1.0/(len(Participate.objects.filter(project_id = p.id).all())*1.0*p.totalTime/3600))
            else:
                injectionrate = "error"
        else:
            curphase = Phase.objects.get(project_id  =p.id,status = True)
            curitr = Iteration.objects.get(phase_id = curphase.id,status = True)
        c = Context({
            'pid':pid,
            'prjname':p.name,
            'density':density,
            'yield':yieldrate,
            'startdate': convertdate(p.start_date),
            'enddate': convertdate(timezone.now()) if p.status==True else convertdate(p.end_date),
            'avesloc':'%.2f' % personmonth,
            'removalrate': personhourrate,
            'personmonths': '%.2f' % pm,
            'epm': '%.2f' % (pm/p.effortestimate),
            'esloc':totsloc*1.0/p.slocestimate,
            'injected':injected,
            'injectionrate':injectionrate,
            'removed':totaldefects, 
            'totph':totph ,
            'slocestimate':slocestimate,
            'curphase':curphase.no,
            'next':curphase.no+1,
            'curitr':curitr.no,
            'totitr':totit,
            'time':time,
            'totsloc':totsloc,
            'user':request.user,
            'graph_data':json.dumps(graph_data),
            })
        return render_to_response('man-project.html',c)
    else:
        return HttpResponseRedirect('/')

@login_required
def addproject(request):
    if request.POST.get('name',"")!="":
        p = Project(name = request.POST['name'],desc = request.POST['description'],slocestimate = int(request.POST['esloc']),effortestimate = int(request.POST['epm']))
        p.status = True
        p.totalSLOC=  0
        p.totalTime = 0
        p.totalDefects = 0
        p.end_date = timezone.now()
        p.start_date = timezone.now()
        p.yieldrate = int(request.POST['yield'])/100.0
        p.save()
        ph = Phase(no = 1,status = True,totalSLOC = 0,totalTime = 0,totalDefects = 0,project_id = p.id, start_date = timezone.now(),end_date = timezone.now())
        ph.save()
        itera = Iteration(no = 1,status = True,totalSLOC = 0,totalTime = 0,totalDefects = 0,phase_id = ph.id, start_date = timezone.now(),end_date = timezone.now())
        liss = request.POST.getlist("developers",[])
        itera.save()
        for i in liss:
            par = Participate(project_id = p.id,developer_id = int(i))
            par.save()
        return HttpResponseRedirect('/manager/dashboard')
    else:
        u = []
        for i  in User.objects.all():
            if not i.is_staff:
                if i.profile.role == USER_DEVELOPER:
                    u.append(i)
        c= Context({'developerlist':u, 'user': request.user})
        return render_to_response("man-newproject.html",c)


@login_required
def manAllProjects(request):
    if request.user.profile.role == USER_MANAGER:
        p = Project.objects.all()
        project = list()
        itera = list()
        phase = list()
        closed = []
        for item in p:
            if not item.status:
                closed.append(item)
                continue
            pid = item.id
            project.append(item)
            ph = Phase.objects.get(project_id = pid,status = True)
            i = Iteration.objects.get(phase = ph,status = True)
            itera.append(i)
            phase.append(ph)
        c = Context({
            'user': request.user,
            'prjlist': itera,
            'closed': closed,
            'prjcount': len(itera),
        })
        return render_to_response("man-allprojects.html", c)
    else:
        return HttpResponseRedirect("/")

@login_required
def newIteration(request,pid):
    p = Project.objects.get(id = int(pid))
    ph = Phase.objects.get(project_id = p.id,status = True)
    itera = Iteration.objects.get(phase_id = ph.id,status = True)
    if request.POST['phase'] == "current":
        i = Iteration(phase_id = ph.id,no = itera.no+1,status = True)
        i.start_date = timezone.now()
        i.end_date = timezone.now()
        i.totalDefects =0
        i.totalTime = 0
        i.totalSLOC = 0
        i.save()
        itera.status = False
        itera.save()
    else:
        pha = Phase(project_id = p.id,no = ph.no+1,status=True)
        pha.start_date = timezone.now()
        pha.end_date = timezone.now()
        pha.totalDefects =0
        pha.totalTime = 0
        pha.totalSLOC = 0
        ph.status = False
        pha.save()
        ph.save()
        i = Iteration(phase_id = pha.id,no = 1,status = True)
        i.start_date = timezone.now()
        i.end_date = timezone.now()
        i.totalDefects =0
        i.totalTime = 0
        i.totalSLOC = 0
        i.save()
        itera.status = False

        itera.save()
    return HttpResponseRedirect('/manager/project/'+pid+"/")
@login_required
def setting(request,pid):
    p = Project.objects.get(id = int(pid))
    name = p.name
    parti = []
    for par in Participate.objects.filter(project_id = p.id).all():
        parti.append(par.developer)
    unparti = []
    esloc = p.slocestimate
    epm = p.effortestimate
    yieldrate = p.yieldrate
    for u in User.objects.all():
        if not u.is_staff:
            if u.profile.role == USER_DEVELOPER and u not in parti:
                unparti.append(u)
    desc = p.desc
    #if request.POST.get('action',"") == "":
    print (len(parti),len(unparti))
    if request.method == 'POST':
        if request.POST['action'] == "rename":
            name = request.POST['newname']
            p.name = name
            p.save()
        elif request.POST['action'] == "edit_developer":
            cur = request.POST.getlist("developers")
            for par in Participate.objects.filter(project_id=  p.id).all():
                par.delete()
            print (len(Participate.objects.all()))
            print (cur)
            for c in cur:
                developer  = User.objects.get(id  = int(c))
                par = Participate(project_id = p.id,developer_id = developer.id)
                par.save()
            parti = []
            for par in Participate.objects.filter(project_id = p.id).all():
                parti.append(par.developer)
            unparti = []
            for u in User.objects.all():
                if not u.is_staff:
                    if u.profile.role == USER_DEVELOPER and u not in parti:
                        unparti.append(u)
        elif request.POST['action'] == "edit_description":
            desc = request.POST["description"]
            p.desc = desc
            p.save()
        elif request.POST['action']  == "change_esloc":
            esloc = request.POST["esloc"]
            p.slocestimate = esloc
            p.save()
        elif request.POST['action']  == "change_epm":
            epm = request.POST["epm"]
            p.effortestimate = epm
            p.save()
        elif request.POST['action']  == "change_yield":
            yieldrate = request.POST["yield"]
            p.yieldrate = yieldrate
            p.save()
        elif request.POST['action']  == "delete_project":
        	for ph in Phase.objects.filter(project_id = p.id).all():
        		for itera in Iteration.objects.filter(phase_id = ph.id).all():
        			itera.delete()
        		ph.delete()
        	p.delete()
        	return HttpResponseRedirect("/manager/dashboard/")
        elif request.POST['action']  == "close_project":
            p.status=False
            ph = Phase.objects.get(project_id = p.id,status = True)
            it = Iteration.objects.get(phase_id = ph.id,status = True)
            it.status = False
            ph.status = False
            it.save()
            ph.save()
            p.save()
            return HttpResponseRedirect("/manager/dashboard/")
    c = Context({
        'pid':pid,
        'user':request.user,
        'curname':name,
        'curesloc':esloc,
        'curepm':epm,
        'curyield':yieldrate,
        'curdescription':desc,
        'developerlist':unparti,
        'curdeveloperlist':parti
    })
    return render_to_response("man-setting.html",c)



def editprofile(req):
    return render_to_response("profile.html")

def updateSession(request):
    type = request.POST['type']
    id = int(request.POST['id'])
    if type == 'mng' :#Management session
        s = ManageSession.objects.get(pk=id)
        t = str(request.POST['time'])
        ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
        s.sessionlast = ts
        s.save()
        response = {
            'time' : s.sessionlast,
        }
    elif type == 'dev': #development session
        s=SLOCSession.objects.get(pk=id)
        s.SLOC = int(request.POST['sloc'])
        t = str(request.POST['time'])
        ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
        s.sessionlast = ts
        s.save()
        response = {
            'time' : s.sessionlast,
            'sloc':s.SLOC
        }
    elif type =='rem':
        s=DefectSession.objects.get(pk=id)
        s.defectno = int(request.POST['defectno'])
        t = str(request.POST['time'])
        ts = int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])
        s.sessionlast = ts
        s.save()
        response = {
            'time': s.sessionlast,
            'defectno':s.defectno,
        }
    return HttpResponse(json.dumps(response))

def updateDefect(request):
    id = request.POST['id']
    d = Defects.objects.get(pk=id)
    d.name = request.POST['name']
    d.typed = request.POST ['type']
    d.iterationInjected = Iteration.objects.get(pk = request.POST['iterationInjected'])
    d.iterationRemoved = Iteration.objects.get(pk= request.POST ['iterationRemoved'])
    d.desc = request.POST['desc']
    d.save()
    response = {
        'name':d.name,
        'type':d.typed,
    }
    return HttpResponse(json.dumps(response))


