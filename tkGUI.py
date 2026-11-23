import tkinter as tk
from tkinter import ttk, font
from tkcalendar import DateEntry
from datetime import date
from fli.search import SearchFlights

#TODO: explain why GUI was made in separate class

class FlightGUI(tk.Tk):

    #stores all the result card frames for current search
    result_cards = []

    #sets up GUI
    def __init__(self):
        #initialize tkinter
        super().__init__()

        #stores global colors
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
    
        #stores global fonts
        self.FONTS = {
            "title": font.Font(family="Helvetica", size=15, weight="bold"),
            "subtitle": font.Font(family="Helvetica", size=12),
            "header": font.Font(family="Helvetica", size=10, weight="bold"),
            "label": font.Font(family="Helvetica", size=8, weight="bold"),
            "regular": font.Font(family="Helvetica", size=8)
        }

        #root setup, size and theme specification
        self.title("Personalized Flight Trips Search!")
        self.geometry("350x450+50+50")
        self.minsize(300,450)
        ttk.Style().theme_use("clam")

        #main gui container frame setup
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        #initialize search_page
        self.search_page = SearchPage(self.container, self)
        self.search_page.grid(row=0, column=0, sticky="nsew")

        #initialize a blank details_page
        self.details_page = DetailsPage(self.container, self)
        self.details_page.grid(row=0, column=0, sticky="nsew")

        #display the search_page at program start
        self.search_page.tkraise()   

    #creates a new card for a roundtrip result and stores it in result_cards[]
    def create_result_card(self, TripInfo):
        #add a result card to search page panel
        self.result_cards.append(self.search_page.create_result_card(TripInfo))

    #deletes all the result cards for a search and resets the results_panel
    def delete_result_cards(self):
        #delete each of the frames
        for card in self.result_cards:
            card.destroy()

        #clear list
        self.result_cards.clear()

        #reset scrollbar
        self.search_page.results_canvas.yview_moveto(0)

    #create specialized message cards based on inputted "type"
    def create_message_card(self, type):
        match type:
            #displayed when 0 results are found
            case "no_results":
                self.result_cards.append(self.search_page.create_empty_card())
                return
            #displays temporarily while fli search algorithm runs
            case "searching":
                self.result_cards.append(self.search_page.create_search_card())
                return
            #displays when the fli search algorithm throws an exception
            case "error":
                self.result_cards.append(self.search_page.create_error_card())
                return
            #default, displays error card
            case _:
                self.result_cards.append(self.search_page.create_error_card())
                return

    #function attached to a results card, opens the corresponding results page
    def open_details(self, TripInfo):
        self.details_page.fill_template(TripInfo)
        self.details_page.tkraise()

#TODO: explain why we made a separate class for the search page
class SearchPage(ttk.Frame):

    #builds the widgets on the search_page
    def __init__(self, parent, controller):
        #initialize object
        super().__init__(parent)
        self.controller = controller

        #build page sections
        self.create_search_panel()
        self.create_results_panel()

    #TODO: explain what this does in detail
    def create_search_panel(self):
        #create panel for date search, and make it maintain aspect ratio
        ttk.Style().configure("search.TFrame", background=self.controller.COLORS["black"])
        self.search_panel = ttk.Frame(self, style="search.TFrame", padding=10)
        self.search_panel.pack(fill="x")
        self.bind("<Configure>", self.resize_search_panel)

        #create panel for title
        self.title_panel = ttk.Frame(self.search_panel, style="search.TFrame", padding=10)
        self.title_panel.pack(side="top")

        #create title
        ttk.Style().configure("title.TLabel", font=self.controller.FONTS["title"], 
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["campus_gold"])
        ttk.Style().configure("subtitle.TLabel", font=self.controller.FONTS["subtitle"], 
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["old_gold"])
        self.title = ttk.Label(self.title_panel, text="GET ME OUT OF HERE!",
            style="title.TLabel", justify="center")
        self.title.grid(row=0, column=0)

        #create subtitle
        self.subtitle = ttk.Label(self.title_panel, text="Search roundtrips between IND and DSM",
            style="subtitle.TLabel", justify="center")
        self.subtitle.grid(row=1, column=0)

        #allow wraparound for title and subtitle during resizing
        self.search_panel.bind("<Configure>", lambda e: (
            self.title.config(wraplength=e.width-40),
            self.subtitle.config(wraplength=e.width-40)
        ))

        #create panel to house input
        self.input_panel = ttk.Frame(self.search_panel, style="search.TFrame")
        self.input_panel.pack()

        #create start and end date labels
        ttk.Style().configure("search_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["white"])

        start_date_label = ttk.Label(self.input_panel, text="Outbound Date:", style="search_label.TLabel")
        start_date_label.grid(row=0, column = 0, padx=5, pady=5)

        end_date_label = ttk.Label(self.input_panel, text="Return Date:", style="search_label.TLabel")
        end_date_label.grid(row=0, column = 1, padx=5, pady=5)
        
        #create start date and end date selectors
        ttk.Style().configure("field.DateEntry")

        #calendar dropdown must be styled separately
        #the arguments are stored in a dictionary
        #so that they are shared between the two DateEntry selectors
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
            "font": self.controller.FONTS["regular"],
            "cursor": "xterm",
            "calendar_cursor": "hand2"
        }

        self.start_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy", mindate=date.today(), **calendar_theme)
        self.start_date.grid(row=1, column = 0, padx=5, pady=5)

        self.end_date = DateEntry(self.input_panel, date_pattern="mm/dd/yyyy", mindate=date.today(), **calendar_theme)
        self.end_date.grid(row=1, column = 1, padx=5, pady=5)

        #add validators to ensure start_date is before end_date
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
        self.submit_button = ttk.Button(self.input_panel, text="SEARCH", style="submit.TButton", cursor="hand2")
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    #TODO: explain why this exists
    def resize_search_panel(self, event):
        #set aspect ratio and max height relative to window height
        aspect_ratio = 3 / 2
        max_height_proportion = 0.4

        #calculate height and max height relative to window
        new_height = int(event.width / aspect_ratio)
        max_height = int(self.winfo_height() * max_height_proportion)

        #cap new height if exceeds max height
        new_height = min(new_height, max_height)

        #update height
        self.search_panel.config(height=new_height)

    #TODO: explain this
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
        #create a panel at the bottom to show total results and export button
        ttk.Style().configure("results_border.TFrame", background=self.controller.COLORS["gray"])
        self.export_panel = ttk.Frame(self, style="results_border.TFrame", padding=10)
        self.export_panel.pack(side="bottom", fill="x")
        self.export_panel.columnconfigure(0, weight=3, uniform="columns")
        self.export_panel.columnconfigure(1, weight=2, uniform="columns")

        #create text to show total results, and allow text wrapping
        ttk.Style().configure("results_num.TLabel", justify="left", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["gray"],
            foreground=self.controller.COLORS["white"])
        self.results_count = ttk.Label(self.export_panel, text="Results: 0", style="results_num.TLabel")
        self.results_count.grid(row=0, column=0, sticky="nsew")
        self.export_panel.bind("<Configure>", lambda e: self.results_count.config(wraplength=(e.width/2)))

        #create the button to export to Excel, hide on start
        ttk.Style().configure("export.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("export.TButton",
            background=[("active", self.controller.COLORS["old_gold"]),("pressed", self.controller.COLORS["old_gold"])])
        self.export_button = ttk.Button(self.export_panel, text="EXPORT TO EXCEL", style="back.TButton", cursor="hand2")
        self.export_button.grid(row=0, column=1, sticky="nsew")
        self.export_button.grid_remove()
        
        #create panel to display cards of search results
        self.results_panel = ttk.Frame(self, style="results_border.TFrame")
        self.results_panel.pack(fill="both", expand=True)

        #create a frame to house scrollbar
        self.results_frame = ttk.Frame(self.results_panel, style="results_border.TFrame")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.results_frame.grid_rowconfigure(0, weight=1)

        #create a scrollbar by making a scroll bar and a canvas
        ttk.Style().configure("results_container.TFrame", background=self.controller.COLORS["white"])
        
        self.results_canvas = tk.Canvas(self.results_frame, bg=self.controller.COLORS["white"], highlightthickness=0)
        self.results_canvas.grid(row=0, column=0, sticky="nsew")

        self.results_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_scroll.grid(row=0, column=1, sticky="ns")

        #configure the canvas to scroll when the scrollbar is moved
        self.results_canvas.configure(yscrollcommand=self.results_scroll.set)

        #create a frame container for the widgets,
        #and configure the canvas to fit the frame fully
        self.results_container = ttk.Frame(self.results_canvas, style="results_container.TFrame", padding=10)
        self.results_window = self.results_canvas.create_window((0,0), window=self.results_container, anchor="nw")

        self.results_container.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.itemconfig(self.results_window, width=e.width))

    #TODO: explain why we are making results separately
    def create_result_card(self, TripInfo):
        #store outbound and return flight info conveniently
        outbound_flight = TripInfo.outbound_flight
        return_flight = TripInfo.return_flight

        #makes a card to display a possible flight 
        ttk.Style().configure("result_card.TFrame")
        new_card = ttk.Frame(self.results_container, style="result_card.TFrame")
        new_card.pack(fill="x", pady=5)
        new_card.columnconfigure(0, weight=3, uniform="columns")
        new_card.columnconfigure(1, weight=3, uniform="columns")
        new_card.columnconfigure(2, weight=2, uniform="columns")

        #creates a small side panel for total cost display
        ttk.Style().configure("cost.TFrame", background=self.controller.COLORS["campus_gold"], padding=5)
        cost_panel = ttk.Frame(new_card, style="cost.TFrame")
        cost_panel.grid(row=0, column=2, sticky="nsew")

        #create text to display cost
        ttk.Style().configure("cost.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        cost = ttk.Label(cost_panel, text=f"{TripInfo.cost}", style="cost.TLabel")
        cost.pack(expand=True)

        #creates frame bg colors and fonts for outbound and return panels
        ttk.Style().configure("info.TFrame", background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_text.TLabel", font=self.controller.FONTS["regular"],
            background=self.controller.COLORS["old_gold"])

        #panel for outbound flight info
        outbound_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        outbound_panel.grid(row=0, column=0, sticky="nsew")

        #display airline
        outbound_airline = ttk.Label(outbound_panel, text=f"Outbound Flight: {outbound_flight.airline}", style="result_label.TLabel")
        outbound_airline.pack(anchor="w")

        #build a string showing all the airports on the trip
        #connected by arrows
        outbound_string = ""
        for i in range(len(outbound_flight.airports)):
            if (i != 0):
                outbound_string += "→"
            outbound_string += f"{outbound_flight.airports[i]}"
        
        outbound_order = ttk.Label(outbound_panel, text=outbound_string, style="result_text.TLabel")
        outbound_order.pack(anchor="w")

        #display departure&arrival times, duration
        outbound_time = ttk.Label(outbound_panel, 
            text=f"{outbound_flight.departure_time} to {outbound_flight.arrival_time} ({outbound_flight.total_duration})",
            style="result_text.TLabel")
        outbound_time.pack(anchor="w")

        #allow resizing of text within outbound_panel
        outbound_panel.bind("<Configure>", lambda e: (
            outbound_airline.config(wraplength=e.width-15),
            outbound_order.config(wraplength=e.width-15),
            outbound_time.config(wraplength=e.width-15),
        ))

        #panel for return flight info
        return_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        return_panel.grid(row=0, column=1, sticky="nsew")

        #display airline
        return_airline = ttk.Label(return_panel, text=f"Return Flight: {return_flight.airline}", style="result_label.TLabel")
        return_airline.pack(anchor="w")

        #build a string showing all the airports on the trip
        #connected by arrows
        return_string = ""
        for i in range(len(return_flight.airports)):
            if (i != 0):
                return_string += "→"
            return_string += f"{return_flight.airports[i]}"
        
        return_order = ttk.Label(return_panel, text=return_string, style="result_text.TLabel")
        return_order.pack(anchor="w")

        #display departure&arrival times, duration
        return_time = ttk.Label(return_panel, 
            text=f"{return_flight.departure_time} to {return_flight.arrival_time} ({return_flight.total_duration})",
            style="result_text.TLabel")
        return_time.pack(anchor="w")

        #allow resizing of text within return_panel
        return_panel.bind("<Configure>", lambda e: (
            return_airline.config(wraplength=e.width-15),
            return_order.config(wraplength=e.width-15),
            return_time.config(wraplength=e.width-15),
        ))

        #configure card to redirect to details page upon click
        self.make_card_clickable(new_card, lambda e: self.controller.open_details(TripInfo))

        return new_card

    #TODO: explain how this works and why
    def make_card_clickable(self, card, function):
        #applies the bind to the original card, and changes pointer
        card.bind("<Button-1>", function)
        card.configure(cursor="hand2")

        #recursively adds binding to child elements
        for child_element in card.winfo_children():
            self.make_card_clickable(child_element, function)


    def create_empty_card(self):
        #makes a plain card with a blue background
        ttk.Style().configure("empty.TFrame", background=self.controller.COLORS["blue"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["blue"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        #label indicates no results were found
        label = ttk.Label(new_card, text="No results found!", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

    def create_search_card(self):
        #makes a plain card with a green background
        ttk.Style().configure("empty.TFrame", background=self.controller.COLORS["green"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["green"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="empty.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        #label indicates search is in progress
        label = ttk.Label(new_card, text="Searching...", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

    def create_error_card(self):
        #makes a plain card with a yellow background
        ttk.Style().configure("error.TFrame", background=self.controller.COLORS["red"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["red"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="error.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        #label displays default error message
        label = ttk.Label(new_card, text="Sorry, we encountered an error. Please try again later!", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

#TODO: explain the purpose of this class
class DetailsPage(ttk.Frame):

    #array to hold all the info frames
    sections = []

    #setup GUI
    def __init__(self, parent, controller):
        #initialize object
        super().__init__(parent)
        self.controller = controller

        #create an empty details page
        self.create_template()

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

        #configure heading to wrap on resize
        self.details_heading_panel.bind("<Configure>", lambda e: self.details_heading.config(wraplength=(e.width - 50)))

        #add a panel in the corner for the cost
        ttk.Style().configure("details_cost_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        self.details_cost_panel = ttk.Frame(self.details_topbar, style="details_cost_panel.TFrame", padding=10)
        self.details_cost_panel.grid(row=0, column=1, sticky="nsew")

        #add cost text
        ttk.Style().configure("details_cost.TLabel", justify="center", font=self.controller.FONTS["header"],
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

        #create a scrollbar by making a scroll bar and a canvas
        ttk.Style().configure("details_container.TFrame", background=self.controller.COLORS["white"])
        
        self.details_canvas = tk.Canvas(self.details_frame, bg=self.controller.COLORS["white"], highlightthickness=0)
        self.details_canvas.grid(row=0, column=0, sticky="nsew")

        self.details_scroll = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_canvas.yview)
        self.details_scroll.grid(row=0, column=1, sticky="ns")
        
        #configure the canvas to scroll when the scrollbar is moved
        self.details_canvas.configure(yscrollcommand=self.details_scroll.set)

        #create a frame container for the widgets,
        #and configure the canvas to fit the frame fully
        self.details_container = ttk.Frame(self.details_canvas, style="results_container.TFrame", padding=10)
        self.details_window = self.details_canvas.create_window((0,0), window=self.details_container, anchor="nw")

        self.details_container.bind("<Configure>", lambda e: self.details_canvas.configure(scrollregion=self.details_canvas.bbox("all")))
        self.details_canvas.bind("<Configure>", lambda e: self.details_canvas.itemconfig(self.details_window, width=e.width))

        #create a button at the bottom and configure it to return back to search screen upon click
        self.back_panel = ttk.Frame(self, style="details_border.TFrame", padding=10)
        self.back_panel.pack(side="bottom", fill="x")

        ttk.Style().configure("back.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("back.TButton",
            background=[("active", self.controller.COLORS["old_gold"]), ("pressed", self.controller.COLORS["old_gold"])])
        self.back_button = ttk.Button(self.back_panel, text="BACK", style="back.TButton", cursor="hand2")
        self.back_button.pack(fill="both", expand=True)
        self.back_button.configure(command=lambda: self.controller.search_page.tkraise())

    #TODO: explain what this does and why
    def fill_template(self, TripInfo):
        #clear sections
        for section in self.sections:
            section.destroy()

        self.sections.clear()

        #reset scrollbar
        self.details_canvas.yview_moveto(0)

        #update template
        self.details_heading.config(text=f"{TripInfo.start_date} - {TripInfo.end_date}")
        self.details_cost.config(text=f"{TripInfo.cost}")

        #add sections for outbound and return flight
        self.add_flight_info(TripInfo.outbound_flight, TripInfo.start_date, "Outbound Flight")
        self.add_flight_info(TripInfo.return_flight, TripInfo.end_date, "Return Flight")

    #TODO: explain why this is a separate function
    def add_flight_info(self, flightInfo, date, label):
        #create a panel to hold flight info
        flight_details_panel = ttk.Frame(self.details_container)
        flight_details_panel.pack(fill="x", pady=5)

        #make a topbar to list type of flight (departure vs. arrival), total flight time, and date
        ttk.Style().configure("flight_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        flight_topbar = ttk.Frame(flight_details_panel, style="flight_panel.TFrame", padding=10)
        flight_topbar.pack(side="top", fill="x")

        #add text to the topbar
        ttk.Style().configure("flight_heading.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().configure("flight_subheading.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        flight_heading = ttk.Label(flight_topbar, text=f"{label} ({flightInfo.total_duration})", style="flight_heading.TLabel")
        flight_heading.pack(side="top")
        flight_subheading = ttk.Label(flight_topbar, text=f"{date}", style="flight_subheading.TLabel")
        flight_subheading.pack(side="top")

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

        #allow resizing of text within flight_details_panel
        flight_details_panel.bind("<Configure>", lambda e: (
            flight_heading.config(wraplength=e.width),
            flight_subheading.config(wraplength=e.width)
        ))

        #cycle through all the legs and layovers to display them
        for i in range(len(flightInfo.legs)):
            #make a card with flight leg details
            flight_leg_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
            flight_leg_card.pack(side="top", fill="x", pady=5)

            #add the text to the flight leg details card
            flight_leg_title = ttk.Label(flight_leg_card, text=f"Flight: {flightInfo.legs[i].duration}", style="flight_details_label.TLabel")
            flight_leg_title.pack(side="top", fill="x")
            flight_leg_airplane = ttk.Label(flight_leg_card, text=f"Aircraft: {flightInfo.legs[i].aircraft}", style="flight_details_text.TLabel")
            flight_leg_airplane.pack(side="top", fill="x")
            flight_leg_departure = ttk.Label(flight_leg_card, text=f"Departure: {flightInfo.legs[i].times["departure"]} from {flightInfo.legs[i].airports["departure"]}", style="flight_details_text.TLabel")
            flight_leg_departure.pack(side="top", fill="x")
            flight_leg_arrival = ttk.Label(flight_leg_card, text=f"Arrival: {flightInfo.legs[i].times["arrival"]} from {flightInfo.legs[i].airports["arrival"]}", style="flight_details_text.TLabel")
            flight_leg_arrival.pack(side="top", fill="x")

            #allow resizing of text within flight_leg_card
            flight_leg_card.bind("<Configure>", lambda e, 
                leg_title=flight_leg_title,
                leg_airplane=flight_leg_airplane,
                leg_departure=flight_leg_departure,
                leg_arrival=flight_leg_arrival: (
                    leg_title.config(wraplength=e.width-20),
                    leg_airplane.config(wraplength=e.width-20),
                    leg_departure.config(wraplength=e.width-20),
                    leg_arrival.config(wraplength=e.width-20)
            ))

            if i < len(flightInfo.legs) - 1:
                #create a layover card in between each flight leg
                flight_layover_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
                flight_layover_card.pack(side="top", fill="x", pady=5)

                flight_layover_title = ttk.Label(flight_layover_card, text=f"Layover: {flightInfo.layovers[i].duration}", style="flight_details_label.TLabel")
                flight_layover_title.pack(side="top", fill="x")
                flight_layover_airport = ttk.Label(flight_layover_card, text=f"Airport: {flightInfo.layovers[i].airport}", style="flight_details_text.TLabel")
                flight_layover_airport.pack(side="top", fill="x")

                #allow resizing of text within flight_leg_layover_card
                flight_layover_card.bind("<Configure>", lambda e, 
                    layover_title = flight_layover_title,
                    layover_airport = flight_layover_airport: (
                        layover_title.config(wraplength=e.width-20),
                        layover_airport.config(wraplength=e.width-20)
                ))
            
        #finally, add flight info card to sections list
        self.sections.append(flight_details_panel)

#create a GUI with no functionality if run as standalone
if __name__ == "__main__":
    gui = FlightGUI()
    gui.mainloop()
