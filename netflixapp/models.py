from distutils.command.upload import upload
from pyexpat import model
from venv import create
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

AGE_CHOICES = (
    ('All', 'All'),
    ('Kids', 'Kids'),
)

MOVIE_CHOICES = (
    ('seasonal', 'Seasonal'),
    ('single', 'Single'),
)

class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile', blank=True)

class Profile(models.Model):
    name = models.CharField(max_length=1000)
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)
    uuid = models.UUIDField(default=uuid.uuid4)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    evaluation = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(choices=MOVIE_CHOICES, max_length=10)
    video = models.ManyToManyField('Video')
    lowVideo = models.ManyToManyField('VideoLow')
    image = models.ImageField(upload_to='covers')
    image_bg = models.ImageField(upload_to='bg', null=False,blank=False)
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=1000)
    file = models.FileField(upload_to='movies')
    
    def __str__(self):
        return self.title

class Videolow(models.Model):
    title = models.CharField(max_length=1000)
    file = models.FileField(upload_to='movies')
    
    def __str__(self):
        return self.title