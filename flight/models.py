from django.db import models
from enum import Enum
from uuid import UUID


class Passenger:
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname


class FlightStatus(Enum):  # NOTE: EnumField in serializers are dumb so hard-code values = str choices for now
    AVAILABLE_FOR_REGISTRATION = "AVAILABLE_FOR_REGISTRATION"
    REGISTRATION_COMPLETED = "REGISTRATION_COMPLETED"
    ON_THE_WAY = "ON_THE_WAY"
    ARRIVED = "ARRIVED"
    DELAYED = "DELAYED"


class Flight:
    def __init__(
            self,
            departure_location: str,
            arrival_location: str,
            max_capacity: int,
            status: str = FlightStatus.AVAILABLE_FOR_REGISTRATION.value
    ) -> None:
        if max_capacity <= 0:
            raise ValueError('Passenger capacity must be greater than 0')
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.max_capacity = max_capacity
        self.status: str = status
        self.passengers: list[int] = []


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.id == other.id
            and self.done == other.done
            and self.result == other.result
        )
