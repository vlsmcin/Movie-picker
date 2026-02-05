import requests
from django.db import transaction
from movies.models import Movie, Genre
import os

TMDB_URL = "https://api.themoviedb.org/3"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}

def parse_date(date_str):
    return date_str if date_str else None

def fetch_and_store(movie_title):
    response = requests.get(f"{TMDB_URL}/search/movie", headers=headers, params={"query": movie_title})
    response.raise_for_status()
    data = response.json()

    movies = []

    with transaction.atomic():
        for mv in data.get('results', []):
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=mv['id'],
                defaults={
                    'title': mv['title'],
                    'overview': mv['overview'],
                    'vote_average': mv['vote_average'],
                    'vote_count': mv['vote_count'],
                    'release_date': parse_date(mv['release_date']),
                    'popularity': mv['popularity'],
                    'poster_path': mv['poster_path'],
                    'backdrop_path': mv.get('backdrop_path'),
                }
            )

            genres = Genre.objects.filter(tmdb_id__in=mv.get('genre_ids', []))

            movie.genres.set(genres)

            movies.append(movie)

    return movies