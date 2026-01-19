from movies.models import Movie
from .models import User, UserMovies
from .serializers import UserSerializer, UserMoviesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserMoviesView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_movies = UserMovies.objects.filter(user=user).select_related('movie')
        serializer = UserMoviesSerializer(user_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if UserMovies.objects.filter(user=user, movie__id=movie_id).exists():
            return Response({"detail": "Movie already associated with user"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        
        watched = request.data.get("watched")
        in_watchlist = request.data.get("in_watchlist")

        if watched is None and in_watchlist is None:
            return Response({"detail": "At least one of watched or in_watchlist must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        user_movie, created = UserMovies.objects.get_or_create(user=user, movie=movie)

        if watched is not None:
            user_movie.watched = watched
        if in_watchlist is not None:
            user_movie.in_watchlist = in_watchlist
        
        user_movie.save()

        serializer = UserMoviesSerializer(user_movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        movie_id = request.query_params.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_movies = UserMovies.objects.get(user=user, movie__id=movie_id)
        except UserMovies.DoesNotExist:
            return Response({"detail": "Movie not associated with user"}, status=status.HTTP_404_NOT_FOUND)
        
        user_movies.delete()
        return Response({"detail": "Movie removed from user"}, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_movie = UserMovies.objects.get(user=user, movie__id=movie_id)
        except UserMovies.DoesNotExist:
            return Response({"detail": "Movie not associated with user"}, status=status.HTTP_404_NOT_FOUND)
        
        watched = request.data.get("watched")
        in_watchlist = request.data.get("in_watchlist")

        if watched is None and in_watchlist is None:
            return Response({"detail": "At least one of watched or in_watchlist must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        if watched is not None:
            user_movie.watched = watched
        if in_watchlist is not None:
            user_movie.in_watchlist = in_watchlist
        
        user_movie.save()

        serializer = UserMoviesSerializer(user_movie)
        return Response(serializer.data, status=status.HTTP_200_OK)