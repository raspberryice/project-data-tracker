from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

# To Be Changed! Use User Groups.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
# To Be Changed! Use User Groups.
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin) # To Be Changed! Use User Groups.
admin.site.register(Project)
admin.site.register(Phase)
admin.site.register(Iteration)
#admin.site.register(Defect)
admin.site.register(SLOCSession)
admin.site.register(Profile)
#admin.site.register(DefectRemovalSession)
#admin.site.register(ManagementSession)
