from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index, name = 'index'),
	url(r'auth/login/$', login, name = 'login'),
	url(r'auth/logout/$', logout, name = 'logout'),
	url(r'auth/profile/$', editprofile, name='editprofile'),
    url(r'developer/dashboard/$', devdashboard, name = 'devdashboard'),
	url(r'developer/allprojects/$', devAllProjects, name = 'devallprojects'),
    url(r'developer/create_defect/',create_defect,name="create_defect"),
	url(r'developer/createdev/', beginDevelopSession, name = 'createdev'),
	url(r'developer/enddev/', endDevelopSession, name = 'enddev'),
	url(r'developer/createrem/',beginDefectSession,name='createrem'),
    url(r'developer/endrem/',endDefectSession,name='endrem'),
	url(r'developer/createmng/',beginManageSession,name='createmng'),
    url(r'developer/endmng/',endManageSession,name='endmng'),
	url(r'developer/project/(?P<pid>\d+)/$',devProject,name='devproject'),
	url(r'developer/project/(?P<pid>\d+)/report/$',devReport,name='devreport'),

	url(r'manager/dashboard/$', mandashboard, name = 'mandashboard'),
	url(r'manager/newproject/$', mannewproject, name = 'mannewproject'),
	url(r'manager/allprojects/$', manAllProjects, name = 'manallprojects'),
	url(r'manager/project/(?P<pid>\d+)/$',manProject,name="manproject"),
	url(r'manager/project/(?P<pid>\d+)/newiteration/$',manNewIteration,name="mannewiteration"),
	url(r'manager/project/(?P<pid>\d+)/report/$',manReport,name="manreport"),
	url(r'manager/project/(?P<pid>\d+)/activity/$',manActivity,name="manactivity"),
	url(r'manager/project/(?P<pid>\d+)/defect/$',manDefect,name="mandefect"),
	url(r'manager/project/(?P<pid>\d+)/setting/$',manSetting,name="mansetting"),
]
