import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Student, Director, School, Instrument
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class StudentTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'students', 'schools', 
        'uniforms', 'props', 'instruments', 'music']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_student(self):

        new_user = User.objects.create_user(
                username="test@email.com",
                email="test@email.com",
                password="test",
                first_name="Testfirst",
                last_name="Testlast"
            )

        student = Student()
        student.user = new_user
        student.prop = None
        student.uniform = None
        student.instrument = None
        student.school = School.objects.get(pk=1)
        student.save()

        response = self.client.get(f"/students/{student.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["prop"], None)
        self.assertEqual(json_response["uniform"], None)
        self.assertEqual(json_response["instrument"], None)
    
    def test_change_student(self):

        new_user = User.objects.create_user(
                username="test@email.com",
                email="test@email.com",
                password="test",
                first_name="Testfirst",
                last_name="Testlast"
            )

        student = Student()
        student.user = new_user
        student.prop = None
        student.uniform = None
        student.instrument = None
        student.school = School.objects.get(pk=1)
        student.save()

        data = {
            "prop": None,
            "uniform": None,
            "instrument": 1,
            "music_parts": [1, 7]
        }

        response = self.client.put(f"/students/{student.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/students/{student.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["prop"], None)
        self.assertEqual(json_response["uniform"], None)
        self.assertEqual(json_response["instrument"]["id"], 1)
        self.assertEqual(json_response["music_parts"][0]["id"], 1)
        self.assertEqual(json_response["music_parts"][1]["id"], 7)

    def test_delete_student(self):

        new_user = User.objects.create_user(
                username="test@email.com",
                email="test@email.com",
                password="test",
                first_name="Testfirst",
                last_name="Testlast"
            )

        student = Student()
        student.user = new_user
        student.prop = None
        student.uniform = None
        student.instrument = None
        student.school = School.objects.get(pk=1)
        student.save()

        response = self.client.delete(f"/students/{student.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/students/{student.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)