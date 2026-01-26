from rest_framework.test import APITestCase
from users.models import User
from django.urls import reverse

# Create your tests here.
class AuthTests(APITestCase):
    def setUp(self):
        """
        Set up a user for authentication tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_user_login(self):
        """
        Test user login to obtain JWT token.
        """
        response = self.client.post(reverse('user-login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Test user login with invalid credentials.
        """
        response = self.client.post(reverse('user-login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)

    def test_user_login_missing_fields(self):
        """
        Test user login with missing fields.
        """
        response = self.client.post(reverse('user-login'), {
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

    def test_user_login_empty_fields(self):
        """
        Test user login with empty fields.
        """
        response = self.client.post(reverse('user-login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

    def test_protected_endpoint_requires_authentication(self):
        """
        Test that a protected endpoint requires authentication.
        """
        response = self.client.get(reverse('user-movies'))
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)

class TokenRefreshTests(APITestCase):
    def setUp(self):
        """
        Set up a user for token refresh tests.
        """
        self.user = User.objects.create_user(
            username='refreshtestuser',
            email='refreshtestuser@example.com',
            password='refreshtestpassword'
        )

    def test_token_refresh(self):
        """
        Test refreshing JWT token.
        """
        login_response = self.client.post(reverse('user-login'), {
            'username': 'refreshtestuser',
            'password': 'refreshtestpassword'
        })
        refresh_token = login_response.data['refresh']

        refresh_response = self.client.post(reverse('auth-refresh'), {
            'refresh': refresh_token
        })
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.data)

    def test_token_refresh_invalid_token(self):
        """
        Test refreshing JWT token with an invalid token.
        """
        refresh_response = self.client.post(reverse('auth-refresh'), {
            'refresh': 'invalidtoken'
        })
        self.assertEqual(refresh_response.status_code, 401)
        self.assertIn('detail', refresh_response.data)

    def test_token_refresh_missing_token(self):
        """
        Test refreshing JWT token with missing token.
        """
        refresh_response = self.client.post(reverse('auth-refresh'), {})
        self.assertEqual(refresh_response.status_code, 400)
        self.assertIn('refresh', refresh_response.data)