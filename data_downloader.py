import tkinter as tk
from tkinter import ttk
import csv
import os
import glob


class SearchableComboBox:
    """A ListBox class that provides a searchable dropdown list."""
    def __init__(self, entry_widget, options):
        self.options = options  # List of options for the dropdown
        self.entry = entry_widget  # External Entry widget to display dropdown
        
        # Bind the Entry widget to filter and display the dropdown
        self.entry.bind("<KeyRelease>", self.on_entry_key)  # Filter options as keys are pressed
        self.entry.bind("<FocusIn>", self.show_dropdown)  # Show dropdown when entry is focused

        # Create Listbox as a dropdown
        self.listbox = tk.Listbox(self.entry.master, height=5, width=30)  # Place dropdown in the same parent widget
        self.listbox.bind("<<ListboxSelect>>", self.on_select)  # Selects the chosen option from the dropdown
        self.listbox.bind("<FocusOut>", self.hide_dropdown)  # Hide dropdown when focus is lost

        # Populate listbox initially with all options
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        """Filter options based on typed input and update dropdown list."""
        typed_value = self.entry.get().strip().lower()  # Get and normalize input text
        self.listbox.delete(0, tk.END)  # Clear previous options

        if not typed_value:  # Show all options if no input
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            # Filter options starting with the typed input
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)  # Populate listbox with filtered options

        self.show_dropdown()  # Ensure dropdown is visible with updated options

    def on_select(self, event):
        """Set the selected option in the entry widget and hide the dropdown."""
        selected_index = self.listbox.curselection()
        if selected_index:  # If an option was selected
            selected_option = self.listbox.get(selected_index)  # Get selected option
            self.entry.delete(0, tk.END)  # Clear current entry text
            self.entry.insert(0, selected_option)  # Insert selected option into entry
        self.hide_dropdown()  # Hide dropdown after selecting an option

    def show_dropdown(self, event=None):
        """Display the dropdown list just below the entry widget."""
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")  # Position listbox below entry
        self.listbox.lift()  # Bring listbox to the front

    def hide_dropdown(self, event=None):
        """Hide the dropdown list."""
        self.listbox.place_forget()  # Remove listbox from display


class BudgetApp:
    """Main application class for the Budget Manager."""
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Manager")
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.main_screen()  # Display main screen

    def find_csv_file(self, root_folder, target_filename="world_population.csv"):
        """Recursively search for a file starting from root_folder."""
        for dirpath, _, filenames in os.walk(root_folder):
            if target_filename in filenames:
                return os.path.join(dirpath, target_filename)  # Return the full path of the file
        return None  # Return None if the file is not found

    def read_countries_from_csv(self, filename):
        """Reads the country names from the CSV file."""
        countries = []
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                countries.append(row['Country/Territory'])  # Get country name from each row
        return countries

    def main_screen(self):
        """Screen for searching countries."""
        self.clear_frame(self.main_frame)  # Clear any existing widgets in main frame

        # Automatically search for the CSV file in the current directory and subdirectories
        file_path = self.find_csv_file(os.getcwd())

        if not file_path:
            print("CSV file not found!")
            return

        # Read countries from the CSV file
        countries = self.read_countries_from_csv(file_path)

        # Create entry field for country search
        country_search_var = tk.Entry(self.main_frame)  # Entry box for typing country name
        country_search_var.grid(row=1, column=0, pady=70)  # Position entry box

        # Create SearchableComboBox with the external entry widget
        SearchableComboBox(country_search_var, countries)  # Initialize dropdown with countries

    def clear_frame(self, frame):
        """Clear all widgets from a frame."""
        for widget in frame.winfo_children():
            widget.destroy()  # Destroy each widget in the frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Budget Manager")
    root.geometry("800x600")  # Set the window size to 800x600
    root.resizable(True, True)  # Allow resizing

    app = BudgetApp(root)
    root.mainloop()
