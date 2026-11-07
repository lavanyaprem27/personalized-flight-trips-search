import tkinter as tk
from tkcalendar import DateEntry

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
    print(f"travel date: {departing_date} | return date: {return_date}")
    print("***********************************************************\n")
    if results == None:
        print("Sorry, no flights found!")
        return

    print(f"{len(results)} trips found")
    for departing_flight, return_flight in results:
        print("\n___________________________________________________________")

        print(f"Departing Flight: {departing_flight.duration} min\n")

        for i in range(len(departing_flight.legs)):
            segment = departing_flight.legs[i]
            print(f"Flight: {segment.airline.value} {segment.flight_number} ({segment.duration} min)")
            print(f"Departure: {segment.departure_datetime} {segment.departure_airport.name}")
            print(f"Arrival: {segment.arrival_datetime} {segment.arrival_airport.name}\n")

            if i < len(departing_flight.legs) - 1:
                layover = departing_flight.layovers[i]
                print(f"Layover: {layover.duration}min in {layover.airport.name}\n")
        
        print("-----------------------------------------------------------")
        
        print(f"Returning Flight: {return_flight.duration}min\n")

        for i in range(len(return_flight.legs)):
                    segment = return_flight.legs[i]
                    print(f"Flight: {segment.airline.value} {segment.flight_number} ({segment.duration} min)")
                    print(f"Departure: {segment.departure_datetime} {segment.departure_airport.name}")
                    print(f"Arrival: {segment.arrival_datetime} {segment.arrival_airport.name}\n")
        
                    if i < len(return_flight.legs) - 1:
                        layover = return_flight.layovers[i]
                        print(f"Layover: {layover.duration}min in {layover.airport.name}\n")
        
        print("-----------------------------------------------------------")

        print(f"Total Price: ${departing_flight.price:.2f} ")



if __name__ == "__main__":
    run()
