import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mtick  # ✅ For formatting large numbers with commas


class SearchableComboBox:
    """Searchable dropdown (ListBox) attached to Entry."""

    def __init__(self, entry_widget, options, on_select_callback):
        self.options = options
        self.entry = entry_widget
        self.on_select_callback = on_select_callback
        self.listbox = tk.Listbox(self.entry.master, height=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.bind("<FocusOut>", self.hide_dropdown)

        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = self.entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for option in self.options:
            if typed_value in option.lower():
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        if self.listbox.curselection():
            selected_option = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)
            self.on_select_callback(selected_option)
        self.hide_dropdown()

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0)
        self.listbox.lift()

    def hide_dropdown(self, event=None):
        self.listbox.place_forget()


class PopulationApp:
    """Application to visualize world population and GDP trends."""

    def __init__(self, root):
        self.root = root
        self.root.title("Population and GDP Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ✅ Load Population and GDP data
        self.pop_file_path = self.find_csv_file("world_population.csv")
        self.gdp_file_path = self.find_csv_file("gdp.csv")

        self.countries, self.population_data = self.read_population_data()
        _, self.gdp_data = self.read_gdp_data()
        self.selected_countries = []
        self.create_widgets()

    def find_csv_file(self, filename):
        """Search for CSV files in the current directory."""
        for dirpath, _, filenames in os.walk(os.getcwd()):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_population_data(self):
        """Read population data from CSV."""
        if not self.pop_file_path:
            print("Population CSV file not found!")
            return [], {}
        countries, population_data = [], {}
        with open(self.pop_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country/Territory']
                countries.append(country)
                population_data[country] = {}
                for year_col in ['1970 Population', '1980 Population', '1990 Population',
                                 '2000 Population', '2010 Population', '2015 Population',
                                 '2020 Population', '2022 Population']:
                    year = int(year_col.split()[0])
                    value = row.get(year_col, "").replace(",", "")
                    if value.isdigit():
                        population_data[country][year] = int(value)
        return countries, population_data

    def read_gdp_data(self):
        """Read GDP data from CSV."""
        if not self.gdp_file_path:
            print("GDP CSV file not found!")
            return [], {}
        countries, gdp_data = [], {}
        with open(self.gdp_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country Name']
                countries.append(country)
                gdp_data[country] = {
                    int(year): float(row[year]) for year in row if year.isdigit() and row[year]
                }
        return countries, gdp_data

    def create_widgets(self):
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").pack(pady=5)
        self.entries = []
        for _ in range(5):
            entry = tk.Entry(self.main_frame)
            entry.pack(pady=5)
            self.entries.append(entry)
            SearchableComboBox(entry, self.countries, self.update_selected_countries)

        # ✅ Buttons for plotting
        ttk.Button(self.main_frame, text="Plot Population", command=self.plot_population).pack(pady=5)
        ttk.Button(self.main_frame, text="Plot GDP", command=self.plot_gdp).pack(pady=5)
        ttk.Button(self.main_frame, text="Plot Population and GDP", command=self.plot_population_and_gdp).pack(pady=10)

        # ✅ Create Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)

    def update_selected_countries(self, _=None):
        """Update the list of selected countries."""
        self.selected_countries = [e.get() for e in self.entries if e.get()]

    def plot_population(self):
        """Plot population trends."""
        self.ax.clear()
        for country in self.selected_countries:
            data = self.population_data.get(country)
            if data:
                years, populations = zip(*sorted(data.items()))
                self.ax.plot(years, populations, marker='o', linestyle='-', label=country)
        self.ax.set_title("Population Growth")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population")
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax.legend()
        self.canvas.draw()

    def plot_gdp(self):
        """Plot GDP trends."""
        self.ax.clear()
        for country in self.selected_countries:
            data = self.gdp_data.get(country)
            if data:
                years, gdps = zip(*sorted(data.items()))
                self.ax.plot(years, gdps, marker='x', linestyle='--', label=country)
        self.ax.set_title("GDP Over Time")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("GDP (USD)")
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax.legend()
        self.canvas.draw()

    def plot_population_and_gdp(self):
        """Plot Population and GDP together with two Y-axes."""
        self.ax.clear()
        self.ax2 = self.ax.twinx()  # ✅ Second Y-axis for GDP

        for country in self.selected_countries:
            pop_data = self.population_data.get(country, {})
            gdp_data = self.gdp_data.get(country, {})

            # ✅ Plot Population on left axis
            if pop_data:
                pop_years, populations = zip(*sorted(pop_data.items()))
                self.ax.plot(pop_years, populations, marker='o', linestyle='-', label=f"{country} Population", color='blue')

            # ✅ Plot GDP on right axis
            if gdp_data:
                gdp_years, gdps = zip(*sorted(gdp_data.items()))
                self.ax2.plot(gdp_years, gdps, marker='x', linestyle='--', label=f"{country} GDP", color='green')

        # ✅ Set axis labels and titles
        self.ax.set_title("Population and GDP Growth")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population")
        self.ax2.set_ylabel("GDP (USD)")

        # ✅ Add commas to both Y-axes
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

        # ✅ Add legends for both plots
        self.ax.legend(loc="upper left")
        self.ax2.legend(loc="upper right")

        # ✅ Update canvas to reflect the changes
        self.canvas.draw()

class GDPApp:
    """Application to visualize GDP trends."""
    def __init__(self, root):
        self.root = root
        self.root.title("GDP Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Find and load GDP data from CSV
        self.file_path = self.find_csv_file("gdp.csv")
        self.countries, self.gdp_data = self.read_csv_data()
        self.selected_countries = []

        # Create widgets (buttons, search boxes, canvas)
        self.create_widgets()

    def find_csv_file(self, filename):
        """Search for CSV file in current directory."""
        for dirpath, _, filenames in os.walk(os.getcwd()):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_csv_data(self):
        """Read the GDP data from CSV and store it in a dictionary."""
        if not self.file_path:
            print("GDP CSV file not found!")
            return [], {}
        countries, gdp_data = [], {}
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country Name']
                countries.append(country)
                gdp_data[country] = {
                    int(year): float(row[year]) for year in row if year.isdigit() and row[year]
                }
        return countries, gdp_data

    def create_widgets(self):
        """Create all UI widgets like search boxes, buttons, and the plot area."""
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").pack(pady=5)
        self.entries = []
        for _ in range(5):
            entry = tk.Entry(self.main_frame)
            entry.pack(pady=5)
            self.entries.append(entry)
            # Add searchable combo-box to select countries
            SearchableComboBox(entry, self.countries, self.update_selected_countries)

        # Add buttons for plotting Population, GDP, or Both
        ttk.Button(self.main_frame, text="Plot Population", command=self.plot_population).pack(pady=5)
        ttk.Button(self.main_frame, text="Plot GDP", command=self.plot_gdp).pack(pady=5)
        ttk.Button(self.main_frame, text="Plot Both", command=self.plot_population_and_gdp).pack(pady=5)

        # Create a Matplotlib figure and canvas to display plots
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)

    def update_selected_countries(self, _=None):
        """Update the list of selected countries."""
        self.selected_countries = [e.get() for e in self.entries if e.get()]

    def plot_population(self):
        """Plot population data for selected countries."""
        self.ax.clear()
        for country in self.selected_countries:
            data = self.population_data.get(country, {})
            if data:
                years, populations = zip(*sorted(data.items()))
                self.ax.plot(years, populations, marker='o', linestyle='-', label=f"{country} Population", color='blue')

        self.ax.set_title("Population Growth")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population")
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax.legend()
        self.canvas.draw()

    def plot_gdp(self):
        """Plot GDP data for selected countries."""
        self.ax.clear()
        for country in self.selected_countries:
            # Assuming you have a structure for GDP data for the selected country
            data = self.gdp_data.get(country, {})
            if data:
                years, gdps = zip(*sorted(data.items()))
                self.ax.plot(years, gdps, marker='x', linestyle='--', label=f"{country} GDP", color='green')

        self.ax.set_title("GDP Over Time")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("GDP (USD)")
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax.legend()
        self.canvas.draw()

    def plot_population_and_gdp(self):
        """Plot both Population and GDP on the same graph with dual Y-axes."""
        self.ax.clear()
        self.ax2 = self.ax.twinx()  # Create secondary Y-axis for GDP

        for country in self.selected_countries:
            # Plot Population data
            pop_data = self.population_data.get(country, {})
            if pop_data:
                pop_years, populations = zip(*sorted(pop_data.items()))
                self.ax.plot(pop_years, populations, marker='o', linestyle='-', label=f"{country} Population", color='blue')

            # Plot GDP data
            gdp_data = self.gdp_data.get(country, {})
            if gdp_data:
                gdp_years, gdps = zip(*sorted(gdp_data.items()))
                self.ax2.plot(gdp_years, gdps, marker='x', linestyle='--', label=f"{country} GDP", color='green')

        # Labels and titles for both Y-axes
        self.ax.set_title("Population and GDP Trends")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population", color='blue')
        self.ax2.set_ylabel("GDP (USD)", color='green')

        # Formatting Y-axes for commas
        self.ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        self.ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

        # Legends for both axes
        self.ax.legend(loc="upper left")
        self.ax2.legend(loc="upper right")

        self.canvas.draw()



# ✅ Alias GDPApp to PopulationApp to keep both buttons working
GDPApp = PopulationApp
