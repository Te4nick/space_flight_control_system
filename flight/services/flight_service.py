from ..models import Flight, FlightStatus
from datetime import datetime


class FlightService:
    def __init__(self):
        self.flights: list[Flight] = []

    def add_flight(
            self,
            departure_location: str,
            arrival_location: str,
            max_capacity: int
    ) -> int:
        """
        Add a new flight to the system
        :param departure_location:
        :param arrival_location:
        :param max_capacity:
        :return: ID of the new flight
        """
        self.flights.append(
            Flight(
                departure_location,
                arrival_location,
                max_capacity,
            )
        )
        return len(self.flights)-1

    def change_flight_status(self, flight_id: int, status: str) -> bool:
        """
        Change flight status
        :param flight_id: Flight ID
        :param status: new flight status (FlightStatus.value)
        :return: True if successful, False otherwise
        """
        try:
            self.flights[flight_id].status = status
            return True
        except IndexError:
            return False

    def buy_ticket(self, flight_id: int, passenger_id: int) -> None:
        """
        Try to buy a ticket. Raises IndexError if flight_id is out of range. Raises ValueError if flight is full.
        :param flight_id: Flight ID
        :param passenger_id: Passenger ID to add to the flight passenger list (NOTE: no checks are performed)
        :return:
        """
        if len(self.flights[flight_id].passengers) >= self.flights[flight_id].max_capacity:
            raise ValueError(f"Flight {flight_id} is already full")

        self.flights[flight_id].passengers.append(passenger_id)

    def is_delayed(self, flight_id: int) -> bool:
        """
        Check if flight is delayed. Raises IndexError if flight is not found.
        :param flight_id: Flight ID
        :return: flight is delayed
        """
        return self.flights[flight_id].status == FlightStatus.DELAYED.value

