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

def searchFlights(departing_date, return_date):

    #variables to store airports
    origin_airport = Airport.IND
    destination_airport = Airport.DSM

    #flight segments
    flight_segments = [
        FlightSegment(
            travel_date=departing_date,
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

    #perform search
    search = SearchFlights()
    results = search.search(filters)

    consoleDemo(results)

    #return list of results
    return results

def consoleDemo(results):
    #exit if no results found
    if results == None:
        print("Sorry, no flights found!")
        return

    print(f"{len(results)} trips found")

    for departing_flight, return_flight in results:
        print("\n___________________________________________________________")

        print(f"Departing Flight: {format_duration(departing_flight.duration)}\n")

        for i in range(len(departing_flight.legs)):
            segment = departing_flight.legs[i]
            print(f"Flight: {segment.airline.value} {segment.flight_number} ({format_duration(segment.duration)})")
            print(f"Departure: {format_datetime(segment.departure_datetime)} from {segment.departure_airport.name}")
            print(f"Arrival: {format_datetime(segment.arrival_datetime)} from {segment.arrival_airport.name}\n")

            if i < len(departing_flight.legs) - 1:
                layover = departing_flight.layovers[i]
                print(f"Layover: {format_duration(layover.duration)} in {layover.airport.name}\n")
        
        print("-----------------------------------------------------------")
        
        print(f"Returning Flight: {format_duration(return_flight.duration)}\n")

        for i in range(len(return_flight.legs)):
                    segment = return_flight.legs[i]
                    print(f"Flight: {segment.airline.value} {segment.flight_number} ({format_duration(segment.duration)})")
                    print(f"Departure: {format_datetime(segment.departure_datetime)} from {segment.departure_airport.name}")
                    print(f"Arrival: {format_datetime(segment.arrival_datetime)} from {segment.arrival_airport.name}\n")
        
                    if i < len(return_flight.legs) - 1:
                        layover = return_flight.layovers[i]
                        print(f"Layover: {format_duration(layover.duration)} in {layover.airport.name}\n")
        
        print("-----------------------------------------------------------")

        print(f"Total Price: ${departing_flight.price:.2f} ")

#helper classes for parsing info
class tripInfo:
    def __init__(self, departing_flight, return_flight):
        #store cost
        self.cost = departing_flight.price
        self.departing_flight = flightInfo(departing_flight)
        self.return_flight = flightInfo(return_flight)


class flightInfo:
    def __init__(self, flight):
        #store duration as formatted string
        self.duration = format_duration(flight.duration)

        #store airline as string
        self.airline = flight.legs[0].airline.value

        #store times as formatted string
        self.departing_time = format_time(flight.legs[0].departure_datetime)
        self.arrival_time = format_time(flight.legs[-1].arrival_datetime)

        #store airports as strings in list
        self.airports = []
        for leg in flight.legs:
               self.airports.append(leg.departure_airport.name)
        self.airports.append(flight.legs[-1].arrival_airport.name)

          

if __name__ == "__main__":
     consoleDemo(searchFlights("2026-12-20", "2027-01-08"))