from ..models import Passenger


class PassengerService:
    def __init__(self):
        self.passengers: list[Passenger] = []

    def add_passenger(self, name: str, surname: str) -> int:
        """
        Register new passenger in the system
        :param name: Passenger name
        :param surname: Passenger surname
        :return: Created Passenger ID
        """
        self.passengers.append(Passenger(name, surname))
        return len(self.passengers)-1

    def get_passenger(self, passenger_id: int) -> Passenger:
        """
        Get a passenger
        :param passenger_id: Passenger ID
        :return: Passenger object or None if no passenger is found
        """
        try:
            return self.passengers[passenger_id]
        except IndexError:
            return None
