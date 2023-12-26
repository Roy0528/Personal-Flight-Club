import requests
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA")


class FlightSearch:

    def get_destination_code(self, city_name):
        headers = {
            "apikey": TEQUILA_API_KEY
        }
        params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(f"{TEQUILA_ENDPOINT}/locations/query", params=params, headers=headers)
        data = response.json()
        code = data["locations"][0]["code"]
        return code


if __name__ == "__main__":
    flight_search = FlightSearch()
    result = flight_search.get_destination_code("Paris")
    print(result)
