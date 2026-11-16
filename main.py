from tkGUI import flightGUI
from search import searchFlights, format_input, tripInfo

gui = flightGUI()

def run():
        gui.homePage.submit_button.config(command=perform_search)
        gui.createEmptyCard()
        gui.mainloop()

def perform_search():
    print("starting!")
    start_date = format_input(gui.homePage.start_date.get_date())
    end_date = format_input(gui.homePage.start_date.get_date())

    # start_date = "2026-12-20"
    # end_date = "2027-01-08"
    results = searchFlights(start_date, end_date)

    gui.deleteResultCards()

    if results == None:
        gui.createEmptyCard()
        return

    for departing_flight, return_flight in results:
        trip = tripInfo(departing_flight, return_flight)
        gui.create_result_card(trip)

if __name__ == "__main__":
    run()