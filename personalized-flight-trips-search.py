import tkinter as tk
from tkcalendar import DateEntry

from fli.models import (
    Airport,
    DateSearchFilters,
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
        sort_by=SortBy.CHEAPEST
    )

    #perform search
    search = SearchFlights()
    results = search.search(filters)

    #print results
    for departing_flight, return_flight in results:
        print("\n___________________________________________________________")
        print("Departing Flight:\n")
        for segment in departing_flight.legs:
            print(f"Flight: {segment.airline.value} {segment.flight_number}")
            print(f"Departure: {segment.departure_datetime}")
            print(f"Arrival: {segment.arrival_datetime}\n")
        print("-----------------------------------------------------------")
        print("Returning Flight:\n")
        for segment in return_flight.legs:
            print(f"Flight: {segment.airline.value} {segment.flight_number}")
            print(f"Departure: {segment.departure_datetime}")
            print(f"Arrival: {segment.arrival_datetime}\n")
        print("-----------------------------------------------------------")
        print(f"Total Price: ${departing_flight.price:.2f} ")



if __name__ == "__main__":
    run()
