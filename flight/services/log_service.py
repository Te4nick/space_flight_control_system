import os

from django.conf import settings
from ..models import Passenger


class LogService:
    def __init__(self, log_file_name: str = "passengers.csv", output_log_path: str = settings.STATIC_URL + "log/"):
        self.log_file_name = log_file_name
        self.output_log_path = output_log_path[1:] + (
            "/" if output_log_path[-1] != "/" else ""  # cut out first '/' to get relative path and set last '/'
        )
        self.log_file = self.output_log_path + self.log_file_name

        with open(self.log_file, "w") as log_file:
            a = Passenger("", "")
            log_file.write(";".join(a.__dict__.keys()) + "\n")

    def write_entry(self, name: str, surname: str) -> None:
        """
        Write a passenger to log file
        :param name: Passenger name
        :param surname: Passenger surname
        :return:
        """
        with open(self.log_file, "a") as log_file:
            log_file.write(";".join([name, surname]) + "\n")

    def get_log_file_path(self) -> str:
        """
        Get the log file path
        :return:
        """
        return self.log_file
