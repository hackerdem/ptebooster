from django.db import models

# Create your models here.

class Recommendation(models.Model):
    topic = models.CharField(max_length=25, null=False, blank=False)
    class Meta:
        abstract = True


class Video(Recommendation):
    video_url= models.CharField(max_length=100,null=False,blank=False)
