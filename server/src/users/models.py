from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    movies = models.ManyToManyField('movies.Movie', through='UserMovies', related_name='users', blank=True)

    def __str__(self):
        return self.username
    
class UserMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_movies')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='movie_users')
    watched = models.BooleanField(default=False)
    in_watchlist = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'movie')