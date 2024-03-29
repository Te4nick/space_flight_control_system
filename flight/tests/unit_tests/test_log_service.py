from django.conf import settings
from django.test import TestCase

from flight.models import Passenger
from flight.services import LogService


class LogServiceTest(TestCase):
    def setUp(self) -> None:
        self.log_file_name = "test_log_service.csv"
        self.service = LogService(log_file_name=self.log_file_name)

    def test_log_service_init_success(self):
        a = Passenger("", "")
        columns = ";".join(a.__dict__.keys()) + "\n"
        with open(self.service.log_file) as csv_file:
            row_names = csv_file.readline()
            self.assertEqual(row_names, columns)

    def test_write_entry_success(self):
        passenger = Passenger("Elon", "Musk")
        columns = ";".join(passenger.__dict__.keys()) + "\n"
        self.service.write_entry(passenger.name, passenger.surname)
        with open(self.service.log_file) as csv_file:
            row_names = csv_file.readline()
            log_entry = csv_file.readline()
            self.assertEqual(row_names, columns)
            self.assertEqual(log_entry, ";".join(passenger.__dict__.values())+"\n")

    def test_get_log_file_path_success(self):
        file_path = (settings.STATIC_URL + "log/" + self.log_file_name)[1:]
        self.assertEqual(self.service.get_log_file_path(), file_path)
