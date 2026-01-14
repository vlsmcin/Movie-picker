from django.urls import path
from . import views

urlpatterns = [
    path("<str:movie_title>/", views.get_movie_by_title, name="get_movie_by_title"),
]