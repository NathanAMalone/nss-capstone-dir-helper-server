import json
from rest_framework import status
from rest_framework.test import APITestCase
from helperapi.models import Director, Instrument, School
from rest_framework.authtoken.models import Token

class InstrumentTests(APITestCase):

    fixtures = ['users', 'tokens', 'directors', 'schools', 'instruments']

    def setUp(self):
        self.director = Director.objects.first()
        token = Token.objects.get(user=self.director.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_create_instrument(self):

        url = "/instruments"

        data = {
            "name": "oboe",
            "type": "woodwind",
            "serial_number": 3542452458,
            "out_for_repair": False,
            "school_owned": False,
            "assigned": True
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "oboe")
        self.assertEqual(json_response["type"], "woodwind")
        self.assertEqual(json_response["serial_number"], 3542452458)
        self.assertEqual(json_response["out_for_repair"], False)
        self.assertEqual(json_response["school_owned"], False)
        self.assertEqual(json_response["assigned"], True)

    def test_get_instrument(self):

        instrument = Instrument()
        instrument.name = "oboe"
        instrument.type = "woodwind"
        instrument.serial_number = 546542462
        instrument.out_for_repair = False
        instrument.school_owned = False
        instrument.assigned = True
        instrument.school = School.objects.get(pk=1)
        instrument.save()

        response = self.client.get(f"/instruments/{instrument.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "oboe")
        self.assertEqual(json_response["type"], "woodwind")
        self.assertEqual(json_response["serial_number"], 546542462)
        self.assertEqual(json_response["out_for_repair"], False)
        self.assertEqual(json_response["school_owned"], False)
        self.assertEqual(json_response["assigned"], True)

    def test_change_instrument(self):

        instrument = Instrument()
        instrument.name = "oboe"
        instrument.type = "woodwind"
        instrument.serial_number = 546542462
        instrument.out_for_repair = False
        instrument.school_owned = False
        instrument.assigned = True
        instrument.school = School.objects.get(pk=1)
        instrument.save()

        data = {
            "name": "bassoon",
            "type": "woodwind",
            "serial_number": 21345,
            "out_for_repair": True,
            "school_owned": True,
        }

        response = self.client.put(f"/instruments/{instrument.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/instruments/{instrument.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "bassoon")
        self.assertEqual(json_response["type"], "woodwind")
        self.assertEqual(json_response["serial_number"], 21345)
        self.assertEqual(json_response["out_for_repair"], True)
        self.assertEqual(json_response["school_owned"], True)

    def test_delete_instrument(self):

        instrument = Instrument()
        instrument.name = "oboe"
        instrument.type = "woodwind"
        instrument.serial_number = 546542462
        instrument.out_for_repair = False
        instrument.school_owned = False
        instrument.assigned = True
        instrument.school = School.objects.get(pk=1)
        instrument.save()

        response = self.client.delete(f"/instruments/{instrument.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/instruments/{instrument.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)