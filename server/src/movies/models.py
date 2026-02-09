from django.db import models
import requests
import os

API_URL = "https://api.themoviedb.org/3"

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    overview = models.TextField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='movies', blank=True)

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name