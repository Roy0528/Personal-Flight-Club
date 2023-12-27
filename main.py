from modules import DataManager, FlightSearch, EmailManager
from datetime import datetime, timedelta

data_manager = DataManager()
flight_search = FlightSearch()
email_manager = EmailManager()

sheet_data = data_manager.get_destination_data()
print(sheet_data)

ORIGIN_CITY_IATA = "TPE"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"Sheet data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for row in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=row["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    try:
        if flight.price < row["lowestPrice"]:
            email_manager.send_email(
                receiver_email="roy32011@gmail.com", # hsuanjung.wu@gmail.com
                subject=f"Lowest Price of {flight.origin_city} to {flight.destination_city}",
                message=f"""
                <html>
                    <body>
                    <h1>Low Price Alert!</h1>
                        <p>
                            Only NT${flight.price} to fly from 
                            <b>{flight.origin_city}-{flight.origin_airport}</b> to 
                            <b>{flight.destination_city}-{flight.destination_airport}</b>,
                            from <em>{flight.out_date} to {flight.return_date}</em>.
                        </p>
                        <br>
                        <a href="{flight.link}">Booking Link</a>
                    </body>
                </html>
                """
            )
    except AttributeError:
        print("No Email Send!")
