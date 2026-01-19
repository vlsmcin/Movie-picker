from rest_framework.test import APITestCase
from django.urls import reverse
from movies.models import Movie
from .models import User, UserMovies

# Create your tests here.
class UserTests(APITestCase):
    def test_create_user(self):
        """
        Test to ensure that a user can be created successfully.
        """
        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_create_user_missing_email(self):
        """
        Test to ensure that user creation fails when required fields are missing.
        """
        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'password': 'securepassword123'
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_password(self):
        """
        Test to ensure that user creation fails when password is missing.
        """
        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'email': 'testuser@example.com'
        })

        self.assertEqual(response.status_code, 400)

    def test_user_creation_duplicate_username(self):
        """
        Test to ensure that user creation fails when username already exists.
        """
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword123'
        )

        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password': 'anotherpassword123'
        })

        self.assertEqual(response.status_code, 400)

class UserMoviesTests(APITestCase):
    def setUp(self):
        """
        Set up a user and authenticate for the tests.
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
    
    def test_get_user_movies_empty(self):
        """
        Test to ensure that getting movies for a user with no movies returns an empty list.
        """
        response = self.client.get(reverse('user-movies'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_user_movies(self):
        """
        Test to ensure that getting movies for a user with movies returns the correct data.
        """
        movie1 = Movie.objects.create(
            tmdb_id=1,
            title="Test Movie 1",
            overview="A movie for testing.",
            vote_average=8.5,
            release_date="2023-01-01",
            poster_path="/testposter1.jpg"
        )
        movie2 = Movie.objects.create(
            tmdb_id=2,
            title="Test Movie 2",
            overview="Another movie for testing.",
            vote_average=7.5,
            release_date="2023-02-01",
            poster_path="/testposter2.jpg"
        )

        UserMovies.objects.create(user=self.user, movie=movie1, watched=True, in_watchlist=False)
        UserMovies.objects.create(user=self.user, movie=movie2, watched=False, in_watchlist=True)

        response = self.client.get(reverse('user-movies'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_add_movie_to_user_missing_movie_id(self):
        """
        Test to ensure that adding a movie without providing movie_id returns 400.
        """
        response = self.client.post(reverse('user-movies'), {})
        self.assertEqual(response.status_code, 400)

    def test_duplicate_add_movie_to_user(self):
        """
        Test to ensure the same movie cannot be added twice to the same user.
        """
        movie = Movie.objects.create(
                tmdb_id=1,
                title="Test Movie",
                overview="A movie for testing.",
                vote_average=8.5,
                release_date="2023-01-01",
                poster_path="/testposter.jpg"
            )
        
        response = self.client.post(reverse('user-movies'), {
            'movie_id': movie.id,
            'watched': True,
            'in_watchlist': False
        })

        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('user-movies'), {
            'movie_id': movie.id,
            'watched': False,
            'in_watchlist': True
        })

        self.assertEqual(response.status_code, 400)

    def test_add_movie_to_nonexistent_movie(self):
        """
        Test to ensure that adding a non-existent movie to a user returns 404.
        """
        response = self.client.post(reverse('user-movies'), {
            'movie_id': 9999
        })

        self.assertEqual(response.status_code, 404)

    def test_add_movie_to_user_no_flags(self):
        """
        Test to ensure that adding a movie without watched or in_watchlist flags returns 400.
        """
        movie = Movie.objects.create(
            tmdb_id=1,
            title="Test Movie",
            overview="A movie for testing.",
            vote_average=8.5,
            release_date="2023-01-01",
            poster_path="/testposter.jpg"
        )

        response = self.client.post(reverse('user-movies'), {
            'movie_id': movie.id
        })

        self.assertEqual(response.status_code, 400)

    def test_add_movie_to_user(self):
        """
        Test to ensure that a movie can be added to a user's list successfully.
        """
        movie = Movie.objects.create(
            tmdb_id=1,
            title="Test Movie",
            overview="A movie for testing.",
            vote_average=8.5,
            release_date="2023-01-01",
            poster_path="/testposter.jpg"
        )

        response = self.client.post(reverse('user-movies'), {
            'movie_id': movie.id,
            'watched': True,
            'in_watchlist': False
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['movie']['id'], movie.id)
        self.assertTrue(response.data['watched'])
        self.assertFalse(response.data['in_watchlist'])
        self.assertTrue(UserMovies.objects.filter(user=self.user, movie=movie).exists())

    def test_remove_movie_from_user_not_associated(self):
        """
        Test to ensure that removing a movie not associated with the user returns 404.
        """
        movie = Movie.objects.create(
            tmdb_id=2,
            title="Another Test Movie",
            overview="Another movie for testing.",
            vote_average=7.5,
            release_date="2023-02-01",
            poster_path="/anothertestposter.jpg"
        )

        response = self.client.delete(
            reverse('user-movies') + f'?movie_id={movie.id}'
        )

        self.assertEqual(response.status_code, 404)
    
    def test_remove_movie_from_user(self):
        """
        Test to ensure that a movie can be removed from a user's list successfully.
        """
        movie = Movie.objects.create(
            tmdb_id=4,
            title="Removable Test Movie",
            overview="A removable movie for testing.",
            vote_average=5.5,
            release_date="2023-04-01",
            poster_path="/removabletestposter.jpg"
        )

        UserMovies.objects.create(user=self.user, movie=movie, watched=True, in_watchlist=True)

        response = self.client.delete(
            reverse('user-movies') + f'?movie_id={movie.id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserMovies.objects.filter(user=self.user, movie=movie).exists())

    def test_remove_movie_missing_movie_id(self):
        """
        Test to ensure that removing a movie without providing movie_id returns 400.
        """
        response = self.client.delete(reverse('user-movies'))
        self.assertEqual(response.status_code, 400)

    def test_patch_movie_flags(self):
        """
        Test to ensure that updating watched and in_watchlist flags works correctly.
        """
        movie = Movie.objects.create(
            tmdb_id=5,
            title="Patchable Test Movie",
            overview="A patchable movie for testing.",
            vote_average=9.0,
            release_date="2023-05-01",
            poster_path="/patchabletestposter.jpg"
        )

        UserMovies.objects.create(user=self.user, movie=movie, watched=False, in_watchlist=True)

        response = self.client.patch(reverse('user-movies'), {
            'movie_id': movie.id,
            'watched': True
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['watched'])
        self.assertTrue(response.data['in_watchlist'])
        self.assertTrue(UserMovies.objects.filter(user=self.user, movie=movie, watched=True).exists())

    def test_patch_movie_flags_nonexistent_movie(self):
        """
        Test to ensure that updating flags for a non-existent movie returns 404.
        """
        response = self.client.patch(reverse('user-movies'), {
            'movie_id': 9999,
            'watched': True
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)

    def test_patch_movie_flags_no_flags(self):
        """
        Test to ensure that updating flags without providing any flags returns 400.
        """
        movie = Movie.objects.create(
            tmdb_id=7,
            title="No Flags Patch Movie",
            overview="A movie for testing no flags patch.",
            vote_average=3.5,
            release_date="2023-07-01",
            poster_path="/noflagspatchmovieposter.jpg"
        )

        UserMovies.objects.create(user=self.user, movie=movie, watched=False, in_watchlist=False)

        response = self.client.patch(reverse('user-movies'), {
            'movie_id': movie.id
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)