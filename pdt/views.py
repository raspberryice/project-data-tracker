from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.contrib import auth
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Profile
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
		user = auth.authenticate(username = req.POST['username'], password = req.POST['password'])
		if user is not None:
			auth.login(req, user)
			if req.user.profile.role == 1:
				return HttpResponseRedirect("/developer/dashboard/")
			else:
				return HttpResponseRedirect("/manager/dashboard/")
		else:
			return render_to_response("login.html", Context({'failed': True}))
	else:
		return render_to_response("login.html", Context({'logged_out': (req.REQUEST.get('prev', '') == '/auth/logout/')}))

def logout(req):
	log_out(req)
	return HttpResponseRedirect("/auth/login/?prev=/auth/logout/")


@login_required
def devdashboard(req):
	if req.user.profile.role == 1:
		prjlist = [
			{
				'name': 'Project 1',
				'curphase': 2,
				'curitr': 3,
			},
			{
				'name': 'Project 2',
				'curphase': 1,
				'curitr': 2
			}
		]
		c = Context({
			'user': req.user,
			'prjlist': prjlist,
		})
		return render_to_response("devdashboard.html", c)
	else:
		return HttpResponseRedirect("/")

@login_required
def mandashboard(req):
	if req.user.profile.role == 2:
		c = Context({
			'user': req.user,
			'prjcount': 3,
		})
		return render_to_response("mandashboard.html", c)
	else:
		return HttpResponseRedirect("/")
