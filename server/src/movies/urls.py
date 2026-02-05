from django.urls import path
from .views import MovieByTitleView, GenreListView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="get_genre_list"),
    path("<str:movie_title>/", MovieByTitleView.as_view(), name="get_movie_by_title"),
]