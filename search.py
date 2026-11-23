from datetime import datetime, date, timedelta

from fli.models import (
    Airport,
    FlightSearchFilters,
    FlightSegment,
    PassengerInfo,
    SeatType,
    TripType,
    SortBy
)
from fli.search import SearchFlights

#TODO: explain why there are so many conversions

#converts a datetime object to fli's date input format ("year-month-day")
def format_input(date) -> str:
    return date.strftime("%Y-%m-%d")

#converts a datetime object to a "##:##AM/PM" time format
def format_time(date) -> str:
    return date.strftime("%I:%M%p")

#formats a datetime object (or a string in "year-month-day" format)
#into a "day, month date, year" format
def format_date(date) -> str:
    #converts string into parseable datetime object
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime("%A %B %d, %Y")

#formats a datetime object into a
#"day, month date, year - ##:##AM/PM" format
def format_datetime(datetime_string: datetime) -> str:
     return datetime_string.strftime("%A %B %d, %Y - %I:%M%p")

#converts minutes into a "#hr #min" format
def format_duration(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours}hr {mins}min" if hours else f"{mins}min"

#TODO: explain how the search algorithm works

def search_flights(outbound_date, return_date):

    #variables to store airports
    origin_airport = Airport.IND
    destination_airport = Airport.DSM

    #specify each trip of the roundtrip as a flight segment
    flight_segments = [
        FlightSegment(
            travel_date=outbound_date,
            departure_airport=[[origin_airport, 0]],
            arrival_airport=[[destination_airport, 0]]
        ), 
        FlightSegment(
            travel_date=return_date,
            departure_airport=[[destination_airport, 0]],
            arrival_airport=[[origin_airport, 0]]
        ),
    ]

    #Set up filter
    filters = FlightSearchFilters(
        trip_type=TripType.ROUND_TRIP,
        passenger_info=PassengerInfo(adults=1),
        seat_type=SeatType.ECONOMY,
        flight_segments=flight_segments,
        sort_by=SortBy.TOP_FLIGHTS
    )

    #perform search with fli library
    search = SearchFlights()
    results = search.search(filters)

    #return list of results
    return results

#TODO: explain purpose of helper classes

#stores general info about a singular roundtrip
#and stores objects specifying outbound and return flight
class TripInfo:
    def __init__(self, start_date, end_date, outbound_flight, return_flight):
        #store cost as formatted string
        self.cost = f"${outbound_flight.price:.2f}"

        #store trip dates as formatted strings
        self.start_date = format_date(start_date)
        self.end_date = format_date(end_date)

        #store flights as FlightInfo objects
        self.outbound_flight = FlightInfo(outbound_flight)
        self.return_flight = FlightInfo(return_flight)

#stores general info about an outbound/return flight
#as well as objects for flight legs and layovers
class FlightInfo:
    def __init__(self, flight):
        #store total duration as formatted string
        self.total_duration = format_duration(flight.duration)

        #store airline as string
        self.airline = flight.legs[0].airline.value

        #store times as formatted string
        self.departure_time = format_time(flight.legs[0].departure_datetime)
        self.arrival_time = format_time(flight.legs[-1].arrival_datetime)

        #store airports as strings in list
        self.airports = [leg.departure_airport.name for leg in flight.legs]
        self.airports.append(flight.legs[-1].arrival_airport.name)

        #store flight legs in list
        self.legs = [LegInfo(leg) for leg in flight.legs]

        #store layovers in list
        self.layovers = [LayoverInfo(layover) for layover in flight.layovers]

#stores info from a flight from one airport to another
class LegInfo:
    def __init__(self, leg):
        #store airports as dictionary of formatted strings
        self.airports = {
            "departure": leg.departure_airport.name,
            "arrival": leg.arrival_airport.name
        }

        #store times as dictionary of formatted strings
        self.times = {
            "departure": format_time(leg.departure_datetime),
            "arrival": format_time(leg.arrival_datetime)
        }

        #store duration as formatted string
        self.duration = format_duration(leg.duration)

        #store aircraft as formatted string
        self.aircraft = f"{leg.airline.value} {leg.flight_number}"

#stores info on a layover between two legs
class LayoverInfo:
    def __init__(self, layover):
        #store layover airport as string
        self.airport = layover.airport.name

        #store layover duration as formatted string
        self.duration = format_duration(layover.duration) 
          
#do not do anything if run as standalone
if __name__ == "__main__":
    pass