# users/tests/test_users.py
import json
from django.test import TestCase, Client
from users.schema import schema

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        mutation = '''
        mutation CreateUser($username: String!, $email: String!, $password: String!) {
            createUser(username: $username, email: $email, password: $password) {
                user {
                    id
                    username
                    email
                }
            }
        }
        '''
        variables = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }

        response = self.client.post(
            '/graphql/',  # Ensure this matches your actual GraphQL endpoint
            data=json.dumps({'query': mutation, 'variables': variables}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertEqual(content['data']['createUser']['user']['username'], 'testuser')
        self.assertEqual(content['data']['createUser']['user']['email'], 'testuser@example.com')
