from uuid import UUID

from django.shortcuts import render
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .services import FlightService, LogService, OperationService, PassengerService
from .serializers import (
    InFlightSerializer,
    FlightIDSerializer,
    InPassengerSerializer,
    PassengerIDSerializer,
    BuyTicketQuerySerializer,
    ChangeFlightStatusSerializer,
    ValidationErrorSerializer,
    OperationSerializer,
    GetOperationQuerySerializer,
)



@extend_schema_view(
    post_flight=extend_schema(
        summary="Post new flight information",
        request=InFlightSerializer,
        responses={
            status.HTTP_201_CREATED: FlightIDSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
    post_flight_status=extend_schema(
        summary="Post new flight status",
        request=ChangeFlightStatusSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
    post_passenger=extend_schema(
        summary="Post new passenger information",
        request=InPassengerSerializer,
        responses={
            status.HTTP_201_CREATED: PassengerIDSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
    get_ticket=extend_schema(
        summary="Buy ticket to flight by user",
        parameters=[BuyTicketQuerySerializer],
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_403_FORBIDDEN: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
    get_delayed=extend_schema(
        summary="Check if flight is delayed",
        parameters=[FlightIDSerializer],
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
    get_log_file=extend_schema(
        summary="Generate passengers.csv and get operation details",
        responses={
            status.HTTP_200_OK: OperationSerializer,
        },
        auth=False,
    ),
    get_log_file_status=extend_schema(
        summary="Get passengers.csv generation status",
        parameters=[GetOperationQuerySerializer],
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    ),
)
class FlightViewSet(ViewSet):
    flight_service = FlightService()
    log_service = LogService()
    ops_service = OperationService()
    passenger_service = PassengerService()

    @action(detail=False, methods=["POST"])
    def post_flight(self, request):
        in_flight = InFlightSerializer(data=request.data)
        if not in_flight.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": in_flight.errors}).data,
            )

        new_flight_id = self.flight_service.add_flight(**in_flight.data)
        return Response(
            status=status.HTTP_201_CREATED,
            data=FlightIDSerializer({"flight_id": new_flight_id}).data
        )

    @action(detail=False, methods=["POST"])
    def post_flight_status(self, request):
        new_flight_status = ChangeFlightStatusSerializer(data=request.data)
        if not new_flight_status.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": new_flight_status.errors}).data,
            )
        print(new_flight_status.data)
        if self.flight_service.change_flight_status(**new_flight_status.data):
            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            status=status.HTTP_404_NOT_FOUND,
        )

    @action(detail=False, methods=["POST"])
    def post_passenger(self, request):
        in_passenger = InPassengerSerializer(data=request.data)
        if not in_passenger.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": in_passenger.errors}).data,
            )

        new_passenger_id = self.passenger_service.add_passenger(**in_passenger.data)
        self.log_service.write_entry(**in_passenger.data)
        return Response(
            status=status.HTTP_201_CREATED,
            data=PassengerIDSerializer({"passenger_id": new_passenger_id}).data
        )

    @action(detail=False, methods=["GET"])
    def get_ticket(self, request):
        query_ser = BuyTicketQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
            )

        if self.passenger_service.get_passenger(query_ser.data["passenger_id"]) is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            self.flight_service.buy_ticket(**query_ser.data)
            return Response(
                status=status.HTTP_200_OK,
            )
        except IndexError:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )

    @action(detail=False, methods=["GET"])
    def get_delayed(self, request):
        query_ser = FlightIDSerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
            )
        try:
            if self.flight_service.is_delayed(query_ser.data["flight_id"]):
                return Response(
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
        except IndexError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["GET"])
    def get_log_file(self, _):
        op_id = self.ops_service.execute_operation(self.log_service.get_log_file_path)
        op = self.ops_service.get_operation(op_id)
        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(op).data,
        )

    @action(detail=False, methods=["GET"])
    def get_log_file_status(self, request):
        query_ser = GetOperationQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
            )

        op = self.ops_service.get_operation(UUID(query_ser.data.get("id")))
        if op is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(
                {
                    "id": op.id,
                    "done": op.done,
                    "result": {
                        "path": op.result,
                    },
                }
            ).data,
        )

