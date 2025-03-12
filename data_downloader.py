import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SearchableComboBox:
    """A ListBox class that provides a searchable dropdown list."""
    def __init__(self, entry_widget, options, on_select_callback):
        self.options = options
        self.entry = entry_widget
        self.on_select_callback = on_select_callback
        self.listbox = tk.Listbox(self.entry.master, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = self.entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        if not typed_value:
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)
            self.on_select_callback(selected_option)
        self.hide_dropdown()

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

    def hide_dropdown(self, event=None):
        self.listbox.place_forget()


class PopulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Population Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.file_path = self.find_csv_file(os.getcwd())
        self.countries, self.population_data = self.read_csv_data()
        self.selected_countries = []
        self.create_widgets()

    def find_csv_file(self, root_folder, filename="world_population.csv"):
        for dirpath, _, filenames in os.walk(root_folder):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def find_gdp_file(self, root_folder, filename="gdp.csv"):
        for dirpath, _, filenames in os.walk(root_folder):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_csv_data(self):
        if not self.file_path:
            print("CSV file not found!")
            return [], {}
        countries = []
        population_data = {}
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country/Territory']
                countries.append(country)
                population_data[country] = {
                    year: int(row[year]) for year in ['1970 Population', '1980 Population', '1990 Population',
                                                      '2000 Population', '2010 Population', '2015 Population',
                                                      '2020 Population', '2022 Population'] if year in row and row[year]
                }
                population_data[country]['Growth Rate'] = float(row['Growth Rate']) if row['Growth Rate'] else 0.0
        return countries, population_data

    def create_widgets(self):
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").grid(row=0, column=0, pady=5)
        
        # Create up to 5 Searchable ComboBoxes for country selection
        self.country_entries = []
        for i in range(5):
            entry = tk.Entry(self.main_frame)
            entry.grid(row=i+1, column=0, pady=5)
            self.country_entries.append(entry)
            SearchableComboBox(entry, self.countries, self.update_selected_countries)

        plot_button = ttk.Button(self.main_frame, text="Plot Population Trend", command=self.plot_population)
        plot_button.grid(row=6, column=0, pady=10)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, pady=10)

    def update_selected_countries(self, country):
        """Update selected countries list when a country is selected in any entry."""
        self.selected_countries = [entry.get() for entry in self.country_entries if entry.get()]

    def plot_population(self):
        """Plot the population growth of up to 5 selected countries."""
        if not self.selected_countries:
            print("No countries selected!")
            return
        
        # Clear the previous plot
        self.ax.clear()

        for country in self.selected_countries:
            if country not in self.population_data:
                print(f"Data not found for {country}.")
                continue

            # Extract population data for the country
            data = self.population_data[country]
            years = [int(year.split()[0]) for year in data.keys() if "Population" in year]
            populations = [data[year] for year in data.keys() if "Population" in year]

            # Plot the population trend for each selected country
            self.ax.plot(years, populations, marker='o', linestyle='-', label=country)

        # Customize plot appearance
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population in Millions")
        self.ax.set_title(f"Population Growth of Selected Countries")
        self.ax.legend()
        self.ax.grid(True)

        # Update the canvas inside Tkinter
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = PopulationApp(root)
    root.mainloop()
