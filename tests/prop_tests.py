import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Prop, Director, School
from rest_framework.authtoken.models import Token

class PropTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'props', 'schools']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_prop(self):

        url = "/props"

        data = {
            "name": "trampoline",
            "assigned": False
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "trampoline")
        self.assertEqual(json_response["assigned"], False)
    
    def test_get_prop(self):

        prop = Prop()
        prop.name = "trampoline"
        prop.assigned = False
        prop.school = School.objects.get(pk=1)
        prop.save()

        response = self.client.get(f"/props/{prop.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "trampoline")
        self.assertEqual(json_response["assigned"], False)
    
    def test_change_prop(self):

        prop = Prop()
        prop.name = "trampoline"
        prop.assigned = False
        prop.school = School.objects.get(pk=1)
        prop.save()

        data = {
            "name": "ship"
        }

        response = self.client.put(f"/props/{prop.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/props/{prop.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "ship")

    def test_delete_prop(self):

        prop = Prop()
        prop.name = "trampoline"
        prop.assigned = False
        prop.school = School.objects.get(pk=1)
        prop.save()

        response = self.client.delete(f"/props/{prop.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/props/{prop.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)