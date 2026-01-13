from django.urls import path
from . import views

urlpatterns = [
    path("movies/<str:movie_title>", views.get_movie_by_title, name="movie_list"),
]