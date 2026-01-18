from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class UserTests(TestCase):
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

# class UserMoviesTests(TestCase):
#     def setUp(self):
#         """
#         Set up a user and some movies for testing.
#         """
#         self.user = User.objects.create_user(
#             username='movielover',