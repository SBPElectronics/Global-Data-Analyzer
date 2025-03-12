import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
    """Application to visualize world population trends."""

    def __init__(self, root):
        self.root = root
        self.root.title("Population Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.file_path = self.find_csv_file("world_population.csv")
        self.countries, self.population_data = self.read_csv_data()
        self.selected_countries = []
        self.create_widgets()

    def find_csv_file(self, filename):
        for dirpath, _, filenames in os.walk(os.getcwd()):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_csv_data(self):
        if not self.file_path:
            print("Population CSV file not found!")
            return [], {}
        countries, population_data = [], {}
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country/Territory']
                countries.append(country)
                population_data[country] = {}
                # Collecting population data mapped by year
                for year_col in ['1970 Population', '1980 Population', '1990 Population',
                                '2000 Population', '2010 Population', '2015 Population',
                                '2020 Population', '2022 Population']:
                    year = int(year_col.split()[0])  # Extract year from column name
                    value = row.get(year_col, "").replace(",", "")  # Handle commas in large numbers
                    if value.isdigit():
                        population_data[country][year] = int(value)
        return countries, population_data

    def create_widgets(self):
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").pack(pady=5)
        self.entries = []
        for _ in range(5):
            entry = tk.Entry(self.main_frame)
            entry.pack(pady=5)
            self.entries.append(entry)
            SearchableComboBox(entry, self.countries, self.update_selected_countries)

        ttk.Button(self.main_frame, text="Plot Population Trend", command=self.plot_population).pack(pady=10)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)

    def update_selected_countries(self, _=None):
        self.selected_countries = [e.get() for e in self.entries if e.get()]

    def plot_population(self):
        self.ax.clear()
        for country in self.selected_countries:
            data = self.population_data.get(country)
            if data:
                years, populations = zip(*sorted(data.items()))
                self.ax.plot(years, populations, marker='o', label=country)
        self.ax.set_title("Population Growth")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Population")
        self.ax.legend()
        self.canvas.draw()


class GDPApp:
    """Application to visualize GDP trends."""

    def __init__(self, root):
        self.root = root
        self.root.title("GDP Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.file_path = self.find_csv_file("gdp.csv")
        self.countries, self.gdp_data = self.read_csv_data()
        self.selected_countries = []
        self.create_widgets()

    def find_csv_file(self, filename):
        for dirpath, _, filenames in os.walk(os.getcwd()):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_csv_data(self):
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
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").pack(pady=5)
        self.entries = []
        for _ in range(5):
            entry = tk.Entry(self.main_frame)
            entry.pack(pady=5)
            self.entries.append(entry)
            SearchableComboBox(entry, self.countries, self.update_selected_countries)

        ttk.Button(self.main_frame, text="Plot GDP Trend", command=self.plot_gdp).pack(pady=10)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)

    def update_selected_countries(self, _=None):
        self.selected_countries = [e.get() for e in self.entries if e.get()]

    def plot_gdp(self):
        self.ax.clear()
        for country in self.selected_countries:
            data = self.gdp_data.get(country)
            if data:
                years, gdps = zip(*sorted(data.items()))
                self.ax.plot(years, gdps, marker='o', label=country)
        self.ax.set_title("GDP Over Time")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("GDP (USD)")
        self.ax.legend()
        self.canvas.draw()
