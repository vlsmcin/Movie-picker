from django.urls import path
from .views import MovieByTitleView

urlpatterns = [
    path("<str:movie_title>/", MovieByTitleView.as_view(), name="get_movie_by_title"),
]