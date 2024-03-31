import time
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from flight.models import FlightStatus
from flight.views import FlightViewSet


class SpaceFlightControlSystemTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def post_valid_flight(
            self,
            departure_location: str = 'Earth',
            arrival_location: str = 'Mars',
            max_capacity: int = 50
    ):
        request = self.factory.post(
            '/api/v1/flight/',
            {
                'departure_location': departure_location,
                'arrival_location': arrival_location,
                'max_capacity': max_capacity,
            },
        )
        return FlightViewSet.as_view({'post': 'post_flight'})(request)

    def post_valid_passenger(self):
        request = self.factory.post(
            '/api/v1/passenger/',
            {
                'name': 'Elon',
                'surname': 'Musk',
            },
        )
        return FlightViewSet.as_view({'post': 'post_passenger'})(request)

    def test_post_flight_valid(self):
        response = self.post_valid_flight()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_flight_validation_error(self):
        request = self.factory.post(
            '/api/v1/flight/',
            {
                'i am': 'error',
            },
        )
        response = FlightViewSet.as_view({'post': 'post_flight'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_flight_status_success(self):
        self.post_valid_flight()
        request = self.factory.post(
            '/api/v1/flight/status',
            {
                'flight_id': 0,
                'status': FlightStatus.ARRIVED.value,
            },
        )
        response = FlightViewSet.as_view({'post': 'post_flight_status'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_flight_status_validation_error(self):
        self.post_valid_flight()
        request = self.factory.post(
            '/api/v1/flight/status',
            {
                'i am': 'error',
            },
        )
        response = FlightViewSet.as_view({'post': 'post_flight_status'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_flight_status_not_found(self):
        request = self.factory.post(
            '/api/v1/flight/status',
            {
                'flight_id': 1_000_000,
                'status': FlightStatus.ARRIVED.value,
            },
        )
        response = FlightViewSet.as_view({'post': 'post_flight_status'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_passenger_valid(self):
        response = self.post_valid_passenger()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_passenger_validation_error(self):
        request = self.factory.post(
            '/api/v1/passenger/',
            {
                'i am': 'error',
            },
        )
        response = FlightViewSet.as_view({'post': 'post_passenger'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_ticket_valid(self):
        flight = self.post_valid_flight()
        passenger = self.post_valid_passenger()
        request = self.factory.get(
            f'/api/v1/ticket/?flight_id={flight.data["flight_id"]}&passenger_id={passenger.data["passenger_id"]}'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_flight_not_found(self):
        flight_id = 1_000_000
        passenger = self.post_valid_passenger()
        request = self.factory.get(
            f'/api/v1/ticket/?flight_id={flight_id}&passenger_id={passenger.data["passenger_id"]}'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_ticket_passenger_not_found(self):
        flight = self.post_valid_flight()
        passenger_id = 1_000_000
        request = self.factory.get(
            f'/api/v1/ticket/?flight_id={flight.data["flight_id"]}&passenger_id={passenger_id}'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_ticket_flight_full(self):
        flight = self.post_valid_flight(max_capacity=1)
        passenger_id1 = self.post_valid_passenger().data["passenger_id"]
        passenger_id2 = self.post_valid_passenger().data["passenger_id"]
        request = self.factory.get(
            f'/api/v1/ticket/?flight_id={flight.data["flight_id"]}&passenger_id={passenger_id1}'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(
            f'/api/v1/ticket/?flight_id={flight.data["flight_id"]}&passenger_id={passenger_id2}'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ticket_validation_error(self):
        request = self.factory.get(
            f'/api/v1/ticket/'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_delayed_valid(self):
        flight_id = self.post_valid_flight().data["flight_id"]
        request = self.factory.post(
            '/api/v1/flight/status',
            {
                'flight_id': flight_id,
                'status': FlightStatus.DELAYED.value,
            },
        )
        FlightViewSet.as_view({'post': 'post_flight_status'})(request)
        request = self.factory.get(
            f'/api/v1/delayed/?flight_id={flight_id}'
        )
        response = FlightViewSet.as_view({'get': 'get_delayed'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_delayed_validation_error(self):
        request = self.factory.get(
            f'/api/v1/delayed/'
        )
        response = FlightViewSet.as_view({'get': 'get_ticket'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_delayed_not_delayed(self):
        flight_id = self.post_valid_flight().data["flight_id"]
        request = self.factory.get(
            f'/api/v1/delayed/?flight_id={flight_id}'
        )
        response = FlightViewSet.as_view({'get': 'get_delayed'})(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_delayed_flight_not_found(self):
        flight_id = 1_000_000
        request = self.factory.get(
            f'/api/v1/delayed/?flight_id={flight_id}'
        )
        response = FlightViewSet.as_view({'get': 'get_delayed'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_log_file_success(self):
        request = self.factory.get("/api/v1/log")
        response = FlightViewSet.as_view({"get": "get_log_file"})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["done"], False)
        self.assertEqual(response.data["result"], None)

    def test_get_log_file_status_success(self):
        desired_response_data = {
            "id": None,
            "done": True,
            "result": {
                "path": "static/log/passengers.csv"
            },
        }

        request = self.factory.get("/api/v1/log")
        response = FlightViewSet.as_view({"get": "get_log_file"})(request)
        desired_response_data["id"] = response.data['id']

        time.sleep(1)

        request = self.factory.get(f"/api/v1/log/status?id={response.data['id']}")
        response = FlightViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, desired_response_data)

    def test_get_log_file_status_validation_error(self):
        desired_response_data = {
            "errors": {
                "id": [
                    "This field is required."
                ]
            }
        }

        request = self.factory.get("/api/v1/log/status?cannot=validate")
        response = FlightViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, desired_response_data)

    def test_get_log_file_status_not_found(self):
        op_id = uuid4()

        request = self.factory.get(f"/api/v1/log/status?id={op_id}")
        response = FlightViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
