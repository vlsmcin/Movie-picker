from django.db import models
import requests
import os

API_URL = "https://api.themoviedb.org/3"

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    release_date = models.DateField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField('Genre', related_name='movies')

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name