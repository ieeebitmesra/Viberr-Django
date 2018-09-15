from django.db import models
from django.urls import reverse
import os
from django.contrib.auth.models import Permission, User

# Create your models here.

class Album(models.Model):
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	artist = models.CharField(max_length=250)
	album_title = models.CharField(max_length=500)
	genre = models.CharField(max_length=100)
	album_logo = models.FileField(null=True)
	def __str__(self):
		return self.album_title + '-' + self.artist

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk':self.pk})

class Song(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	song_title = models.CharField(max_length=250)
	song = models.FileField(null=True)
	is_favorite = models.BooleanField(default=False)

	def filename(self):
		return os.path.basename(self.song.name)
	
	def __str__(self):
		return self.song_title

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk':self.album.pk})