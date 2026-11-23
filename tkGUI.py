import tkinter as tk
from tkinter import ttk, font
from tkcalendar import DateEntry
from datetime import date
from fli.search import SearchFlights

#The class FlightGUI is dedicated to creating the GUI
#for the program. It by itself doesn't do much. Rather, 
#the tkinter widgets are actually built by two other
#classes, SearchPage and DetailsPage. I chose separate
#the tkinter code used to build the app's two pages into
#separate classes to keep each page's functionality separate. 
#This way, it is easier to track what each page contributes
#to the program's functionality, and FlightGUI doesn't become
#extremely long and confusing to read. FlightGUI serves as
#the root for the UI - it initializes Tkinter,
#stores the colors and fonts used by the 2 pages, builds the 
#2 pages upon init, and provides helper functions for main.py
#to interact with SearchPage and DetailsPage.
class FlightGUI(tk.Tk):

    result_cards = []

    def __init__(self):
        super().__init__()

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
    
        self.FONTS = {
            "title": font.Font(family="Helvetica", size=15, weight="bold"),
            "subtitle": font.Font(family="Helvetica", size=12),
            "header": font.Font(family="Helvetica", size=10, weight="bold"),
            "label": font.Font(family="Helvetica", size=8, weight="bold"),
            "regular": font.Font(family="Helvetica", size=8)
        }

        self.title("Personalized Flight Trips Search!")
        self.geometry("350x450+50+50")
        self.minsize(300,450)
        ttk.Style().theme_use("clam")

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.search_page = SearchPage(self.container, self)
        self.search_page.grid(row=0, column=0, sticky="nsew")

        self.details_page = DetailsPage(self.container, self)
        self.details_page.grid(row=0, column=0, sticky="nsew")

        self.search_page.tkraise()   

    #create_result_card(), delete_result_cards(), and create_message_card()
    #all interact with SearchPage's results_panel to display information. 
    #I could technically have made these within SearchPage itself, but I 
    #wanted to keep them in FlightGUI so that main doesn't have to access
    #FlightGUI.search_page. FlightGUI handles that itself. FlightGUI takes
    #responsibility of managing the current cards and deleting them upon reset.
    #It does this by storing all the tkinter Frames in result_cards[],
    #and iteratively deleting each one.

    def create_result_card(self, TripInfo):
        self.result_cards.append(self.search_page.create_result_card(TripInfo))

    def delete_result_cards(self):
        for card in self.result_cards:
            card.destroy()

        self.result_cards.clear()

        self.search_page.results_canvas.yview_moveto(0)

    #Unlike result cards, which displays different information,
    #message cards just show generic text. Since no parameters
    #are needed to draw these cards, I got rid of the individual
    #functions to draw each type of card and merged them into 
    #a single function. main.py can specify which kind of card it wants
    #by typing the keywords used in the below match statement
    def create_message_card(self, type):
        match type:
            case "no_results":
                self.result_cards.append(self.search_page.create_empty_card())
                return
            case "searching":
                self.result_cards.append(self.search_page.create_search_card())
                return
            case "error":
                self.result_cards.append(self.search_page.create_error_card())
                return
            case _:
                self.result_cards.append(self.search_page.create_error_card())
                return

    #open_details() is actually a function used by SearchPage.
    #When a result card is clicked, the UI switches to a more
    #detailed page showing information specific to the flight
    #legs and layovers. I chose to put this function in FlightGUI
    #rather than SearchPage because it interacts solely with DetailsPage,
    #which SearchPage doesn't have direct access to. This function
    #routes SearchPage to interact with DetailsPage through FlightGUI.
    def open_details(self, TripInfo):
        self.details_page.fill_template(TripInfo)
        self.details_page.tkraise()

#This class does most of the heavy lifting for FlightGUI,
#because it creates the search page. The search page
#has two main sections: the search panel and the results panel.
#The search panel the interface where the user can enter
#their travel dates via DateTime entries and submit them 
#to search.py. The results panel creates a scrollbar 
#which will be populated with information cards showing the 
#program's status or the invididual roundtrips found by search.py.
#The results panel also has an option to export the found
#results to an excel sheet. It is worth noting that
#SearchPage itself doesn't perform the fli search and
#doesn't generate the excel sheet. These actions are
#assigned to SearchPage's buttons by main.py at initializaton.
class SearchPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_search_panel()
        self.create_results_panel()

    #This function creates the top half of SearchPage's UI,
    #where the user can specify their travel dates and submit them.
    #I separated the code building the widgets for the search_panel
    #from building the results panel for readability. Both sections
    #are standalone, so it is easier to organize the code to build
    #them separately than together in one long function. There is
    #a lot going on in this function, but to summarize, it creates a
    #frame with a title, subtitle, two DateEntry fields with labels, and
    #a submit button.
    def create_search_panel(self):
        ttk.Style().configure("search.TFrame", background=self.controller.COLORS["black"])
        self.search_panel = ttk.Frame(self, style="search.TFrame", padding=10)
        self.search_panel.pack(fill="x")
        self.bind("<Configure>", self.resize_search_panel)

        self.title_panel = ttk.Frame(self.search_panel, style="search.TFrame", padding=10)
        self.title_panel.pack(side="top")

        ttk.Style().configure("title.TLabel", font=self.controller.FONTS["title"], 
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["campus_gold"])
        ttk.Style().configure("subtitle.TLabel", font=self.controller.FONTS["subtitle"], 
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["old_gold"])
        self.title = ttk.Label(self.title_panel, text="GET ME OUT OF HERE!",
            style="title.TLabel", justify="center")
        self.title.grid(row=0, column=0)

        self.subtitle = ttk.Label(self.title_panel, text="Search roundtrips between IND and DSM",
            style="subtitle.TLabel", justify="center")
        self.subtitle.grid(row=1, column=0)

        #This bind function allows the title to wraparound
        #when the window is resized. I added this because I
        #noticed that the large text would flow off the window
        #when I made the width really small. The tkinter Labels'
        #wraparound limits are dynamically adjusted to be proportional
        #to the width of the search panel. I include very similar 
        #bindings to other elements such as the text within
        #results cards, the heading on the details page, 
        #and the text on the results page. I'm not going
        #to clarify them because they operate very similarly.
        self.search_panel.bind("<Configure>", lambda e: (
            self.title.config(wraplength=e.width-40),
            self.subtitle.config(wraplength=e.width-40)
        ))

        self.input_panel = ttk.Frame(self.search_panel, style="search.TFrame")
        self.input_panel.pack()

        ttk.Style().configure("search_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["white"])

        start_date_label = ttk.Label(self.input_panel, text="Outbound Date:", style="search_label.TLabel")
        start_date_label.grid(row=0, column = 0, padx=5, pady=5)

        end_date_label = ttk.Label(self.input_panel, text="Return Date:", style="search_label.TLabel")
        end_date_label.grid(row=0, column = 1, padx=5, pady=5)
        
        #create start date and end date selectors
        ttk.Style().configure("field.DateEntry")

        #The below dictionary stores the styling for the 
        #calendar dropdown portion of the DateEntry fields.
        #Unlike the text input field of the DateEntry, which
        #can be styled using ttk, the calendars are build in 
        #regular tkinter and must be styled separately via
        #arguments upon initialization. The style arguments
        #are stored in a dictionary so that they
        #are shared between the two DateEntry widgets.
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

        self.end_date.bind("<<DateEntrySelected>>", self.regulate_dates)
        self.start_date.bind("<<DateEntrySelected>>", self.regulate_dates)

        self.end_date.bind("<FocusOut>", self.regulate_dates)
        self.start_date.bind("<FocusOut>", self.regulate_dates)

        #Here, we are binding all the elements to become focused
        #when they are clicked. This prevents the DateTime
        #popups from staying open forever by closing them
        #as soon as something else is clicked.
        self.bind_all("<Button-1>",  lambda e: e.widget.focus_set())

        ttk.Style().configure("submit.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("submit.TButton",
            background=[("active", self.controller.COLORS["old_gold"]), ("pressed", self.controller.COLORS["old_gold"])])
        self.submit_button = ttk.Button(self.input_panel, text="SEARCH", style="submit.TButton", cursor="hand2")
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    #I wanted the search panel to maintain a 3:2 ratio
    #for aesthetic purposes. Tkinter has no way to enforce this
    #so the below function is bound to the search panel to update its
    #height to be a proportion of its width. I also cap the max height to
    #40% of the window height so that a wide window doesn't have
    #the panel taking up most of the screen.
    def resize_search_panel(self, event):
        aspect_ratio = 3 / 2
        max_height_proportion = 0.4

        new_height = int(event.width / aspect_ratio)
        max_height = int(self.winfo_height() * max_height_proportion)

        new_height = min(new_height, max_height)

        self.search_panel.config(height=new_height)

    #Initially, I was planning for the program to raise an error
    #when the start date was after the end date. I then realized that
    #it would be more convenient for the user if this issue was immediately
    #resolved by setting both dates to date that was most recently inputted.
    #This way, the user doesn't have to worry about errors when submitting.
    #The below function does exactly that whenever the user selects a date
    #on the calendar popup or types in the date manually.
    def regulate_dates(self, event):
        if (self.start_date.get_date() > self.end_date.get_date()):
            if event.widget == self.start_date:
                self.end_date.set_date(self.start_date.get_date())
            else:
                self.start_date.set_date(self.end_date.get_date())

    #The function below creates the second half of the search page,
    #the results panel. First, it creates a bar at the bottom that
    #shows the total amount of results found after a search, and
    #shows an export button (that is only visible when there are results)
    #The second half creates a scrollbar to house all the message and result cards.
    #As mentioned before, I made building the results_panel separate from 
    #building the search panel for simplicity and some form of code organization.
    #The two sections do not depend on each other, so they can be added separately
    #during SearchPage's initialization.
    def create_results_panel(self):
        ttk.Style().configure("results_border.TFrame", background=self.controller.COLORS["gray"])
        self.export_panel = ttk.Frame(self, style="results_border.TFrame", padding=10)
        self.export_panel.pack(side="bottom", fill="x")
        self.export_panel.columnconfigure(0, weight=3, uniform="columns")
        self.export_panel.columnconfigure(1, weight=2, uniform="columns")

        ttk.Style().configure("results_num.TLabel", justify="left", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["gray"],
            foreground=self.controller.COLORS["white"])
        self.results_count = ttk.Label(self.export_panel, text="Results: 0", style="results_num.TLabel")
        self.results_count.grid(row=0, column=0, sticky="nsew")
        self.export_panel.bind("<Configure>", lambda e: self.results_count.config(wraplength=(e.width/2)))

        ttk.Style().configure("export.TButton", font=self.controller.FONTS["label"], 
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().map("export.TButton",
            background=[("active", self.controller.COLORS["old_gold"]),("pressed", self.controller.COLORS["old_gold"])])
        self.export_button = ttk.Button(self.export_panel, text="EXPORT TO EXCEL", style="back.TButton", cursor="hand2")
        self.export_button.grid(row=0, column=1, sticky="nsew")
        self.export_button.grid_remove()
        
        self.results_panel = ttk.Frame(self, style="results_border.TFrame")
        self.results_panel.pack(fill="both", expand=True)

        self.results_frame = ttk.Frame(self.results_panel, style="results_border.TFrame")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.results_frame.grid_rowconfigure(0, weight=1)

        #The code below creates a scrollable frame. Tkinter doesn't allow frames
        #to be scrollable, so a parent frame must be stored within a 
        #canvas. I accomplish this by first creating the scrollbar and the canvas,
        #and linking the two to move together when the other is manipulated.
        #Then, I create a window on the canvas to display the parent frame, and the
        #window is dynamically resized to fit all of the parent frame's contents.
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

    #This function creates a card displaying trip information for
    #one of the results returned by search.py. Each result card is
    #independent of the other, and can be stored/deleted by FlightGUI.
    #The function takes in a TripInfo instance, which is passed in by
    #main.py. The function parses the values within the instance and
    #displays a summary of the outbound flight, return flight, and cost
    #in three columns. My inspiration for displaying the trip info as
    #separate cards rather than a big list is from the Google Flights UI itself.
    #Separating the results visually makes it easier to distinguish them from each other.
    def create_result_card(self, TripInfo):

        outbound_flight = TripInfo.outbound_flight
        return_flight = TripInfo.return_flight

        ttk.Style().configure("result_card.TFrame")
        new_card = ttk.Frame(self.results_container, style="result_card.TFrame")
        new_card.pack(fill="x", pady=5)
        new_card.columnconfigure(0, weight=3, uniform="columns")
        new_card.columnconfigure(1, weight=3, uniform="columns")
        new_card.columnconfigure(2, weight=2, uniform="columns")

        ttk.Style().configure("cost.TFrame", background=self.controller.COLORS["campus_gold"], padding=5)
        cost_panel = ttk.Frame(new_card, style="cost.TFrame")
        cost_panel.grid(row=0, column=2, sticky="nsew")

        ttk.Style().configure("cost.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        cost = ttk.Label(cost_panel, text=f"{TripInfo.cost}", style="cost.TLabel")
        cost.pack(expand=True)

        ttk.Style().configure("info.TFrame", background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_label.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["old_gold"])
        ttk.Style().configure("result_text.TLabel", font=self.controller.FONTS["regular"],
            background=self.controller.COLORS["old_gold"])

        outbound_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        outbound_panel.grid(row=0, column=0, sticky="nsew")

        outbound_airline = ttk.Label(outbound_panel, text=f"Outbound Flight: {outbound_flight.airline}", style="result_label.TLabel")
        outbound_airline.pack(anchor="w")

        outbound_string = ""
        for i in range(len(outbound_flight.airports)):
            if (i != 0):
                outbound_string += "→"
            outbound_string += f"{outbound_flight.airports[i]}"
        
        outbound_order = ttk.Label(outbound_panel, text=outbound_string, style="result_text.TLabel")
        outbound_order.pack(anchor="w")

        outbound_time = ttk.Label(outbound_panel, 
            text=f"{outbound_flight.departure_time} to {outbound_flight.arrival_time} ({outbound_flight.total_duration})",
            style="result_text.TLabel")
        outbound_time.pack(anchor="w")

        outbound_panel.bind("<Configure>", lambda e: (
            outbound_airline.config(wraplength=e.width-15),
            outbound_order.config(wraplength=e.width-15),
            outbound_time.config(wraplength=e.width-15),
        ))

        return_panel = ttk.Frame(new_card, style="info.TFrame", padding=5)
        return_panel.grid(row=0, column=1, sticky="nsew")

        return_airline = ttk.Label(return_panel, text=f"Return Flight: {return_flight.airline}", style="result_label.TLabel")
        return_airline.pack(anchor="w")

        return_string = ""
        for i in range(len(return_flight.airports)):
            if (i != 0):
                return_string += "→"
            return_string += f"{return_flight.airports[i]}"
        
        return_order = ttk.Label(return_panel, text=return_string, style="result_text.TLabel")
        return_order.pack(anchor="w")

        return_time = ttk.Label(return_panel, 
            text=f"{return_flight.departure_time} to {return_flight.arrival_time} ({return_flight.total_duration})",
            style="result_text.TLabel")
        return_time.pack(anchor="w")

        return_panel.bind("<Configure>", lambda e: (
            return_airline.config(wraplength=e.width-15),
            return_order.config(wraplength=e.width-15),
            return_time.config(wraplength=e.width-15),
        ))

        self.make_card_clickable(new_card, lambda e: self.controller.open_details(TripInfo))

        return new_card

    #I wanted to make each result card redirect to a page with more
    #detailed info. When I tried binding the card frame itself to
    #mouse clicks, nothing happened. This is because the frame itself
    #was covered up by its child elements, so the mouse never actually
    #touches the parent frame. I fixed this problem by assigning all
    #the child widgets to respond to the click as well. The function below
    #does this by first applying the bind to the widget 
    #passed in as a parameter, and then recursively calling it on all the
    #child elements. This way, everything within the card redirects to 
    #the details page.
    def make_card_clickable(self, card, function):
        card.bind("<Button-1>", function)
        card.configure(cursor="hand2")

        for child_element in card.winfo_children():
            self.make_card_clickable(child_element, function)

    #The following three functions, create_empty_card(),
    #create_search_card(), and create_error_card() make plain
    #colored cards that display a message when no results are found,
    #when the search algorithm is running, and when an exception is thrown.
    #Thse three are run by a single function in FlightGUI, which calls upon
    #SearchPage to make an approprate message card based on a descriptive
    #keyword passed in as a parameter. 
    def create_empty_card(self):
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
        ttk.Style().configure("error.TFrame", background=self.controller.COLORS["red"])
        ttk.Style().configure("normal_text.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["red"],
            foreground=self.controller.COLORS["white"])

        new_card = ttk.Frame(self.results_container, style="error.TFrame", padding=10)
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text="Sorry, we encountered an error. Please try again later!", style="normal_text.TLabel")
        label.pack(expand="true")

        return new_card

#DetailsPage is a page that opens more specific information
#on a particular flight result, showing info on layovers
#and flight legs that aren't shown on the search page. 
#I originally wasn't planning on adding this feature when 
#planning the MVP, and was hoping to show all relevant information
#on the search page itself. I realized that there was way too much
#to show, so I simplified the search page results and added this
#page as an option to view the extra details. DetailsPage is initialized
#as an empty template and is hidden at init. When a result card is
#clicked, the template is populated with relevant information and
#the the page is shown in the place of the search page.
class DetailsPage(ttk.Frame):

    sections = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_template()

    #The template is created very similarly to the results_panel
    #of SearchPage. At the top, there is a heading showing the 
    #travel dates and the total trip cost. At the bottom, there
    #is a button that redirects back to the search page. And in
    #the center, there is a large scrolling frame designed exactly
    #as it was in SearchPage. The frame is created blank, and
    #relevant information will be added once a card is clicked.
    def create_template(self):
        ttk.Style().configure("details_topbar.TFrame", background=self.controller.COLORS["black"])
        self.details_topbar = ttk.Frame(self, style="details_topbar.TFrame")
        self.details_topbar.pack(side="top", fill="x")

        self.details_topbar.columnconfigure(0, weight=5, uniform="columns")
        self.details_topbar.columnconfigure(1, weight=1, uniform="columns")

        ttk.Style().configure("details_heading_panel.TFrame", background=self.controller.COLORS["black"])
        self.details_heading_panel = ttk.Frame(self.details_topbar, style="details_heading_panel.TFrame", padding=20)
        self.details_heading_panel.grid(row=0, column=0, sticky="nsew")

        ttk.Style().configure("details_dates.TLabel", justify="left", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["black"],
            foreground=self.controller.COLORS["white"])
        self.details_heading = ttk.Label(self.details_heading_panel, text="Monday November 23, 2026 - Monday November 23, 2026", style="details_dates.TLabel")
        self.details_heading.pack(side="left", fill="both", expand=True)

        self.details_heading_panel.bind("<Configure>", lambda e: self.details_heading.config(wraplength=(e.width - 50)))

        ttk.Style().configure("details_cost_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        self.details_cost_panel = ttk.Frame(self.details_topbar, style="details_cost_panel.TFrame", padding=10)
        self.details_cost_panel.grid(row=0, column=1, sticky="nsew")

        ttk.Style().configure("details_cost.TLabel", justify="center", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        self.details_cost = ttk.Label(self.details_cost_panel, text="$650", style="details_cost.TLabel")
        self.details_cost.place(relx=0.5,rely=0.5, anchor="center")

        ttk.Style().configure("details_border.TFrame", background=self.controller.COLORS["gray"])
        self.details_panel = ttk.Frame(self, style="details_border.TFrame")
        self.details_panel.pack(side="top", fill="both", expand=True)

        self.details_frame = ttk.Frame(self.details_panel, style="details_border.TFrame")
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=0)
        self.details_frame.grid_rowconfigure(0, weight=1)

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

    #This function is called when a result card is clicked.
    #Similar to how result cards are populated, the 
    #scrolling frame is cleared and then cards are added
    #to display information about the outbound and return flight.
    #The template's heading is also updated to display
    #the trip cost and travel dates. I thought it was convenient
    #to simply update the details page rather than generating
    #a new page each time. Therefore, fill template mainly
    #just updates the widgets on the details page.
    def fill_template(self, TripInfo):
        for section in self.sections:
            section.destroy()

        self.sections.clear()

        self.details_canvas.yview_moveto(0)

        self.details_heading.config(text=f"{TripInfo.start_date} - {TripInfo.end_date}")
        self.details_cost.config(text=f"{TripInfo.cost}")

        self.add_flight_info(TripInfo.outbound_flight, TripInfo.start_date, "Outbound Flight")
        self.add_flight_info(TripInfo.return_flight, TripInfo.end_date, "Return Flight")

    #This function creates a large card to display a one-way flight.
    #It takes in a FlightInfo instance to generate information,
    #as well as a date and label to correspondingly update the heading
    #with the day of travel and the kind of flight (outbound/return).
    #Within the large card, there are smaller cards that house information
    #for a flight leg or a layover. Once again, I wanted to make them into 
    #distinctive cards to make it easier for the user to visualize the different
    #"steps" that make up the entire one-way trip. Each time the template is filled,
    #the old cards are cleared and new ones are generated. This just to play it safe,
    #in the case a trip has more than 1 stop (they usually don't).
    def add_flight_info(self, FlightInfo, date, label):
        flight_details_panel = ttk.Frame(self.details_container)
        flight_details_panel.pack(fill="x", pady=5)

        ttk.Style().configure("flight_panel.TFrame", background=self.controller.COLORS["campus_gold"])
        flight_topbar = ttk.Frame(flight_details_panel, style="flight_panel.TFrame", padding=10)
        flight_topbar.pack(side="top", fill="x")

        ttk.Style().configure("flight_heading.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        ttk.Style().configure("flight_subheading.TLabel", font=self.controller.FONTS["label"],
            background=self.controller.COLORS["campus_gold"],
            foreground=self.controller.COLORS["white"])
        flight_heading = ttk.Label(flight_topbar, text=f"{label} ({FlightInfo.total_duration})", style="flight_heading.TLabel")
        flight_heading.pack(side="top")
        flight_subheading = ttk.Label(flight_topbar, text=f"{date}", style="flight_subheading.TLabel")
        flight_subheading.pack(side="top")

        ttk.Style().configure("flight_container.TFrame", background=self.controller.COLORS["old_gold"])
        flight_details_container = ttk.Frame(flight_details_panel, style="flight_container.TFrame", padding=10)
        flight_details_container.pack(side="top", fill="both", expand=True)

        ttk.Style().configure("flight_details_card.TFrame", background=self.controller.COLORS["white"])
        ttk.Style().configure("flight_details_label.TLabel", font=self.controller.FONTS["header"],
            background=self.controller.COLORS["white"])
        ttk.Style().configure("flight_details_text.TLabel", font=self.controller.FONTS["regular"],
            background=self.controller.COLORS["white"])

        flight_details_panel.bind("<Configure>", lambda e: (
            flight_heading.config(wraplength=e.width),
            flight_subheading.config(wraplength=e.width)
        ))

        #The following loop cycles through all the flight legs and layovers
        #within the FlightInfo instance, and creates a respective card.
        #It runs under the logic that there is always 1 less layover than there
        #are flight legs, so for every iteration except for the last, a layover card
        #is made after the leg card. This makes sure that the display alternates between
        #flight legs and layovers, as the occur in real life. Typically there are only
        #2 legs and 1 layover per trip, but the loop allows the program to update the display
        #appropriately in the case there is more than 1 stop.
        for i in range(len(FlightInfo.legs)):
            flight_leg_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
            flight_leg_card.pack(side="top", fill="x", pady=5)

            flight_leg_title = ttk.Label(flight_leg_card, text=f"Flight: {FlightInfo.legs[i].duration}", style="flight_details_label.TLabel")
            flight_leg_title.pack(side="top", fill="x")
            flight_leg_airplane = ttk.Label(flight_leg_card, text=f"Aircraft: {FlightInfo.legs[i].aircraft}", style="flight_details_text.TLabel")
            flight_leg_airplane.pack(side="top", fill="x")
            flight_leg_departure = ttk.Label(flight_leg_card, text=f"Departure: {FlightInfo.legs[i].times["departure"]} from {FlightInfo.legs[i].airports["departure"]}", style="flight_details_text.TLabel")
            flight_leg_departure.pack(side="top", fill="x")
            flight_leg_arrival = ttk.Label(flight_leg_card, text=f"Arrival: {FlightInfo.legs[i].times["arrival"]} from {FlightInfo.legs[i].airports["arrival"]}", style="flight_details_text.TLabel")
            flight_leg_arrival.pack(side="top", fill="x")

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

            if i < len(FlightInfo.legs) - 1:
                flight_layover_card = ttk.Frame(flight_details_container, style="flight_details_card.TFrame", padding=10)
                flight_layover_card.pack(side="top", fill="x", pady=5)

                flight_layover_title = ttk.Label(flight_layover_card, text=f"Layover: {FlightInfo.layovers[i].duration}", style="flight_details_label.TLabel")
                flight_layover_title.pack(side="top", fill="x")
                flight_layover_airport = ttk.Label(flight_layover_card, text=f"Airport: {FlightInfo.layovers[i].airport}", style="flight_details_text.TLabel")
                flight_layover_airport.pack(side="top", fill="x")

                flight_layover_card.bind("<Configure>", lambda e, 
                    layover_title = flight_layover_title,
                    layover_airport = flight_layover_airport: (
                        layover_title.config(wraplength=e.width-20),
                        layover_airport.config(wraplength=e.width-20)
                ))
            
        self.sections.append(flight_details_panel)

if __name__ == "__main__":
    gui = FlightGUI()
    gui.mainloop()
