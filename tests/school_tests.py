import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Director, School
from rest_framework.authtoken.models import Token

class SchoolTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'schools', 'schools']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_get_school(self):

        school = School()
        school.name = "Sound of Software"
        school.save()

        response = self.client.get(f"/schools/{school.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Sound of Software")