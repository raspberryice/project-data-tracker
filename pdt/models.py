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


class Session(models.Model):
    iteration = models.ForeignKey(Iteration)
    developer = models.ForeignKey(Developer)
    start_date = models.DateTimeField(auto_now_add=True)



class DevelopmentSession(Session):
    SLOC = models.IntegerField
    def getSLOC (self,newSLOC):
        self.SLOC = newSLOC


class ManagementSession(Session):
    {

    }


class DefectRemovalSession(Session):
    defectno = models.IntegerField


class Defect(models.Model):
    session=models.ForeignKey(DefectRemovalSession)
    type = models.IntegerField
    iterationInjected= models.ForeignKey(Iteration,related_name='injected')
    iterationRemoved = models.ForeignKey(Iteration,related_name='removed')
    desc = models.CharField(max_length=300)
    status = models.IntegerField


class Timer(models.Model):
    totalTime = models.DurationField
    session = models.OneToOneField(Session)


