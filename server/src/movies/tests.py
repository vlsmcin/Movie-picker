from django.test import TestCase
from .models import Movie, Genre
from django.core.management import call_command
from django.urls import reverse

# Create your tests here.
class MovieTests(TestCase):
    def test_single_movie_found(self):
        """
        Test to ensure that a single movie can be found by title.
        """
        movie = Movie.objects.create(
            tmdb_id=1,
            title="Inception",
            overview="A mind-bending thriller",
            vote_average=8.8,
            vote_count=21000,
            release_date="2010-07-16",
            popularity=150.0,
            poster_path="/inception.jpg"
        )

        response = self.client.get(reverse('get_movie_by_title', args=['Inception']))
        self.assertContains(response, "Inception")

    def test_similar_movies_found(self):
        """
        Test to ensure that multiple similar movies can be found by title.
        """
        Movie.objects.create(
            tmdb_id=1,
            title="The Matrix",
            overview="A computer hacker learns about the true nature of reality.",
            vote_average=8.7,
            vote_count=17000,
            release_date="1999-03-31",
            popularity=120.0,
            poster_path="/matrix.jpg"
        )
        Movie.objects.create(
            tmdb_id=2,
            title="The Matrix Reloaded",
            overview="The sequel to The Matrix.",
            vote_average=7.2,
            vote_count=13000,
            release_date="2003-05-15",
            popularity=100.0,
            poster_path="/matrix_reloaded.jpg"
        )
        response = self.client.get(reverse('get_movie_by_title', args=['Matrix']))
        self.assertContains(response, "The Matrix")
        self.assertContains(response, "The Matrix Reloaded")

    def test_no_movie_found(self):
        """
        Test to ensure that an appropriate response is given when no movie is found.
        """
        Movie.objects.create(
            tmdb_id=1,
            title="Interstellar",
            overview="A team of explorers travel through a wormhole in space.",
            vote_average=8.6,
            vote_count=14000,
            release_date="2014-11-07",
            popularity=130.0,
            poster_path="/interstellar.jpg"
        )

        response = self.client.get(reverse('get_movie_by_title', args=['NonExistentMovie']))
        self.assertContains(response, "Movie not found", status_code=404)

    def test_find_movie_in_tmdb_api(self):
        """
        Test to ensure that a movie not in the database is fetched from the TMDB API.
        """
        call_command('fill_genres')
        response = self.client.get(reverse('get_movie_by_title', args=['Inception']))
        self.assertContains(response, "Inception")
        self.assertTrue(Movie.objects.filter(title__icontains='Inception').exists())

    def test_movie_with_missing_optional_fields(self):
        """
        Test to ensure that a movie with missing optional can be created too.
        """

        Movie.objects.create(
            tmdb_id=20,
            title="Unknown Movie"
        )

        response = self.client.get(
            reverse('get_movie_by_title', args=['Unknown'])
        )

        self.assertContains(response, "Unknown Movie")

class GenreTests(TestCase):
    def test_all_genres_registered(self):
        """
        Test to ensure that all genres are registered in the database.
        """
        call_command('fill_genres')
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 19)