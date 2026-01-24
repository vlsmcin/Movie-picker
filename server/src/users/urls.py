from django.urls import path
from .views import UserCreateView, UserMoviesView

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
    path("me/movies/", UserMoviesView.as_view(), name="user-movies"),
]