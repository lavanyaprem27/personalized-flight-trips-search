from tkGUI import flightGUI
from search import searchFlights, format_input, tripInfo
import threading

gui = flightGUI()

def run():
        gui.homePage.submit_button.config(command=get_dates)
        gui.mainloop()

def get_dates():
    gui.deleteResultCards()
    gui.create_message_card("searching")
    print("starting!")
    
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
        results = searchFlights(start_date, end_date)
        sorted_results = sorted(results, key=lambda result: result[0].price)
        gui.after(0, lambda: display_results(sorted_results))
    except Exception:
        gui.deleteResultCards()
        gui.create_message_card("error")


def display_results(results):
    #queued GUI update
    gui.deleteResultCards()
    if results == None:
        gui.create_message_card("no_results")
        return

    for departing_flight, return_flight in results:
        trip = tripInfo(departing_flight, return_flight)
        gui.create_result_card(trip)


if __name__ == "__main__":
    run()