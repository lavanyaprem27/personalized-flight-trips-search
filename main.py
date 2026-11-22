from tkGUI import flightGUI
from search import searchFlights, format_input, tripInfo
import threading

gui = flightGUI()
flights = []

def run():
        #configure the submit button to run search procedure
        gui.homePage.submit_button.config(command=get_dates)

        #start the main loop
        gui.mainloop()

def get_dates():
    #get rid of previous flight results
    flights.clear()
    gui.deleteResultCards()

    #create a message to indicate search
    gui.create_message_card("searching")
    print("starting!")

    #get dates from DateEntry fields
    start_date = format_input(gui.homePage.start_date.get_date())
    end_date = format_input(gui.homePage.end_date.get_date())

    #create a thread to search
    threading.Thread(
        target=perform_search,
        args=(start_date, end_date),
        daemon=True
    ).start()

def perform_search(start_date, end_date):
    #what happens in the search thread
    #use a try/except to display a basic error message for exceptions
    try:
        #perform search
        results = searchFlights(start_date, end_date)

        #queue GUI to display the results
        gui.after(0, lambda: display_results(start_date, end_date, results))

    except Exception:
        #just show a basic error message if met with an exception
        gui.deleteResultCards()
        gui.create_message_card("error")


def display_results(start_date, end_date, results):
    #queued GUI update

    #delete old cards
    gui.deleteResultCards()

    #display message if no results
    if results == None:
        gui.create_message_card("no_results")
        return

    #sort results by price
    sorted_results = sorted(results, key=lambda result: result[0].price)

    #process results to display cards
    for departing_flight, return_flight in sorted_results:
        #create a tripInfo object to store a single flight result, and store in flights[]
        trip = tripInfo(start_date, end_date, departing_flight, return_flight)
        flights.append(trip)

        #create a new result card using the tripInfo object
        gui.create_result_card(trip)


if __name__ == "__main__":
    run()