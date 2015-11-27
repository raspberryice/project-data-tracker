from django.conf.urls import url
import pdt.views as views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'verify$',views.verify,name='verify'),
	url(r'auth/login/', views.login, name = 'login'),
	url(r'auth/logout/', views.logout, name = 'logout'),
	url(r'developer/dashboard/', views.devdashboard, name = 'devdashboard'),
	url(r'developer/createdev/', views.beginDevelopeSession, name = 'createdev'),
	url(r'developer/enddev/', views.endDevelopeSession, name = 'enddev'),
	url(r'manager/dashboard/$',views.mandashboard, name = 'mandashboard'),
	url(r'manager/project/(?P<pid>\d+)/$',views.manProject,name="manproject"),
	url(r'manager/project/(?P<pid>\d+)/report/$',views.manReport,name="manreport"),
	url(r'developer/createrem/$',views.beginDefectSession,name="createrem"),
	url(r'developer/endrem/$',views.endDefectSession,name="endrem"),
	url(r'developer/createrem/adddefect/$',views.addDefect,name='add'),
	url(r'manager/newproject/$',views.addproject,name='addproject'),
#newly added
	
	url(r'developer/allprojects/$', views.devAllProjects, name = 'devallprojects'),
	url(r'developer/createmng/',views.beginManageSession,name='createmng'),
    url(r'developer/endmng/',views.endManageSession,name='endmng'),
	url(r'developer/project/(?P<pid>\d+)/$',views.devProject,name='devproject'),
	url(r'developer/project/(?P<pid>\d+)/report/$',views.devReport,name='devreport'),

	
	url(r'manager/allprojects/$', views.manAllProjects, name = 'manallprojects'),
	url(r'manager/project/(?P<pid>\d+)/$',views.manProject,name="manproject"),
	#url(r'manager/project/(?P<pid>\d+)/newiteration/$',views.manNewIteration,name="mannewiteration"),
	url(r'manager/project/(?P<pid>\d+)/activity/$',views.manActivity,name="manactivity"),
	url(r'manager/project/(?P<pid>\d+)/defect/$',views.manDefect,name="mandefect"),
	url(r'manager/project/(?P<pid>\d+)/setting/$',views.manSetting,name="mansetting"),
]