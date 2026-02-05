from rest_framework.test import APITestCase
from users.models import User
from .models import Movie, Genre
from django.core.management import call_command
from django.urls import reverse

# Create your tests here.
class MovieTests(APITestCase):
    def setUp(self):
        """
        Set up authentication for the tests.
        """
        self.user = User.objects.create_user(
            username='movielover',
            email='movielover@example.com',
            password='movieloverpassword'
        )

        response = self.client.post(reverse('user-login'), {
            'username': 'movielover',
            'password': 'movieloverpassword'
        })

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_single_movie_found(self):
        """
        Test to ensure that a single movie can be found by title.
        """
        response = self.client.get(reverse('get_movie_by_title', args=['Inception']))

        self.assertContains(response, "title")
        self.assertContains(response, "overview")
        self.assertContains(response, "vote_average")
        self.assertContains(response, "release_date")
        self.assertContains(response, "poster_path")
        self.assertContains(response, "backdrop_path")
        self.assertContains(response, "genres")

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
            poster_path="/matrix.jpg",
            backdrop_path="/matrix_backdrop.jpg"
        )
        Movie.objects.create(
            tmdb_id=2,
            title="The Matrix Reloaded",
            overview="The sequel to The Matrix.",
            vote_average=7.2,
            vote_count=13000,
            release_date="2003-05-15",
            popularity=100.0,
            poster_path="/matrix_reloaded.jpg",
            backdrop_path="/matrix_reloaded_backdrop.jpg"
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
            poster_path="/interstellar.jpg",
            backdrop_path="/interstellar_backdrop.jpg"
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
        Test to ensure that a movie with missing optional fields can be created too.
        """

        Movie.objects.create(
            tmdb_id=20,
            title="Unknown Movie",
            backdrop_path="/unknown_backdrop.jpg"
        )

        response = self.client.get(
            reverse('get_movie_by_title', args=['Unknown'])
        )

        self.assertContains(response, "Unknown Movie")

    def test_multiple_genre_names(self):
        """
        Test to ensure that a movie with multiple genres returns all genre names.
        """
        genre1 = Genre.objects.create(tmdb_id=28, name="Action")
        genre2 = Genre.objects.create(tmdb_id=12, name="Adventure")

        movie = Movie.objects.create(
            tmdb_id=100,
            title="Action Adventure Movie",
            backdrop_path="/action_adventure_backdrop.jpg"
        )
        movie.genres.add(genre1, genre2)

        response = self.client.get(
            reverse('get_movie_by_title', args=['Action Adventure Movie'])
        )

        self.assertContains(response, "Action")
        self.assertContains(response, "Adventure")

class GenreTests(APITestCase):
    def setUp(self):
        """
        Set up authentication for the tests, and add all genres to the database.
        """
        self.user = User.objects.create_user(
            username='movielover',
            email='movielover@example.com',
            password='movieloverpassword'
        )

        response = self.client.post(reverse('user-login'), {
            'username': 'movielover',
            'password': 'movieloverpassword'
        })

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        call_command('fill_genres')

    def test_all_genres_registered(self):
        """
        Test to ensure that all genres are registered in the database.
        """
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 19)

    def test_genre_list_endpoint(self):
        """
        Test to ensure that the genre list endpoint returns all genres.
        """
        response = self.client.get(reverse('get_genre_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 19)