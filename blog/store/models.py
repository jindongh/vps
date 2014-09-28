from django.db import models
from django.dispatch import dispatcher
from django.db.models import signals

# Create your models here.
class App(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)
    apk = models.FileField(upload_to='./upload/')
    version = models.CharField(max_length=200)
    package = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.name

