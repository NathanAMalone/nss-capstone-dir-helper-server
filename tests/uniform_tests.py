import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Director, Uniform, School
from rest_framework.authtoken.models import Token

class UniformTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'schools', 'uniforms']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_create_uniform(self):

        url = "/uniforms"

        data = {
            "uniform_number": 37,
            "size": "large",
            "out_for_cleaning": False,
            "assigned": True
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["uniform_number"], 37)
        self.assertEqual(json_response["size"], "large")
        self.assertEqual(json_response["out_for_cleaning"], False)
        self.assertEqual(json_response["assigned"], True)

    def test_get_uniform(self):

        uniform = Uniform()
        uniform.uniform_number = 37
        uniform.size = "large"
        uniform.out_for_cleaning = False
        uniform.assigned = True
        uniform.school = School.objects.get(pk=1)
        uniform.save()

        response = self.client.get(f"/uniforms/{uniform.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["uniform_number"], 37)
        self.assertEqual(json_response["size"], "large")
        self.assertEqual(json_response["out_for_cleaning"],False)
        self.assertEqual(json_response["assigned"], True)

    def test_change_uniform(self):

        uniform = Uniform()
        uniform.uniform_number = 37
        uniform.size = "large"
        uniform.out_for_cleaning = False
        uniform.assigned = True
        uniform.school = School.objects.get(pk=1)
        uniform.save()

        data = {
            "uniform_number": 39,
            "size": "medium",
            "out_for_cleaning": True,
        }

        response = self.client.put(f"/uniforms/{uniform.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/uniforms/{uniform.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["uniform_number"], 39)
        self.assertEqual(json_response["size"], "medium")
        self.assertEqual(json_response["out_for_cleaning"], True)
        
    def test_delete_uniform(self):

        uniform = Uniform()
        uniform.uniform_number = 37
        uniform.size = "large"
        uniform.out_for_cleaning = False
        uniform.assigned = True
        uniform.school = School.objects.get(pk=1)
        uniform.save()

        response = self.client.delete(f"/uniforms/{uniform.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/uniforms/{uniform.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)