from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer
from .services.tmdb_service import fetch_and_store

class MovieByTitleView(APIView):
    def get(self, request, movie_title):
        movies = Movie.objects.filter(title__icontains=movie_title)

        if movies.exists():
            return Response(MovieSerializer(movies, many=True).data)

        try: 
            movies = fetch_and_store(movie_title)
            
            if movies:
                return Response(MovieSerializer(movies, many=True).data)
            
            return Response({'detail': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException:
            return Response({'detail': 'Failed to fetch data from TMDB'}, status=status.HTTP_502_BAD_GATEWAY)
        
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all().distinct()
        return Response(GenreSerializer(genres, many=True).data)