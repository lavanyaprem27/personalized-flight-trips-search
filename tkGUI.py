import tkinter as tk
from tkinter import ttk, font
from tkcalendar import DateEntry
from datetime import date
from fli.search import SearchFlights

class flightGUI(tk.Tk):

    result_cards = []

    def __init__(self):
        super().__init__()

        #colors
        self.COLORS = {
            "black": "#000000",
            "old_gold": "#CFB991",
            "campus_gold": "#C28E0E",
            "gray": "#474448",
            "white": "#FFFFFF",
            "red": "#D36161",
            "green": "#19B45F",
            "blue": "#587AF6"
        } 
    
        #fonts
        self.FONTS = {
            "title": font.Font(family="Helvetica", size=20, weight="bold"),
            "subtitle": font.Font(family="Helvetica", size=15),
            "header": font.Font(family="Helvetica", size=10, weight="bold"),
            "label": font.Font(family="Helvetica", size=8, weight="bold"),
            "regular": font.Font(family="Helvetica", size=8)
        }

        #root setup
        self.title("Personalized Flight Trips Search!")
        self.geometry("300x450+50+50")
        ttk.Style().theme_use("clam")

        #main gui container frame setup
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.homePage = searchPage(self.container, self)
        self.homePage.grid(row=0, column=0, sticky="nsew")

        self.detailsPage = detailsPage(self.container, self)
        self.detailsPage.grid(row=0, column=0, sticky="nsew")

        self.detailsPage.tkraise()

        

    def create_result_card(self, tripInfo, index):
        #add a result card to search page panel
        self.result_cards.append(self.homePage.create_result_card(tripInfo, index))

    def deleteResultCards(self):
        for card in self.result_cards:
            card.destroy()

        self.result_cards.clear()

    def create_message_card(self, type):
        #create specialized message cards based on inputted "type"
        match type:
            case "no_results":
                self.result_cards.append(self.homePage.create_empty_card())
                return
            case "searching":
                self.result_cards.append(self.homePage.create_search_card())
                return
            case "error":
                self.result_cards.append(self.homePage.create_error_card())
                return
            case _:
                self.result_cards.append(self.homePage.create_error_card())
                return


class searchPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_search_panel()
        self.create_results_panel()


    def create_search_panel(self):
        #create panel for date search, and make it maintain aspect ratio
        ttk.Style().configure("search.TFrame", background=self.controller.COLORS["black"])
        self.search_panel = ttk.Frame(self, style="search.TFrame", padding=10)
        self.search_panel.pack(fill="x")
        self.bind("<Configure>", self.resize_search_panel)

        #create panel for title
        self.title_panel = ttk.Frame(self.search_panel, style="search.TFrame", padding=10)
        self.title_panel.pack(side="top")

        #create title and subtitle
        ttk.Style().configure("title.TLabel", font=self.controller.FONTS["title"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["campus_gold"])
        ttk.Style().configure("subtitle.TLabel", font=self.controller.FONTS["subtitle"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["old_gold"])
        self.title = ttk.Label(self.title_panel, text="GET ME OUT OF HERE!", style="title.TLabel")
        self.title.grid(row=0, column=0)
        self.subtitle = ttk.Label(self.title_panel, text="Search roundtrips between IND and DSM", style="subtitle.TLabel")
        self.subtitle.grid(row=1, column=0)

        #create panel to house input
        self.input_panel = ttk.Frame(self.search_panel, style="search.TFrame")
        self.input_panel.pack()

        #create start and end date labels
        ttk.Style().configure("search_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["white"])

        start_date_label = ttk.Label(self.input_panel, text="Departing Date:", style="search_label.TLabel")
        start_date_label.grid(row=0, column = 0, padx=5, pady=5)

        end_date_label = ttk.Label(self.input_panel, text="Returning Date:", style="search_label.TLabel")
        end_date_label.grid(row=0, column = 1, padx=5, pady=5)
        
        #create start date and end date selectors
        ttk.Style().configure("field.DateEntry")

        calendar_theme = {
            "style": "field.DateEntry",
            "firstweekday": "sunday",
            "showweeknumbers": False,
            "background": self.controller.COLORS["gray"],
            "normalbackground": self.controller.COLORS["white"],
            "normalforeground": self.controller.COLORS["black"],
            "othermonthbackground": self.controller.COLORS["white"],
            "othermonthforeground": self.controller.COLORS["black"],
            "weekendbackground": self.controller.COLORS["old_gold"],
            "weekendforeground": self.controller.COLORS["black"],
            "othermonthwebackground": self.controller.COLORS["old_gold"],
            "othermonthweforeground": self.controller.COLORS["black"],
            "selectbackground": self.controller.COLORS["campus_gold"],
            "othermonth": self.controller.COLORS["gray"],
            "font": self.controller.FONTS["regular"]
        }

        self.start_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy", mindate=date.today(), **calendar_theme)
        self.start_date.grid(row=1, column = 0, padx=5, pady=5)

        self.end_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy", mindate=date.today(), **calendar_theme)
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
        ttk.Style().configure("submit.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("submit.TButton",
            background=[("active", self.controller.COLORS["old_gold"]), ("pressed", self.controller.COLORS["old_gold"])])
        self.submit_button = ttk.Button(self.input_panel, text="SEARCH", style="submit.TButton")
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

    def create_results_panel(self):
        #create panel to display cards of search results
        ttk.Style().configure("results_border.TFrame", background=self.controller.COLORS["gray"])
        self.results_panel = ttk.Frame(self, style="results_border.TFrame")
        self.results_panel.pack(fill="both", expand=True)

        #create a frame to house scrollbar
        self.results_frame = ttk.Frame(self.results_panel, style="results_border.TFrame")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.results_frame.grid_rowconfigure(0, weight=1)


        #create a scrollbar by making a scroll bar, a canvas, and a holder 
        ttk.Style().configure("results_container.TFrame", background=self.controller.COLORS["white"])
        
        self.results_canvas = tk.Canvas(self.results_frame, bg=self.controller.COLORS["white"], highlightthickness=0)
        self.results_canvas.grid(row=0, column=0, sticky="nsew")

        self.results_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_scroll.grid(row=0, column=1, sticky="ns")

        self.results_canvas.configure(yscrollcommand=self.results_scroll.set)

        self.results_container = ttk.Frame(self.results_canvas, style="results_container.TFrame", padding=10)
        self.results_window = self.results_canvas.create_window((0,0), window=self.results_container, anchor="nw")

        self.results_container.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.itemconfig(self.results_window, width=e.width))

    def create_result_card(self, tripInfo, index):
        #store departing and return flight info conveniently
        departing_flight = tripInfo.departing_flight
        return_flight = tripInfo.return_flight

        #makes a card to display a possible flight 
        ttk.Style().configure("result_card.TFrame")
        new_card = ttk.Frame(self.results_container, style="result_card.TFrame")
        new_card.pack(fill="x", pady=5)
        new_card.columnconfigure(0, weight=3, uniform="columns")
        new_card.columnconfigure(1, weight=3, uniform="columns")
        new_card.columnconfigure(2, weight=2, uniform="columns")

        #creates a small side panel for total cost display
        ttk.Style().configure("cost.TFrame", background=self.controller.COLORS["campus_gold"])
        cost_panel = ttk.Frame(new_card, style="cost.TFrame")
        cost_panel.grid(row=0, column=2, sticky="nsew")

        ttk.Style().configure("cost.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        cost = ttk.Label(cost_panel, text=f"${tripInfo.cost}", style="cost.TLabel")
        cost.pack(expand=True, padx=10, pady=10)

        #creates colors and fonts for departing and return panels
        ttk.Style().configure("info.TFrame", background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_text.TLabel", font=self.controller.FONTS["regular"],
            background=self.controller.COLORS["old_gold"])


        #panel for departing flight info
        departing_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        departing_panel.grid(row=0, column=0, sticky="nsew")

        depart_airline = ttk.Label(departing_panel, text=f"Departing Flight: {departing_flight.airline}", style="result_label.TLabel")
        depart_airline.pack(anchor="w")

        depart_string = ""
        for i in range(len(departing_flight.airports)):
            if (i != 0):
                depart_string += "→"
            depart_string += f"{departing_flight.airports[i]}"
        
        depart_order = ttk.Label(departing_panel, text=depart_string, style="result_text.TLabel")
        depart_order.pack(anchor="w")

        depart_time = ttk.Label(departing_panel, 
            text=f"{departing_flight.departing_time} to {departing_flight.arrival_time} ({departing_flight.total_duration})",
            style="result_text.TLabel")
        depart_time.pack(anchor="w")

        #panel for return flight info
        return_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        return_panel.grid(row=0, column=1, sticky="nsew")

        return_airline = ttk.Label(return_panel, text=f"Returning Flight: {return_flight.airline}", style="result_label.TLabel")
        return_airline.pack(anchor="w")

        return_string = ""
        for i in range(len(return_flight.airports)):
            if (i != 0):
                return_string += "→"
            return_string += f"{return_flight.airports[i]}"
        
        return_order = ttk.Label(return_panel, text=return_string, style="result_text.TLabel")
        return_order.pack(anchor="w")

        return_time = ttk.Label(return_panel, 
            text=f"{return_flight.departing_time} to {return_flight.arrival_time} ({return_flight.total_duration})",
            style="result_text.TLabel")
        return_time.pack(anchor="w")

        return new_card

    def create_empty_card(self):
        #makes a card to display a possible flight 
        ttk.Style().configure("empty.TFrame", background=self.controller.COLORS["blue"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["blue"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="No results found!", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

    def create_search_card(self):
        #makes a card to display a possible flight 
        ttk.Style().configure("empty.TFrame", background=self.controller.COLORS["green"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["green"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="Searching...", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

    def create_error_card(self):
        #makes a card to indicate an exception or error with search
        ttk.Style().configure("error.TFrame", background=self.controller.COLORS["red"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["red"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="error.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="Sorry, we encountered an error. Please try again later!", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

class detailsPage(ttk.Frame):

    #array to hold all the info frames
    sections = []
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_template()
        self.fill_template()

    def create_template(self):
        #create a panel to serve as heading
        ttk.Style().configure("details_topbar.TFrame", background=self.controller.COLORS["black"])
        self.details_topbar = ttk.Frame(self, style="details_topbar.TFrame")
        self.details_topbar.pack(side="top", fill="x")

        self.details_topbar.columnconfigure(0, weight=5, uniform="columns")
        self.details_topbar.columnconfigure(1, weight=1, uniform="columns")

        #create a container for the heading
        ttk.Style().configure("details_heading_panel.TFrame", background=self.controller.COLORS["black"])
        self.details_heading_panel = ttk.Frame(self.details_topbar, style="details_heading_panel.TFrame", padding=20)
        self.details_heading_panel.grid(row=0, column=0, sticky="nsew")

        #add text to heading, use dummy values for now
        ttk.Style().configure("details_dates.TLabel", justify="left", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["white"])
        self.details_heading = ttk.Label(self.details_heading_panel, text="Monday November 23, 2026 - Monday November 23, 2026", style="details_dates.TLabel")
        self.details_heading.pack(side="left", fill="both", expand=True)

        self.details_heading_panel.bind("<Configure>", lambda e: self.details_heading.config(wraplength=(e.width - 50)))

        #add a corner for the cost
        ttk.Style().configure("details_cost_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        self.details_cost_panel = ttk.Frame(self.details_topbar, style="details_cost_panel.TFrame", padding=10)
        self.details_cost_panel.grid(row=0, column=1, sticky="nsew")

        #add cost text
        ttk.Style().configure("details_cost.TLabel", justify="center", font=self.controller.FONTS["subtitle"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        self.details_cost = ttk.Label(self.details_cost_panel, text="$650", style="details_cost.TLabel")
        self.details_cost.place(relx=0.5,rely=0.5, anchor="center")

        #create panel to display cards of flight info
        ttk.Style().configure("details_border.TFrame", background=self.controller.COLORS["gray"])
        self.details_panel = ttk.Frame(self, style="details_border.TFrame")
        self.details_panel.pack(side="top", fill="both", expand=True)

        #create a frame to house scrollbar
        self.details_frame = ttk.Frame(self.details_panel, style="details_border.TFrame")
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=0)
        self.details_frame.grid_rowconfigure(0, weight=1)

        #create a scrollbar by making a scroll bar, a canvas, and a holder 
        ttk.Style().configure("details_container.TFrame", background=self.controller.COLORS["white"])
        
        self.details_canvas = tk.Canvas(self.details_frame, bg=self.controller.COLORS["white"], highlightthickness=0)
        self.details_canvas.grid(row=0, column=0, sticky="nsew")

        self.details_scroll = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_canvas.yview)
        self.details_scroll.grid(row=0, column=1, sticky="ns")

        self.details_canvas.configure(yscrollcommand=self.details_scroll.set)

        self.details_container = ttk.Frame(self.details_canvas, style="results_container.TFrame", padding=10)
        self.details_window = self.details_canvas.create_window((0,0), window=self.details_container, anchor="nw")

        self.details_container.bind("<Configure>", lambda e: self.details_canvas.configure(scrollregion=self.details_canvas.bbox("all")))
        self.details_canvas.bind("<Configure>", lambda e: self.details_canvas.itemconfig(self.details_window, width=e.width))

        #create a button at the bottom to return back to home screen
        self.back_panel = ttk.Frame(self, style="details_border.TFrame", padding=10)
        self.back_panel.pack(side="bottom", fill="x")

        ttk.Style().configure("back.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("back.TButton",
            background=[("active", self.controller.COLORS["old_gold"]), ("pressed", self.controller.COLORS["old_gold"])])
        self.submit_button = ttk.Button(self.back_panel, text="BACK", style="back.TButton")
        self.submit_button.pack(fill="both", expand=True)

    def fill_template(self):
        #clear sections
        for section in self.sections:
            section.destroy()

        self.sections.clear()


        #add sections for departing and return flight
        self.add_flight_info()
        self.add_flight_info()

    def add_flight_info(self):
        #create a panel to hold flight info
        flight_details_panel = ttk.Frame(self.details_container)
        flight_details_panel.pack(fill="x", pady=5)

        #make a topbar to list type of flight (departing vs. arrival) and total flight time
        ttk.Style().configure("flight_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        flight_topbar = ttk.Frame(flight_details_panel, style="flight_panel.TFrame", padding=10)
        flight_topbar.pack(side="top", fill="x")

        #add text to the topbar
        ttk.Style().configure("flight_heading.TLabel", justify="left", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        flight_heading = ttk.Label(flight_topbar, text="Departing Flight (1hr 20m)", style="flight_heading.TLabel")
        flight_heading.pack(side="left")

        #create a container to hold the specific flight info
        ttk.Style().configure("flight_container.TFrame", background=self.controller.COLORS["old_gold"])
        flight_details_container = ttk.Frame(flight_details_panel, style="flight_container.TFrame", padding=10)
        flight_details_container.pack(side="top", fill="both", expand=True)

        #generate cards for flight info
        ttk.Style().configure("flight_details_card.TFrame", background=self.controller.COLORS["white"])
        ttk.Style().configure("flight_details_label.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["white"])
        ttk.Style().configure("flight_details_text.TLabel", font=self.controller.FONTS["regular"],
            background=self.controller.COLORS["white"])
        
        for i in range(2):
            #make a card with flight leg details
            flight_leg_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
            flight_leg_card.pack(side="top", fill="x", pady=5)

            #add the text to the flight leg details card
            flight_leg_title = ttk.Label(flight_leg_card, text="Flight: 1hr 40min", style="flight_details_label.TLabel")
            flight_leg_title.pack(side="top", fill="x")
            flight_leg_airplane = ttk.Label(flight_leg_card, text="Aircraft: United Airlines 2770", style="flight_details_text.TLabel")
            flight_leg_airplane.pack(side="top", fill="x")
            flight_leg_departure = ttk.Label(flight_leg_card, text="Departure: Monday November 23, 2026 - 06:45PM from DSM", style="flight_details_text.TLabel")
            flight_leg_departure.pack(side="top", fill="x")
            flight_leg_arrival = ttk.Label(flight_leg_card, text="Return: Monday November 23, 2026 - 08:25PM from ORD", style="flight_details_text.TLabel")
            flight_leg_arrival.pack(side="top", fill="x")

            if i < 2 - 1:
                #create a layover card in between each flight leg
                flight_layover_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
                flight_layover_card.pack(side="top", fill="x", pady=5)

                flight_layover_title = ttk.Label(flight_layover_card, text="Layover: 1hr 10min", style="flight_details_label.TLabel")
                flight_layover_title.pack(side="top", fill="x")
                flight_layover_airport = ttk.Label(flight_layover_card, text="Airport: ORD", style="flight_details_text.TLabel")
                flight_layover_airport.pack(side="top", fill="x")
            
        #finally, add flight info card to sections list
        self.sections.append(flight_details_panel)


if __name__ == "__main__":
    gui = flightGUI()
    gui.mainloop()
