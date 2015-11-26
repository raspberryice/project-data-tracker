from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.contrib import auth
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import *
from django.utils import timezone


# Create your views here.

def index(req):
    if req.user.is_authenticated():
        if req.user.profile.role == 1:
            return HttpResponseRedirect("/developer/dashboard/")
        else:
            return HttpResponseRedirect("/manager/dashboard/")
    else:
        return HttpResponseRedirect("/auth/login/")


def login(req):
    if req.POST:
        user = auth.authenticate(username=req.POST['username'], password=req.POST['password'])
        if user is not None:
            auth.login(req, user)
            if req.user.profile.role == 1:
                return HttpResponseRedirect("/developer/dashboard/")
            else:
                return HttpResponseRedirect("/manager/dashboard/")
        else:
            return render_to_response("login.html", Context({'failed': True}))
    else:
        return render_to_response("login.html", Context({'logged_out': (req.GET.get('prev', '') == '/auth/logout/')}))


def logout(req):
    log_out(req)
    return HttpResponseRedirect("/auth/login/?prev=/auth/logout/")


@login_required
def devdashboard(req):
    if req.user.profile.role == 1:
        prjlist = [
            {
                'name': 'Project 1',
                'id': 1001,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 2',
                'id': 1002,
                'curphase': 1,
                'curitr': 2
            },
            {
                'name': 'Project 3',
                'id': 1003,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 4',
                'id': 1004,
                'curphase': 1,
                'curitr': 2
            },
            {
                'name': 'Project 5',
                'id': 1005,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 6',
                'id': 1006,
                'curphase': 1,
                'curitr': 2
            },
        ]
        c = Context({
            'user': req.user,
            'prjlist': prjlist,
            'totprjcnt': 10,  # total number of projects the developer attended
            'justcompleted': (req.GET.get('prev', '') == '/developer/enddev/'),
        })
        return render_to_response("dev-dashboard.html", c)
    else:
        return HttpResponseRedirect("/")


@login_required
def beginDevelopSession(request):
    prjid = request.POST.get("prjid", -1)
    if prjid != -1:
        # create a development session
        # ...
        # pass the sessionid
        c = Context({'prjname': "Project 1", 'phasename': "Elaboration", 'itrno': 3, 'user': request.user, 'sid': 1023})
        return render_to_response("dev-action.html", c)
    return HttpResponseRedirect("/")


@login_required
def endDevelopSession(request):
    # do the saving
    # s = SLOCSesson.objects.get(id = request.id)
    # s.sessionlast = request.POST['time']
    # s.SLOC = request.POST['SLOC']
    # s.save()
    print("sid: " + request.POST['sid'])  # development session id
    print("sloc: " + request.POST['sloc'])
    print("time: " + request.POST['time'] + ", type: ")
    print(type(request.POST['time']))
    return HttpResponseRedirect('/developer/dashboard/?prev=/developer/endrem/')


@login_required
def beginDefectSession(request):
    pid = request.POST['prjid']
    # project = get_object_or_404(Project, pk=pid)
    # create session
    # add session to project's current iteration
    # pass the session id
    c = {
        'prjname': "Project 1",
        'phasename': "Elaboration",
        'itrno': 3,
        'sid': 1011,
    }
    return render(request, "dev-defect.html", c)

@login_required
def endDefectSession(request):
    # save session
    return HttpResponseRedirect('/developer/dashboard/?prev=/developer/enddef/')


@login_required
def beginManageSession(request):
    pid = request.POST['prjid']
    # project = get_object_or_404(Project, pk=pid)
    # create session
    # add session to project's current iteration
    # pass the session id
    c = {
        'prjname': "Project 1",
        'phasename': "Elaboration",
        'itrno': 3,
        'sid': 1011,
    }
    return render(request, "dev-manage.html", c)

@login_required
def endManageSession(request):
     # save session
    return HttpResponseRedirect('/developer/dashboard/?prev=/developer/endman/')

@login_required
def mandashboard(req):
    if req.user.profile.role == 2:
        prjlist = [
            {
                'name': 'Project 1',
                'id': 1001,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 2',
                'id': 1002,
                'curphase': 1,
                'curitr': 2
            },
            {
                'name': 'Project 3',
                'id': 1003,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 4',
                'id': 1004,
                'curphase': 1,
                'curitr': 2
            },
            {
                'name': 'Project 5',
                'id': 1005,
                'curphase': 2,
                'curitr': 3,
            },
            {
                'name': 'Project 6',
                'id': 1006,
                'curphase': 1,
                'curitr': 2
            },
        ]
        c = Context({
            'user': req.user,
            'prjlist': prjlist,
            'prjcount': 6,
        })
        return render_to_response("man-dashboard.html", c)
    else:
        return HttpResponseRedirect("/")


##view report
@login_required
def manReport(req, pid):
    if req.user.profile.role == 2:
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
        return render_to_response("man-report.html", c)
    else:
        return HttpResponseRedirect("/")


@login_required
def manProject(req, pid):
    if req.user.profile.role == 2:
        # get data of project(id = pid)

        c = Context({
            'user': req.user,
            'prjname': "Project 3",
            'curphase': 2,
            'curitr': 3,
            'tottime': 30,  # days from project creation to today
            'totsloc': 2345,
            'totslocesti': 35,  # stands for 35%
            'personmonths': 20,
            'pmesti': 30,
            'avesloc': 117,
            'iterationclosed': True
        })
        return render_to_response("man-project.html", c)
    else:
        return HttpResponseRedirect("/")

@login_required
def mannewproject(req):
    if req.user.profile.role == 2:
        if req.method == 'POST':
            print ("Create a new project: ")
            print (req.POST.getlist("developers", []))
            return HttpResponseRedirect("/")
        else:
            developerlist = [
                {
                    'id': 1001,
                    'name': "Harry Potter"
                },
                {
                    'id': 1002,
                    'name': "Albus Dumbledore"
                },
                {
                    'id': 1003,
                    'name': "Zoey Lee"
                },
                {
                    'id': 1004,
                    'name': "Monad"
                },
                {
                    'id': 1005,
                    'name': "Curry"
                },
                {
                    'id': 1006,
                    'name': "Haskell"
                }
            ]
            return render_to_response("man-newproject.html", Context({'user': req.user, 'developerlist': developerlist}))
    else:
        return HttpResponseRedirect("/")

def manNewIteration(req, pid):
    if req.user.profile.role == 2 and req.method == 'POST':
        print ("new iteration at", req.POST.get("phase"), "phase")
        # do something

    return HttpResponseRedirect("/manager/project/" + pid)
