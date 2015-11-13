from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template import Context
from models import Comment
# Create your views here.
def index(req):
	clist = Comment.objects.all()
	c = Context({"clist": clist,})
	return render_to_response("index.html", c)

def add(req):
	if req.POST:
		post = req.POST
		newcomment = Comment(name = post['name'], content = post['content'])
		newcomment.save()
		return HttpResponseRedirect('../')
	return render_to_response('add.html')