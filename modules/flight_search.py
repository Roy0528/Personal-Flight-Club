import requests
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2"
TEQUILA_API_KEY = os.getenv("TEQUILA")


class FlightSearch:

    def get_destination_code(self, city_name):
        code = "TESTING"
        return code
