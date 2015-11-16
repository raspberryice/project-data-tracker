from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200)
    status = models.IntegerField
    totalTime = models.IntegerField
    totalSLOC = models.IntegerField
    totalDefects =models.IntegerField

    def __str__ (self):
        return self.name

class User(models.Model):
    userid = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)

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
    no= models.IntegerField
    status = models.IntegerField
    totalTime = models.IntegerField
    totalSLOC = models.IntegerField
    totalDefects = models.IntegerField
    def __str__(self):
        return self.no
class Developer(models.Model):
    name = models.CharField(max_length = 30)
    user = models.ForeignKey(User)

class Session(models.Model):
    iteration = models.ForeignKey(Iteration)
    developer = models.ForeignKey(Developer)
    start_date = models.DateTimeField(auto_now_add=True)
    sessionlast = models.IntegerField
    
class DefectSession(Session):
    defectno = models.IntegerField

class SLOCSession(Session):
    SLOC = models.IntegerField
class ManageSession(Session):
    pass
class Defect(models.Model):
    session=models.ForeignKey(DefectSession)
    type = models.IntegerField
    iterationInjected = models.ForeignKey(Iteration,related_name='injected')
    iterationRemoved = models.ForeignKey(Iteration,related_name='removed')
    desc = models.CharField(max_length=300)
    status = models.IntegerField

class Participate(models.Model):
    developer = models.ForeignKey(Developer)
    project = models.ForeignKey(Project)



class Manager(Developer):
    pass


