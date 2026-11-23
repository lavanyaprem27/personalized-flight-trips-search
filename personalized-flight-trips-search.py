import tkinter as tk
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

#variables to store dates
departing_date = "2026-12-20"
return_date = "2027-01-08"

#variables to store airports
origin_airport = Airport.IND
destination_airport = Airport.DSM

def format_date(date) -> str:
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime("%A %B %d, %Y")

def format_datetime(datetime_string: datetime) -> str:
     return datetime_string.strftime("%A %B %d, %Y - %I:%M%p")

def format_duration(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours}hr {mins}min" if hours else f"{mins}min"


def run():

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

    #print results
    print(f"{origin_airport.value} <--> {destination_airport.value}")
    print(f"travel date: {format_date(departing_date)} | return date: {format_date(return_date)}")
    print("***********************************************************\n")

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



if __name__ == "__main__":
    run()
