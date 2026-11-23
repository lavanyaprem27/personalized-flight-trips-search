from tkGUI import FlightGUI
from search import search_flights, format_input, TripInfo
import pandas as pd
from openpyxl.styles import Alignment, Font
import threading

#instance of GUI class
gui = FlightGUI()

#stores tripInfo objects from recent search
found_trips = []

def run():
    #configure the submit button to run search procedure
    gui.search_page.submit_button.config(command=get_dates)

    #configure the export button to run export procedure
    gui.search_page.export_button.config(command=results_to_excel)

    #start the main loop
    gui.mainloop()

#TODO: explain the 3 function process of processing results
def get_dates():
    #get rid of previous flight results
    found_trips.clear()
    gui.delete_result_cards()

    #create a message to indicate search
    gui.create_message_card("searching")

    #get dates from DateEntry fields
    start_date = format_input(gui.search_page.start_date.get_date())
    end_date = format_input(gui.search_page.end_date.get_date())

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
        results = search_flights(start_date, end_date)

        #queue GUI to display the results
        gui.after(0, lambda: display_results(start_date, end_date, results))

    except Exception:
        #just show a basic error message if met with an exception
        gui.delete_result_cards()
        gui.create_message_card("error")


def display_results(start_date, end_date, results):
    #queued GUI update

    #delete old cards
    gui.delete_result_cards()

    #display message if no results, hide export button
    if results == None:
        gui.create_message_card("no_results")
        gui.search_page.results_count.config(text="Results: 0")
        gui.search_page.export_button.grid_remove()
        return

    #sort results by price
    sorted_results = sorted(results, key=lambda result: result[0].price)

    #process results to display cards
    for outbound_flight, return_flight in sorted_results:
        
        #create a tripInfo object to store a single flight result, and store in found_trips[]
        trip = TripInfo(start_date, end_date, outbound_flight, return_flight)
        found_trips.append(trip)

        #create a new result card using the tripInfo object
        gui.create_result_card(trip)

    #update results count and show export button
    gui.search_page.results_count.config(text=f"Results: {len(sorted_results)}")
    gui.search_page.export_button.grid()

#TODO: explain how this works
def results_to_excel():
    #converts results in found_trips[] into an excel file

    #array that stores column names
    col_names = [
        "Total Price",
        "Outbound Airline", "Outbound Duration", "Outbound Departure Time", "Outbound Arrival Time", "Outbound Layover Airport", "Outbound Layover Duration",
        "Return Airline", "Return Duration", "Return Departure Time", "Return Arrival Time", "Return Layover Airport", "Return Layover Duration"]
    
    #array to store individual rows
    rows = []

    #iterate over tripInfo objects in found_trips[] to create rows
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

    #generate table
    table = pd.DataFrame(rows, columns=col_names)

    #create excel file
    with pd.ExcelWriter('IND_DSM_Roundtrip.xlsx', engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="results", index=False, startrow=1)

        sheet=writer.sheets["results"]

        #format cost in dollars
        for cell in sheet["A"][1:]:
            cell.number_format = '$#,##0.00'

        #add title row above table and format it as centered and bolded
        sheet.merge_cells("A1:M1")
        sheet["A1"] = f"{found_trips[0].start_date} - {found_trips[0].end_date} Roundtrip"
        sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
        sheet["A1"].font = Font(bold=True)

        #appropriately widen the columns
        for column in sheet.columns:

            #get the letter name accessor for the column
            column_name = column[1].column_letter

            #iterate through cells in column (skipping title) and find max width needed
            relative_max_width = 0
            for cell in column[1:]:
                if cell.value is not None:
                    relative_max_width = max(relative_max_width, len(str(cell.value)))

            #update column length to max +1 padding
            sheet.column_dimensions[column_name].width = relative_max_width + 2

#upon file run command
if __name__ == "__main__":
    run()