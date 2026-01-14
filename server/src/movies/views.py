from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
import os
from .models import Movie, Genre

url = "https://api.themoviedb.org/3"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}

def parse_date(date_str):
    return date_str if date_str else None

def get_movie_by_title(request, movie_title):
    movies = Movie.objects.filter(title__icontains=movie_title)

    if movies.exists():
        return JsonResponse([{
            'tmdb_id': movie.tmdb_id,
            'title': movie.title,
            'overview': movie.overview,
            'vote_average': movie.vote_average,
            'vote_count': movie.vote_count,
            'release_date': movie.release_date,
            'popularity': movie.popularity,
            'poster_path': movie.poster_path,
            'genres': [genre.name for genre in movie.genres.all()]
        } for movie in movies], safe=False)
    else:
        try: 
            response = requests.get(f"{url}/search/movie", headers=headers, params={"query": movie_title})
            response.raise_for_status()
            data = response.json()
            if data['results']:
                movies = []

                for mv in data['results']:
                    movie, created = Movie.objects.get_or_create(
                        tmdb_id=mv['id'],
                        defaults={
                            'title': mv['title'],
                            'overview': mv['overview'],
                            'vote_average': mv['vote_average'],
                            'vote_count': mv['vote_count'],
                            'release_date': parse_date(mv['release_date']),
                            'popularity': mv['popularity'],
                            'poster_path': mv['poster_path']
                        }
                    )

                    genres = [
                        Genre.objects.get(tmdb_id=genre_id)
                        for genre_id in mv.get('genre_ids', [])
                    ]

                    movie.genres.set(genres)

                    movies.append({
                        'tmdb_id': movie.tmdb_id,
                        'title': movie.title,
                        'overview': movie.overview,
                        'vote_average': movie.vote_average,
                        'vote_count': movie.vote_count,
                        'release_date': movie.release_date,
                        'popularity': movie.popularity,
                        'poster_path': movie.poster_path,
                        'genres': [genre.name for genre in movie.genres.all()]
                    })

                return JsonResponse(movies, safe=False)
            else:
                return JsonResponse({'error': 'Movie not found'}, status=404)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)