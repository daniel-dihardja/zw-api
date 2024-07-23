# users/tests/test_users.py
import json
from graphene_django.utils.testing import GraphQLTestCase
from users.schema import schema

class UserTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

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

        response = self.query(
            mutation,
            variables=variables
        )

        # Debug response
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Content:", response.content)

        # Handle redirect
        if response.status_code == 301:
            location = response.headers['Location']
            response = self.client.post(
                location,
                data=json.dumps({'query': mutation, 'variables': variables}),
                content_type='application/json'
            )
            print("Redirect Status Code:", response.status_code)
            print("Redirect Content:", response.content)

        # Check response
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertEqual(content['data']['createUser']['user']['username'], 'testuser')
        self.assertEqual(content['data']['createUser']['user']['email'], 'testuser@example.com')
