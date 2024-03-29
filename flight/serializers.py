from rest_framework import serializers
from rest_enumfield import EnumField

from .models import FlightStatus


class InFlightSerializer(serializers.Serializer):
    departure_location = serializers.CharField(max_length=50)
    arrival_location = serializers.CharField(max_length=50)
    max_capacity = serializers.IntegerField(min_value=1, default=50)


class FlightIDSerializer(serializers.Serializer):
    flight_id = serializers.IntegerField(min_value=0, required=True)


class InPassengerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)


class PassengerIDSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField(min_value=0, required=True)


class BuyTicketQuerySerializer(FlightIDSerializer, PassengerIDSerializer):
    pass


class ChangeFlightStatusSerializer(FlightIDSerializer):
    status = EnumField(choices=FlightStatus, required=True)


class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )


class OperationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, min_length=36, max_length=36)
    done = serializers.BooleanField()
    result = serializers.DictField()


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)