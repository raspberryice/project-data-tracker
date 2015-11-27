from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(Project)
admin.site.register(Participate)
admin.site.register(Phase)
admin.site.register(Iteration)
admin.site.register(SLOCSession)
admin.site.register(DefectSession)
admin.site.register(ManageSession)


