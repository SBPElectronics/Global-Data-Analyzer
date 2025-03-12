# main.py

import tkinter as tk
from tkinter import ttk, Menu
from data_downloader import PopulationApp, GDPApp  # Import both apps

class TheDataAnalyser:
    def __init__(self, root):  
        self.root = root
        root.geometry("300x300")

        canvas = tk.Canvas(root, height=2, width=400, highlightthickness=0)
        canvas.pack(fill="x")

        menubar = Menu(root)
        self.root.config(menu=menubar) 

        helpMenu = Menu(menubar, tearoff=0) 
        helpMenu.add_command(label="About")
        helpMenu.add_command(label="Check For Updates")
        menubar.add_cascade(label="Help", menu=helpMenu)

        collaboratorMenu = Menu(menubar, tearoff=0)
        collaboratorMenu.add_command(label="hum-projects")
        collaboratorMenu.add_command(label="SBPElectronics")
        collaboratorMenu.add_command(label="MAHPROJECTS")
        menubar.add_cascade(label="Contributors", menu=collaboratorMenu)

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack()  

        self.title = tk.Label(self.main_frame, text="The Global Data Analyzer")
        self.title.pack(fill="x", expand=True)

        # Population button
        self.population_button = tk.Button(
            self.main_frame,
            text="See Population of Countries",
            bg="red",
            fg="black",
            command=self.open_population_app
        )
        self.population_button.pack(fill="x", expand=True)

        # GDP button
        self.gdp_button = tk.Button(
            self.main_frame,
            text="See GDP of Countries",
            bg="blue",
            fg="white",
            command=self.open_gdp_app
        )
        self.gdp_button.pack(fill="x", expand=True)

    def open_population_app(self):
        new_window = tk.Toplevel(self.root)
        PopulationApp(new_window)

    def open_gdp_app(self):
        new_window = tk.Toplevel(self.root)
        GDPApp(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = TheDataAnalyser(root)
    root.mainloop()
