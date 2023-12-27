import requests
import os
from .flight_data import FlightData
from datetime import datetime, timedelta

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA")
TEQUILA_HEADERS = {
    "apikey": TEQUILA_API_KEY
}


class FlightSearch:

    def get_destination_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(f"{TEQUILA_ENDPOINT}/locations/query",
                                params=params, headers=TEQUILA_HEADERS)
        data = response.json()
        code = data["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "TWD"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",
                                params=params, headers=TEQUILA_HEADERS)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["cityFrom"],
            origin_airport=data["flyFrom"],
            destination_city=data["cityTo"],
            destination_airport=data["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: NT${flight_data.price}")
        return flight_data


if __name__ == "__main__":
    flight_search = FlightSearch()
    tomorrow = datetime.now() + timedelta(days=1)
    three_days_later = datetime.now() + timedelta(days=180)
    result = flight_search.check_flights("TPE", "KMJ", tomorrow, three_days_later)
    print(f"出發日期： {result.out_date}")
    print(f"回國日期： {result.return_date}")
