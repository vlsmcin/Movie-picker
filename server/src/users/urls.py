from django.urls import path
from .views import UserCreateView, UserMoviesView

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
    path("<int:user_id>/movies/", UserMoviesView.as_view(), name="user-movies"),
]