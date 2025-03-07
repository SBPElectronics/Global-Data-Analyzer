import tkinter as tk
from tkinter import ttk
from data_downloader import PopulationApp  # Import PopulationApp class

class TheDataAnalyser:
    def __init__(self, root):  
        self.root = root
        root.geometry("300x300")
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding=10)  
        self.main_frame.pack()  
        self.title = tk.Label(self.main_frame, text="The Global Data Analyzer")
        self.title.pack(fill = "x", expand = True ) 

        # Button to open PopulationApp
        self.population_button = tk.Button(
            self.main_frame, 
            text="See Population of Countries", 
            bg="red", 
            fg="black", 
            command=self.open_population_app  # Calls the function
        )
        self.population_button.pack(fill="x", expand=True)  

    def open_population_app(self):
        new_window = tk.Toplevel(self.root)  # Create a new window
        PopulationApp(new_window)  # Open PopulationApp in the new window

if __name__ == "__main__":
    root = tk.Tk()
    app = TheDataAnalyser(root)  
    root.mainloop()
