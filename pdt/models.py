from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser

class Project(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200)
    status = models.BooleanField()
    totalTime = models.IntegerField()
    totalSLOC = models.IntegerField()
    totalDefects =models.IntegerField()

    def __str__ (self):
        return self.name
class Profile(models.Model):
    user = models.OneToOneField(User)
    ROLE_NAMES = (
        (1, 'Developer'),
        (2, 'Manager')
    )
    role = models.IntegerField(choices = ROLE_NAMES)
    def __str__(self):
        return self.user.username + ": " + str(self.role)
        
class Phase(models.Model):
    PHASE_NAMES = (
        (1,'Inception'),
        (2,'Elaboration'),
        (3,'Construction'),
        (4,'Migration')
    )
    project = models.ForeignKey(Project)
    no = models.IntegerField(choices=PHASE_NAMES,default=1)
    status = models.BooleanField()
    totalTime = models.IntegerField()
    totalSLOC = models.IntegerField()
    totalDefects = models.IntegerField()
    def __str__(self):
       return self.project.name+"-"+str(self.no)

class Iteration(models.Model):
    phase = models.ForeignKey(Phase)
    no= models.IntegerField()
    status = models.BooleanField()
    totalTime = models.IntegerField()
    totalSLOC = models.IntegerField()
    totalDefects = models.IntegerField()
    def __str__(self):
        return self.phase.project.name+"-"+str(self.phase.no)+"-"+str(self.no)

class SLOCSession(models.Model):
    iteration = models.ForeignKey(Iteration)
    developer = models.ForeignKey(User)
    start_date = models.DateTimeField(auto_now_add=True)
    sessionlast = models.IntegerField()
    SLOC = models.IntegerField()

# class DefectSession(models.Model):
#     iteration = models.ForeignKey(Iteration)
#     developer = models.ForeignKey(User,related_name='defect')
#     start_date = models.DateTimeField(auto_now_add=True)
#     sessionlast = models.IntegerField
#     defectno = models.IntegerField


class ManageSession(models.Model):
    iteration = models.ForeignKey(Iteration)
    manager = models.ForeignKey(User)
    start_date = models.DateTimeField(auto_now_add=True)
    sessionlast = models.IntegerField

# class Defects(models.Model):
#     session=models.ForeignKey(DefectSession)
#     typed = models.IntegerField
#     iterationInjected = models.ForeignKey(Iteration,related_name='injected')
#     iterationRemoved = models.ForeignKey(Iteration,related_name='removed')
#     desc = models.CharField(max_length=300)
#     status = models.IntegerField

class Participate(models.Model):
    developer = models.ForeignKey(User)
    project = models.ForeignKey(Project)


