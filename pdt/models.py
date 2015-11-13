from django.db import models

# Create your models here.
class Comment(models.Model):
	name = models.CharField(max_length=30)
	pub_date = models.DateTimeField('date published')
	content = models.CharField(max_length=2000)

