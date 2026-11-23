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

def searchFlights(outbound_date, return_date):

    #variables to store airports
    origin_airport = Airport.IND
    destination_airport = Airport.DSM

    #flight segments
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

    for outbound_flight, return_flight in results:
        print("\n___________________________________________________________")

        print(f"Departing Flight: {format_duration(outbound_flight.duration)}\n")

        for i in range(len(outbound_flight.legs)):
            segment = outbound_flight.legs[i]
            print(f"Flight: {segment.airline.value} {segment.flight_number} ({format_duration(segment.duration)})")
            print(f"Departure: {format_datetime(segment.departure_datetime)} from {segment.departure_airport.name}")
            print(f"Arrival: {format_datetime(segment.arrival_datetime)} from {segment.arrival_airport.name}\n")

            if i < len(outbound_flight.legs) - 1:
                layover = outbound_flight.layovers[i]
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

        print(f"Total Price: ${outbound_flight.price:.2f} ")

#helper classes for parsing info
class tripInfo:
    def __init__(self, start_date, end_date, outbound_flight, return_flight):
        #store cost as formatted string
        self.cost = f"${outbound_flight.price:.2f}"

        #store trip dates as formatted strings
        self.start_date = format_date(start_date)
        self.end_date = format_date(end_date)

        #store flights as flightInfo objects
        self.outbound_flight = flightInfo(outbound_flight)
        self.return_flight = flightInfo(return_flight)


class flightInfo:
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
        self.legs = [legInfo(leg) for leg in flight.legs]

        #store layovers in list
        self.layovers = [layoverInfo(layover) for layover in flight.layovers]

class legInfo:
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

class layoverInfo:
    def __init__(self, layover):
        #store layover airport as string
        self.airport = layover.airport.name

        #store layover duration as formatted string
        self.duration = format_duration(layover.duration) 
          

if __name__ == "__main__":
     consoleDemo(searchFlights("2026-12-20", "2027-01-08"))