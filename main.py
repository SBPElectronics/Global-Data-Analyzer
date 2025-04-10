import tkinter as tk
from tkinter import ttk, Menu
from data_downloader import PopulationApp, GDPApp  # Import both apps
from explore import open_dataset  # Import the function from explore.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TheDataAnalyser:
    def __init__(self, root):  
        self.root = root
        root.geometry("300x300")

        # Create a canvas to separate the menu
        canvas = tk.Canvas(root, height=2, width=400, highlightthickness=0)
        canvas.pack(fill="x")

        # Menu bar for Help and Contributors
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

        # Main frame for buttons
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack()  

        # Title label for the main window
        self.title = tk.Label(self.main_frame, text="The Global Data Analyzer")
        self.title.pack(fill="x", expand=True)

        # Button to see Population or GDP of a country
        self.single_data_button = tk.Button(
            self.main_frame,
            text="See GDP or Population of a Country",
            bg="blue",
            fg="white",
            command=self.open_single_data_app
        )
        self.single_data_button.pack(fill="x", expand=True)

        # Button to see both Population and GDP of a country
        self.both_data_button = tk.Button(
            self.main_frame,
            text="See Both GDP and Population of a Country",
            bg="green",
            fg="black",
            command=self.open_both_data_app
        )
        self.both_data_button.pack(fill="x", expand=True)

        # Pass 'root' when calling open_dataset
        self.dataset_button = tk.Button(self.main_frame, text="Open Dataset", command=lambda: open_dataset(root),
                                        bg="green",
                                        fg="black",)
        self.dataset_button.pack(fill = 'x', expand=True)

    def open_single_data_app(self):
        new_window = tk.Toplevel(self.root)
        PopulationApp(new_window)  # Open population data, or you could switch to GDPApp based on input

    def open_both_data_app(self):
        new_window = tk.Toplevel(self.root)
        BothDataApp(new_window)  # Open a new window to view both GDP and Population data

class BothDataApp:
    """Class to view both GDP and Population for a single country"""

    def __init__(self, root):
        self.root = root
        self.root.title("GDP and Population for a Country")
        
        # Frame to hold widgets
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        # Country selection input
        self.country_label = tk.Label(self.main_frame, text="Select a Country:")
        self.country_label.pack(pady=5)

        self.country_entry = tk.Entry(self.main_frame)
        self.country_entry.pack(pady=5)

        # Button to fetch both GDP and Population data
        self.plot_button = tk.Button(self.main_frame, text="Plot GDP and Population", command=self.plot_data)
        self.plot_button.pack(pady=5)

        # Create matplotlib figure for plotting
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)

        # Data for GDP and Population
        self.population_data = {}  # To be filled with real data
        self.gdp_data = {}  # To be filled with real data

        # Load your data (for now, just placeholders)
        self.load_data()

    def load_data(self):
        # Load Population data (this can come from a CSV or API)
        self.population_data = {
            "2020": 700000000,  # Example: for a country
            "2021": 705000000
        }

        # Load GDP data (this can come from a CSV or API)
        self.gdp_data = {
            "2020": 15000,  # Example GDP in USD
            "2021": 16000
        }

    def plot_data(self):
        self.ax.clear()

        # Extract years for plotting
        years = sorted(set(self.population_data.keys()).union(self.gdp_data.keys()))
        
        # Plot Population data
        population_values = [self.population_data.get(year, 0) for year in years]
        self.ax.plot(years, population_values, marker='o', label="Population", color="blue")

        # Plot GDP data
        gdp_values = [self.gdp_data.get(year, 0) for year in years]
        self.ax.plot(years, gdp_values, marker='o', label="GDP", color="green")

        # Set titles and labels
        self.ax.set_title("GDP and Population Over Time")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Values")
        self.ax.legend()

        # Redraw canvas
        self.canvas.draw()

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TheDataAnalyser(root)
    root.mainloop()
