import tkinter as tk
from tkinter import ttk, Menu
from data_downloader import PopulationApp  # Import PopulationApp class
from data_visualizer import GDPApp  # Import GDPApp class

class TheDataAnalyser:
    def __init__(self, root):  
        self.root = root
        root.geometry("300x300")

        canvas = tk.Canvas(root, height=2, width=400, highlightthickness=0) # Draws a line between the two labels for a neat look
        canvas.pack(fill = "x") # The placingxt="Home")

        menubar = Menu(root) # Creates the toolbar at the top
        self.root.config(menu=menubar) 

        helpMenu = Menu(menubar, tearoff=0) 
        helpMenu.add_command(label="About") # New button
        helpMenu.add_command(label="Check For Updates") # Open button
        menubar.add_cascade(label="Help", menu=helpMenu) # File dropdown


        collaboratorMenu = Menu(menubar, tearoff=0) 
        collaboratorMenu.add_command(label="hum-projects") 
        collaboratorMenu.add_command(label="SBPElectronics")
        collaboratorMenu.add_command(label="MAHPROJECTS")
        menubar.add_cascade(label="Contributors", menu=collaboratorMenu) # File dropdown



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
        
        # Button to open GDPApp
        self.gdp_button = tk.Button(
            self.main_frame, 
            text="See GDP of Countries", 
            bg="blue", 
            fg="white", 
            command=self.open_gdp_app  # Calls the function
        )
        self.gdp_button.pack(fill="x", expand=True)  

    def open_population_app(self):
        new_window = tk.Toplevel(self.root)  # Create a new window
        PopulationApp(new_window)  # Open PopulationApp in the new window

    def open_gdp_app(self):
        new_window = tk.Toplevel(self.root)  # Create a new window
        GDPApp(new_window)  # Open GDPApp in the new window

if __name__ == "__main__":
    root = tk.Tk()
    app = TheDataAnalyser(root)  
    root.mainloop()

