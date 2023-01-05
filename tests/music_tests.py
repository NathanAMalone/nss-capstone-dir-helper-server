import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Music, Director, School
from rest_framework.authtoken.models import Token

class MusicTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'music', 'schools']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_music(self):

        url = "/music"

        data = {
            "name": "In Dreams",
            "part": "trombone",
            "assigned": False
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "In Dreams")
        self.assertEqual(json_response["part"], "trombone")
        self.assertEqual(json_response["assigned"], False)
    
    def test_get_music(self):

        music = Music()
        music.name = "In Dreams"
        music.part = "trombone"
        music.assigned = False
        music.school = School.objects.get(pk=1)
        music.save()

        response = self.client.get(f"/music/{music.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "In Dreams")
        self.assertEqual(json_response["part"], "trombone")
        self.assertEqual(json_response["assigned"], False)
    
    def test_change_music(self):

        music = Music()
        music.name = "In Dreams"
        music.part = "trombone"
        music.assigned = False
        music.school = School.objects.get(pk=1)
        music.save()

        data = {
            "name": "In Dreams",
            "part": "tuba",
        }

        response = self.client.put(f"/music/{music.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/music/{music.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "In Dreams")
        self.assertEqual(json_response["part"], "tuba")

    def test_delete_music(self):

        music = Music()
        music.name = "In Dreams"
        music.part = "trombone"
        music.assigned = False
        music.school = School.objects.get(pk=1)
        music.save()

        response = self.client.delete(f"/music/{music.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/music/{music.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)