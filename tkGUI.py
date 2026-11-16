import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

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

        self.create_result_card("1")
        self.create_result_card("2")
        self.create_result_card("3")
        self.create_result_card("4")

    def create_result_card(self, flight_info):
        #add a result card to search page panel
        self.result_cards.append(self.homePage.create_result_card(flight_info))


class searchPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.create_search_panel()
        self.create_results_panel()


    def create_search_panel(self):
        #create panel for date search, and make it maintain aspect ratio
        search_style = ttk.Style().configure("search.TFrame", background="#7280bf")
        self.search_panel = ttk.Frame(self, style="search.TFrame")
        self.search_panel.pack(fill="x")
        self.bind("<Configure>", self.resize_search_panel)

        #create panel to house input
        self.input_panel = ttk.Frame(self.search_panel, style="search.TFrame")
        self.input_panel.place(relx=0.5, rely=0.5, anchor="center")

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
        submit_button = ttk.Button(self.input_panel, text="Search")
        submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

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

        #set min and max dates for each appropriately to prevent overstepping
        self.start_date.config(maxdate=self.end_date.get_date())
        self.end_date.config(mindate=self.start_date.get_date())



    def create_results_panel(self):
        #create panel to display cards of search results
        results_style = ttk.Style().configure("results.TFrame", background="#545c80")
        self.results_panel = ttk.Frame(self, style="results.TFrame")
        self.results_panel.pack(fill="both", expand=True)

        #create a frame to house scrollbar
        self.results_frame = ttk.Frame(self.results_panel, style="results.TFrame")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.results_frame.grid_rowconfigure(0, weight=1)


        #create a scrollbar by making a scroll bar, a canvas, and a holder 
        container_style = ttk.Style().configure("results_container.TFrame", background="#ffffff")
        
        self.results_canvas = tk.Canvas(self.results_frame)
        self.results_canvas.grid(row=0, column=0, sticky="nsew")

        self.results_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_scroll.grid(row=0, column=1, sticky="ns")

        self.results_canvas.configure(yscrollcommand=self.results_scroll.set)

        self.results_container = ttk.Frame(self.results_canvas, style="results_container.TFrame", padding=10)
        self.results_window = self.results_canvas.create_window((0,0), window=self.results_container, anchor="nw")


        self.results_container.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.itemconfig(self.results_window, width=e.width))
        

    def create_result_card(self, flight_info):
        #makes a card to display a possible flight 
        card_style = ttk.Style().configure("result_card.TFrame", background="#000000")
        new_card = ttk.Frame(self.results_container, style="result_card.TFrame", padding=(10, 10))
        new_card.pack(fill="x", pady=5)

        label = ttk.Label(new_card, text=flight_info)
        label.pack(side="top", padx=10, pady=10)

        return new_card

if __name__ == "__main__":
    gui = flightGUI()
    gui.mainloop()
