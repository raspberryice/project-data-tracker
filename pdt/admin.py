from django.contrib import admin
from .models import Project,Phase,Iteration,Session,Defect,DevelopmentSession,DefectRemovalSession,ManagementSession

admin.site.register(Project)
admin.site.register(Phase)
admin.site.register(Iteration)
admin.site.register(Session)
admin.site.register(Defect)
admin.site.register(DevelopmentSession)
admin.site.register(DefectRemovalSession)
admin.site.register(ManagementSession)