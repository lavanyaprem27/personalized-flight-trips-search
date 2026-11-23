from tkGUI import FlightGUI
from search import search_flights, format_input, TripInfo
import pandas as pd
from openpyxl.styles import Alignment, Font
import threading

gui = FlightGUI()

found_trips = []

#Typically, the commands of Tkinter buttons are initialized
#as soon as the button is made. In this case, I chose to configure
#the submit and export buttons on the search_page in main.py
#because the commands use functions that depend on features
#within other classes (submit button needs search algorithm
#from search.py, export button uses the TripInfo objects stored
#in main.py)
def run():
    gui.search_page.submit_button.config(command=get_dates)
    gui.search_page.export_button.config(command=results_to_excel)

    gui.mainloop()

#This is the command used by the submit button to perform the
#Google Flights search. This function originally handled everything
#from clearing the results, using the fli library to search, and
#updating the GUI. I realized that this caused a very similar issue
#to something we learned in CS180 when working on Swing GUIs:
#the GUI would freeze while the main thread worked on other methods.
#Now, get_dates() only handles clearing the results and starting a 
#search thread.
def get_dates():
    found_trips.clear()
    gui.delete_result_cards()

    gui.create_message_card("searching")

    start_date = format_input(gui.search_page.start_date.get_date())
    end_date = format_input(gui.search_page.end_date.get_date())

    threading.Thread(
        target=perform_search,
        args=(start_date, end_date),
        daemon=True
    ).start()

#This function is what runs within the separate thread. It relies
#on search.py to use the fli library and gather results from Google Flights.
#I've noticed that sometimes the fli library fails to connect,
#so I've included a broad try/except to display an error message when this happens.
def perform_search(start_date, end_date):
    try:
        results = search_flights(start_date, end_date)
        gui.after(0, lambda: display_results(start_date, end_date, results))

    except Exception:
        gui.delete_result_cards()
        gui.create_message_card("error")

#This function is the queued GUI update that happens after the thread finishes.
#The results are not naturally sorted by price, so I use a lambda to sort
#the results (tuples of the fli class FlightResult) from lowest to highest price.
#I then use the FlightResult instances to create my own TripInfo instances,
#which store the most relevant info in text format. This is more convenient
#for making the result cards, as I don't have to format the information multiple times.
def display_results(start_date, end_date, results):
    gui.delete_result_cards()

    if results == None:
        gui.create_message_card("no_results")
        gui.search_page.results_count.config(text="Results: 0")
        gui.search_page.export_button.grid_remove()
        return

    sorted_results = sorted(results, key=lambda result: result[0].price)

    for outbound_flight, return_flight in sorted_results:
        trip = TripInfo(start_date, end_date, outbound_flight, return_flight)
        found_trips.append(trip)

        gui.create_result_card(trip)

    gui.search_page.results_count.config(text=f"Results: {len(sorted_results)}")
    gui.search_page.export_button.grid()

#This function is used by the export button and creates an excel sheet
#in the working directory with basic information from each found trip.
#The export functionality is only available when there is at least 1 result.
#The function uses pandas and openpyxl to build the table row-by-row from
#each TripInfo object stored. Afterwards, all the price entrys in row A1
#are formatted into numbers, and each column's width is set to its widest entry.
def results_to_excel():
    col_names = [
        "Total Price",
        "Outbound Airline", "Outbound Duration", "Outbound Departure Time", "Outbound Arrival Time", "Outbound Layover Airport", "Outbound Layover Duration",
        "Return Airline", "Return Duration", "Return Departure Time", "Return Arrival Time", "Return Layover Airport", "Return Layover Duration"]
    
    rows = []

    for trip in found_trips:
        new_row = []

        #total price (formatted as float)
        new_row.append(float(trip.cost[1:]))

        #outbound info

        #airline
        new_row.append(trip.outbound_flight.airline)
        #duration
        new_row.append(trip.outbound_flight.total_duration)
        #departure time
        new_row.append(trip.outbound_flight.departure_time)
        #arrival time
        new_row.append(trip.outbound_flight.arrival_time)
        #layover airport
        new_row.append(trip.outbound_flight.layovers[0].airport)
        #layover duration
        new_row.append(trip.outbound_flight.layovers[0].duration)

        #return info

        #airline
        new_row.append(trip.return_flight.airline)
        #duration
        new_row.append(trip.return_flight.total_duration)
        #departure time
        new_row.append(trip.return_flight.departure_time)
        #arrival time
        new_row.append(trip.return_flight.arrival_time)
        #layover airport
        new_row.append(trip.return_flight.layovers[0].airport)
        #layover duration
        new_row.append(trip.return_flight.layovers[0].duration)

        #append final row
        rows.append(new_row)

    table = pd.DataFrame(rows, columns=col_names)

    with pd.ExcelWriter('IND_DSM_Roundtrip.xlsx', engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="results", index=False, startrow=1)

        sheet=writer.sheets["results"]

        for cell in sheet["A"][1:]:
            cell.number_format = '$#,##0.00'

        #Here, I am merging the first row into a single cell to display a title.
        #The title simply shows the start and end date of the trips.
        sheet.merge_cells("A1:M1")
        sheet["A1"] = f"{found_trips[0].start_date} - {found_trips[0].end_date} Roundtrip"
        sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
        sheet["A1"].font = Font(bold=True)

        #This loop iterates through each column in the spreadsheet.
        #It first starts by finding out the column's letter name,
        #which is needed to apply the new width. Then, it iterates through
        #every filled cell (except the first one, which is a merged cell) and keeps
        #track of the widest cell. In the end, the max width is applied
        #to the column with an extra 2 pixels for padding.
        for column in sheet.columns:
            column_name = column[1].column_letter

            relative_max_width = 0
            for cell in column[1:]:
                if cell.value is not None:
                    relative_max_width = max(relative_max_width, len(str(cell.value)))

            sheet.column_dimensions[column_name].width = relative_max_width + 2

if __name__ == "__main__":
    run()