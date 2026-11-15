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

class searchPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.create_search_panel()

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
        self.start_date = DateEntry(self.input_panel)
        self.start_date.grid(row=1, column = 0, padx=5, pady=5)

        #create end date
        self.end_date = DateEntry(self.input_panel)
        self.end_date.grid(row=1, column = 1, padx=5, pady=5)

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

if __name__ == "__main__":
    gui = flightGUI()
    gui.mainloop()
