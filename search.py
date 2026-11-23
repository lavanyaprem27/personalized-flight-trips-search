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

#All the functions below convert datetime objects into a
#more human readable format. Both the fli library search results
#and the DateTime entries used in the GUI to input travel dates return
#information in the form of datetime objects, so I use these to easily
#convert the returned info into text to display on the GUI

def format_input(date) -> str:
    return date.strftime("%Y-%m-%d")

def format_time(date) -> str:
    return date.strftime("%I:%M%p")

def format_date(date) -> str:
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime("%A %B %d, %Y")

def format_datetime(datetime_string: datetime) -> str:
     return datetime_string.strftime("%A %B %d, %Y - %I:%M%p")

def format_duration(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours}hr {mins}min" if hours else f"{mins}min"

#This search function uses the fli library to return roundtrip options
#between the Indianapolis Airport and Des Moines Airport.
#The structure of this function follows the procedure advised by punitarani, the
#creator of the fli library. It starts by specifying the requested flight segments, 
#aka outbound and return flights, to search for. Then we create a filter to narrow 
#down the search to the top round trips of the specified flight segments
#for a single economy seat. The fli library performs the search using
#searchFlights().search(filters) and returns the results as tuples of the
#class FlightResult, two for each search result representing the outbound and return flight.
def search_flights(outbound_date, return_date):

    origin_airport = Airport.IND
    destination_airport = Airport.DSM

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

    filters = FlightSearchFilters(
        trip_type=TripType.ROUND_TRIP,
        passenger_info=PassengerInfo(adults=1),
        seat_type=SeatType.ECONOMY,
        flight_segments=flight_segments,
        sort_by=SortBy.TOP_FLIGHTS
    )

    search = SearchFlights()
    results = search.search(filters)

    return results

#The following classes are used for storing relevant information
#provided by fli's FlightResult instances in formatted text that
#can be easily accessed by tkGUI.py to make the result cards. 
#I noticed that FlightResult itself stored specific information
#on layovers and individual flights between airports as separate objects,
#so I mirrored that with my usage of LayoverInfo and LegInfo. One thing
#I did differently was to make TripInfo hold the outbound and return flights
#rather than a tuple, so that I could also store general information
#like the total cost and start/end dates searched for.
#The outbound and inbound FlightResult objects are passed into TripInfo,
#which handles making the nested FlightInfo, LegInfo, and LayoverInfo objects
#by passing FlightResult's own representations of this info into their 
#constructors. In the end, my classes have a similar heirachy to FlightResult.

class TripInfo:
    def __init__(self, start_date, end_date, outbound_flight, return_flight):
        #store cost as formatted string
        self.cost = f"${outbound_flight.price:.2f}"

        self.start_date = format_date(start_date)
        self.end_date = format_date(end_date)

        self.outbound_flight = FlightInfo(outbound_flight)
        self.return_flight = FlightInfo(return_flight)

class FlightInfo:
    def __init__(self, flight):
        self.total_duration = format_duration(flight.duration)

        self.airline = flight.legs[0].airline.value

        self.departure_time = format_time(flight.legs[0].departure_datetime)
        self.arrival_time = format_time(flight.legs[-1].arrival_datetime)

        self.airports = [leg.departure_airport.name for leg in flight.legs]
        self.airports.append(flight.legs[-1].arrival_airport.name)

        self.legs = [LegInfo(leg) for leg in flight.legs]

        self.layovers = [LayoverInfo(layover) for layover in flight.layovers]

class LegInfo:
    def __init__(self, leg):
        self.airports = {
            "departure": leg.departure_airport.name,
            "arrival": leg.arrival_airport.name
        }

        self.times = {
            "departure": format_time(leg.departure_datetime),
            "arrival": format_time(leg.arrival_datetime)
        }

        self.duration = format_duration(leg.duration)

        self.aircraft = f"{leg.airline.value} {leg.flight_number}"

class LayoverInfo:
    def __init__(self, layover):
        self.airport = layover.airport.name

        self.duration = format_duration(layover.duration) 
          
if __name__ == "__main__":
    pass