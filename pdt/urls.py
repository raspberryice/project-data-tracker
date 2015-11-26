from django.conf.urls import url
from . import views

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
]

