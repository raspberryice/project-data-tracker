from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    ROLE_NAMES = (
        (1, 'Developer'),
        (2, 'Manager')
    )
    user = models.OneToOneField(User)
    role = models.IntegerField(choices = ROLE_NAMES)

    def __str__(self):
        return self.user.username + ": " + str(self.role)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Profile.objects.get_or_create(user=instance)

# post_save.connect(create_user_profile, sender=User)

class Project(models.Model):
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200)
    status = models.IntegerField
    totalTime = models.IntegerField
    totalSLOC = models.IntegerField
    totalDefects = models.IntegerField

    def __str__(self):
        return self.name


class Phase(models.Model):
    PHASE_NAMES = (
        (1,'Inception'),
        (2,'Elaboration'),
        (3,'Construction'),
        (4,'Migration')
    )
    project = models.ForeignKey(Project)
    no = models.IntegerField(choices=PHASE_NAMES,default=1)
    status = models.IntegerField
    totalTime = models.IntegerField
    totalSLOC = models.IntegerField
    totalDefects = models.IntegerField
    def __str__(self):
       return self.no


class Iteration(models.Model):
    phase = models.ForeignKey(Phase)
    no = models.IntegerField
    status = models.IntegerField
    totalTime = models.IntegerField
    totalSLOC = models.IntegerField
    totalDefects = models.IntegerField
    def __str__(self):
        return self.no


class Session(models.Model):
    creator = models.ForeignKey(User)
    iteration = models.ForeignKey(Iteration)
    totalTime = models.DurationField


class DevelopmentSession(Session):
    SLOC = models.IntegerField
    def getSLOC (self,newSLOC):
        self.SLOC = newSLOC


class ManagementSession(Session):
    pass


class DefectRemovalSession(Session):
    removed = models.IntegerField


class Defect(models.Model):
    session = models.ForeignKey(DefectRemovalSession)
    type = models.IntegerField
    iterationInjected = models.ForeignKey(Iteration,related_name='injected')
    iterationRemoved = models.ForeignKey(Iteration,related_name='removed')
    desc = models.CharField(max_length=300)
    status = models.IntegerField
