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


if __name__ == "__main__":
    run()
