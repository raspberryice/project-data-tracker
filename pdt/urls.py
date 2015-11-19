from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index, name = 'index'),
	url(r'auth/login/$', login, name = 'login'),
	url(r'auth/logout/$', logout, name = 'logout'),
	url(r'developer/dashboard/$', devdashboard, name = 'devdashboard'),
	url(r'developer/createdev/', beginDevelopSession, name = 'createdev'),
	url(r'developer/enddev/', endDevelopSession, name = 'enddev'),
	url(r'manager/dashboard/$', mandashboard, name = 'mandashboard'),
	url(r'manager/report/(?P<pid>\d+)/$',manReport,name="manreport"),

]
