from rest_framework import serializers
from .models import Movie, Genre

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "overview",
            "vote_average",
            "release_date",
            "poster_path",
            "backdrop_path",
            "genres",
        ]