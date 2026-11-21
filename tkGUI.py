import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from fli.search import SearchFlights

class flightGUI(tk.Tk):

    result_cards = []

    def __init__(self):
        super().__init__()

        #root setup
        self.title("Get me out of here!")
        self.geometry("300x450+50+50")

        #main gui container frame setup
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.homePage = searchPage(self.container, self)
        self.homePage.pack(fill="both", expand=True)

    def create_styles(self):
        #colors
        #fonts
        pass

    def create_result_card(self, tripInfo):
        #add a result card to search page panel
        self.result_cards.append(self.homePage.create_result_card(tripInfo))

    def deleteResultCards(self):
        for card in self.result_cards:
            card.destroy()

        self.result_cards.clear()

    def createEmptyCard(self):
        self.result_cards.append(self.homePage.create_empty_card())

    def createTempCard(self):
        self.result_cards.append(self.homePage.create_temporary_card())


class searchPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_search_panel()
        self.create_results_panel()


    def create_search_panel(self):
        #create panel for date search, and make it maintain aspect ratio
        ttk.Style().configure("search.TFrame", background="#7280bf")
        self.search_panel = ttk.Frame(self, style="search.TFrame", padding=10)
        self.search_panel.pack(fill="x")
        self.bind("<Configure>", self.resize_search_panel)

        #create panel for title
        self.title_panel = ttk.Frame(self.search_panel, style="search.TFrame", padding=10)
        self.title_panel.pack(side="top")

        #create title and subtitle
        self.title = ttk.Label(self.title_panel, text="GET ME OUT OF HERE!")
        self.title.grid(row=0, column=0)
        self.subtitle = ttk.Label(self.title_panel, text="Search roundtrips between IND and DSM")
        self.subtitle.grid(row=1, column=0)

        #create panel to house input
        self.input_panel = ttk.Frame(self.search_panel, style="search.TFrame")
        self.input_panel.pack()

        #create start and end date labels
        start_date_label = ttk.Label(self.input_panel, text="Departing Date:")
        start_date_label.grid(row=0, column = 0, padx=5, pady=5)

        end_date_label = ttk.Label(self.input_panel, text="Returning Date:")
        end_date_label.grid(row=0, column = 1, padx=5, pady=5)
        
        #create start date
        self.start_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy")
        self.start_date.grid(row=1, column = 0, padx=5, pady=5)

        #create end date
        self.end_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy")
        self.end_date.grid(row=1, column = 1, padx=5, pady=5)

        #add validators to ensure start < end
        self.end_date.bind("<<DateEntrySelected>>", self.regulate_dates)
        self.start_date.bind("<<DateEntrySelected>>", self.regulate_dates)

        self.end_date.bind("<FocusOut>", self.regulate_dates)
        self.start_date.bind("<FocusOut>", self.regulate_dates)

        #add a function to shift focus to anything that was clicked
        #prevents dateTime entries from staying open forever
        self.bind_all("<Button-1>",  lambda e: e.widget.focus_set())

        #create submit button
        self.submit_button = ttk.Button(self.input_panel, text="Search")
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def resize_search_panel(self, event):
        #set aspect ratio
        aspect_ratio = 3 / 2
        max_height_proportion = 0.4

        #calculate height, but cap if is too long
        new_height = int(event.width / aspect_ratio)
        max_height = int(self.winfo_height() * max_height_proportion)

        #cap new height if exceeds max proportion
        new_height = min(new_height, max_height)

        self.search_panel.config(height=new_height)

    def regulate_dates(self, event):
        #if the start date ends up being after the end date,
        #update the non-active dateEntry to be the same day as the active one
        if (self.start_date.get_date() > self.end_date.get_date()):
            if event.widget == self.start_date:
                #change end date to be equal to start date
                self.end_date.set_date(self.start_date.get_date())
            else:
                #change start date to be equal to end date
                self.start_date.set_date(self.end_date.get_date())

        # #set min and max dates for each appropriately to prevent overstepping
        # self.start_date.config(maxdate=self.end_date.get_date())
        # self.end_date.config(mindate=self.start_date.get_date())



    def create_results_panel(self):
        #create panel to display cards of search results
        ttk.Style().configure("results.TFrame", background="#545c80")
        self.results_panel = ttk.Frame(self, style="results.TFrame")
        self.results_panel.pack(fill="both", expand=True)

        #create a frame to house scrollbar
        self.results_frame = ttk.Frame(self.results_panel, style="results.TFrame")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.results_frame.grid_rowconfigure(0, weight=1)


        #create a scrollbar by making a scroll bar, a canvas, and a holder 
        ttk.Style().configure("results_container.TFrame", background="#ffffff")
        
        self.results_canvas = tk.Canvas(self.results_frame, bg="#ffffff", highlightthickness=0)
        self.results_canvas.grid(row=0, column=0, sticky="nsew")

        self.results_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_scroll.grid(row=0, column=1, sticky="ns")

        self.results_canvas.configure(yscrollcommand=self.results_scroll.set)

        self.results_container = ttk.Frame(self.results_canvas, style="results_container.TFrame", padding=10)
        self.results_window = self.results_canvas.create_window((0,0), window=self.results_container, anchor="nw")

        self.results_container.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.itemconfig(self.results_window, width=e.width))

    def create_result_card(self, tripInfo):
        #store departing and return flight info conveniently
        departing_flight = tripInfo.departing_flight
        return_flight = tripInfo.return_flight

        #makes a card to display a possible flight 
        ttk.Style().configure("result_card.TFrame", background="#000000")
        new_card = ttk.Frame(self.results_container, style="result_card.TFrame")
        new_card.pack(fill="x", pady=5)
        new_card.columnconfigure(0, weight=3, uniform="columns")
        new_card.columnconfigure(1, weight=3, uniform="columns")
        new_card.columnconfigure(2, weight=2, uniform="columns")

        #creates a small side panel for total cost display
        ttk.Style().configure("cost.TFrame", background="#10882E")
        cost_panel = ttk.Frame(new_card, style="cost.TFrame")
        cost_panel.grid(row=0, column=2, sticky="nsew")

        cost = ttk.Label(cost_panel, text=f"${tripInfo.cost}")
        cost.pack(expand=True, padx=10, pady=10)

        #creates colors for departing and return panels
        ttk.Style().configure("info.TFrame", background="#6EAD7E")

        #panel for departing flight info
        departing_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        departing_panel.grid(row=0, column=0, sticky="nsew")

        depart_airline = ttk.Label(departing_panel, text=f"Departing Flight: {departing_flight.airline}")
        depart_airline.pack(anchor="w")

        depart_string = ""
        for i in range(len(departing_flight.airports)):
            if (i != 0):
                depart_string += "→"
            depart_string += f"{departing_flight.airports[i]}"
        
        depart_order = ttk.Label(departing_panel, text=depart_string)
        depart_order.pack(anchor="w")

        depart_time = ttk.Label(departing_panel, 
            text=f"{departing_flight.departing_time} to {departing_flight.arrival_time} ({departing_flight.duration})")
        depart_time.pack(anchor="w")

        #panel for return flight info
        return_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        return_panel.grid(row=0, column=1, sticky="nsew")

        return_airline = ttk.Label(return_panel, text=f"Returning Flight: {return_flight.airline}")
        return_airline.pack(anchor="w")

        return_string = ""
        for i in range(len(return_flight.airports)):
            if (i != 0):
                return_string += "→"
            return_string += f"{return_flight.airports[i]}"
        
        return_order = ttk.Label(return_panel, text=return_string)
        return_order.pack(anchor="w")

        return_time = ttk.Label(return_panel, 
            text=f"{return_flight.departing_time} to {return_flight.arrival_time} ({return_flight.duration})")
        return_time.pack(anchor="w")

        return new_card

    def create_empty_card(self):
        #makes a card to display a possible flight 
        ttk.Style().configure("empty.TFrame", background="#C62121")
        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="No results found!")
        label.pack(expand="true")

        return new_card

    def create_temporary_card(self):
        #makes a card to display a possible flight 
        ttk.Style().configure("empty.TFrame", background="#217EC6")
        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="Searching...")
        label.pack(expand="true")

        return new_card

if __name__ == "__main__":
    gui = flightGUI()
    gui.mainloop()
