import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd

def open_dataset(parent):
    # Open file dialog to select a dataset
    file_path = filedialog.askopenfilename(title="Select Dataset",
                                           filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
    if file_path:
        display_dataset(parent, file_path)

def display_dataset(parent, file_path):
    # Create a new window to display the dataset
    data_window = tk.Toplevel(parent)  # Use the parent (main window)
    data_window.title("Dataset Viewer")
    data_window.geometry("800x500")

    # Read the dataset (CSV or Excel)
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        messagebox.showerror("Error", "Unsupported file format")
        return

    # Create Treeview widget to display the dataset in a table
    tree = ttk.Treeview(data_window)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    # Set column headers
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Insert data into the treeview (table)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")