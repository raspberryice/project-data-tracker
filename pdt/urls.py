from django.conf.urls import url
from pdt import views

urlpatterns = [
	#authorization
	url(r'^$', views.index, name='index'),
	url(r'verify$',views.verify,name='verify'),
	url(r'auth/login/', views.login, name = 'login'),
	url(r'auth/logout/', views.logout, name = 'logout'),
	url(r'auth/profile/$', views.editprofile, name='editprofile'),
	#developer-dashboard
	url(r'developer/dashboard/', views.devdashboard, name = 'devdashboard'),
	url(r'developer/allprojects/$', views.devAllProjects, name = 'devallprojects'),
	#developer-sessions
	url(r'developer/createdev/', views.beginDevelopeSession, name = 'createdev'),
	url(r'developer/enddev/', views.endDevelopeSession, name = 'enddev'),
	url(r'developer/createrem/$',views.beginDefectSession,name="createrem"),
	url(r'developer/endrem/$',views.endDefectSession,name="endrem"),
	url(r'developer/createrem/adddefect/$',views.addDefect,name='add'),
	url(r'developer/createmng/$',views.beginManageSession,name='beginmanage'),
	url(r'developer/endmng/$',views.endManageSession,name='endmanage'),
	#developer-report
	url(r'developer/project/(?P<pid>\d+)/$',views.devProject,name='devproject'),
	url(r'developer/project/(?P<pid>\d+)/report/$',views.devReport,name='devreport'),
	#manager-dashboard
	url(r'manager/dashboard/$',views.mandashboard, name = 'mandashboard'),
	url(r'manager/allprojects/$', views.manAllProjects, name = 'manallprojects'),
	url(r'manager/project/(?P<pid>\d+)/$',views.manProject,name="manproject"),
	url(r'manager/project/(?P<pid>\d+)/report/$',views.manReport,name="manreport"),
	url(r'manager/project/(?P<pid>\d+)/activity/$',views.manActivity,name="manactivity"),
	url(r'manager/project/(?P<pid>\d+)/defect/$',views.manDefect,name="mandefect"),
	#manager-manage-project
	url(r'manager/newproject/$',views.addproject,name='addproject'),
	url(r'manager/project/(?P<pid>\d+)/newiteration/$',views.newIteration,name = 'newiteration'),
	url(r'manager/project/(?P<pid>\d+)/setting/$',views.setting,name="setting"),
]
