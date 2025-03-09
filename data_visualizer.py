import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SearchableComboBox:
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

class GDPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP Trends")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.file_path = self.find_csv_file(os.getcwd())
        self.countries, self.gdp_data = self.read_csv_data()
        self.selected_countries = []
        self.create_widgets()

    def find_csv_file(self, root_folder, filename="world_gdp.csv"):
        for dirpath, _, filenames in os.walk(root_folder):
            if filename in filenames:
                return os.path.join(dirpath, filename)
        return None

    def read_csv_data(self):
        if not self.file_path:
            print("CSV file not found!")
            return [], {}
        countries = []
        gdp_data = {}
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = row['Country']
                countries.append(country)
                gdp_data[country] = {
                    year: float(row[year]) for year in row.keys() if year.isdigit() and row[year]
                }
        return countries, gdp_data

    def create_widgets(self):
        ttk.Label(self.main_frame, text="Select up to 5 Countries:").grid(row=0, column=0, pady=5)
        self.country_entries = []
        for i in range(5):
            entry = tk.Entry(self.main_frame)
            entry.grid(row=i+1, column=0, pady=5)
            self.country_entries.append(entry)
            SearchableComboBox(entry, self.countries, self.update_selected_countries)
        plot_button = ttk.Button(self.main_frame, text="Plot GDP Trend", command=self.plot_gdp)
        plot_button.grid(row=6, column=0, pady=10)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, pady=10)

    def update_selected_countries(self, country):
        self.selected_countries = [entry.get() for entry in self.country_entries if entry.get()]

    def plot_gdp(self):
        if not self.selected_countries:
            print("No countries selected!")
            return
        self.ax.clear()
        for country in self.selected_countries:
            if country not in self.gdp_data:
                print(f"Data not found for {country}.")
                continue
            data = self.gdp_data[country]
            years = sorted(map(int, data.keys()))
            gdp_values = [data[str(year)] for year in years]
            self.ax.plot(years, gdp_values, marker='o', linestyle='-', label=country)
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("GDP in Trillions USD")
        self.ax.set_title("GDP Growth of Selected Countries")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = GDPApp(root)
    root.mainloop()
