from django.test import TestCase

from flight.models import Flight, FlightStatus
from flight.services import FlightService


class FlightServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = FlightService()

    def test_add_flight(self):
        flight = Flight('Earth', 'Mars', 20)
        added_flight_id = self.service.add_flight(
            flight.departure_location,
            flight.arrival_location,
            flight.max_capacity
        )

        self.assertEqual(self.service.flights[added_flight_id].departure_location, flight.departure_location)
        self.assertEqual(self.service.flights[added_flight_id].arrival_location, flight.arrival_location)
        self.assertEqual(self.service.flights[added_flight_id].max_capacity, flight.max_capacity)

    def test_change_flight_status(self):
        flight = Flight('Earth', 'Mars', 20)
        self.service.flights = [flight]
        added_flight_id = 0
        status = FlightStatus.DELAYED.value

        self.assertEqual(self.service.change_flight_status(added_flight_id, status), True)
        self.assertEqual(self.service.flights[added_flight_id].status, status)

    def test_change_flight_status_not_found(self):
        self.assertEqual(self.service.change_flight_status(0, ''), False)

    def test_buy_ticket(self):
        flight = Flight('Earth', 'Mars', 20)
        self.service.flights = [flight]
        added_flight_id = 0
        passenger_id = 0

        self.service.buy_ticket(added_flight_id, passenger_id)

        self.assertEqual(self.service.flights[added_flight_id].passengers[0], passenger_id)

    def test_buy_ticket_flight_full(self):
        flight = Flight('Earth', 'Mars', 1)
        passenger_id = 0
        flight.passengers = [passenger_id]
        self.service.flights = [flight]
        added_flight_id = 0

        self.assertRaises(ValueError, self.service.buy_ticket, added_flight_id, passenger_id)

    def test_is_delayed_true(self):
        flight = Flight('Earth', 'Mars', 20)
        flight.status = FlightStatus.DELAYED.value
        self.service.flights = [flight]
        added_flight_id = 0

        self.assertEqual(self.service.is_delayed(added_flight_id), True)

    def test_is_delayed_false(self):
        flight = Flight('Earth', 'Mars', 20)
        self.service.flights = [flight]
        added_flight_id = 0

        self.assertEqual(self.service.is_delayed(added_flight_id), False)
