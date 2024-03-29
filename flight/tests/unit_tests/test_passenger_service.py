from django.test import TestCase

from flight.models import Passenger
from flight.services import PassengerService


class PassengerServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = PassengerService()

    def test_add_passenger(self):
        passenger = Passenger(name='Water', surname='Rock')
        added_passenger_id = self.service.add_passenger(passenger.name, passenger.surname)
        self.assertEqual(self.service.passengers[added_passenger_id].name, passenger.name)
        self.assertEqual(self.service.passengers[added_passenger_id].surname, passenger.surname)

    def test_get_student_success(self):
        passenger = Passenger(name='Water', surname='Rock')
        self.service.passengers.append(passenger)
        self.assertEqual(passenger, self.service.get_passenger(0))


