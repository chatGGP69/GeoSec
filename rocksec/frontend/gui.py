# rocksec/frontend/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.topography import Topography
from models.contact import Contact
from models.rock_layer import RockLayer
from frontend.canvas_frame import ScrollableFrame
import pandas as pd
from tkinter import filedialog
from logic.plotting import advanced_plot_section


topography = Topography()
contacts = []
rock_layers = []
current_contact = None

rock_types = ["Limestone", "Sandstone", "Shale", "Basalt", "Conglomerate"]

def build_gui(root):
    global distance_entry, elevation_entry, surface_listbox
    global contact_name_entry, contact_distance_entry, contact_elevation_entry
    global contact_listbox, contact_points_listbox
    global layer_top_contact_dropdown, layer_bottom_contact_dropdown
    global rock_type_var, rock_type_dropdown, layers_listbox

    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill="both", expand=True)
    frame = scrollable_frame.scrollable_frame

    # Surface Points
    tk.Label(frame, text="Surface Point:").grid(row=0, column=0, columnspan=2)
    tk.Label(frame, text="Distance (m):").grid(row=1, column=0)
    distance_entry = tk.Entry(frame)
    distance_entry.grid(row=1, column=1)

    tk.Label(frame, text="Elevation (m):").grid(row=2, column=0)
    elevation_entry = tk.Entry(frame)
    elevation_entry.grid(row=2, column=1)

    tk.Button(frame, text="Add Surface Point", command=add_surface_point).grid(row=3, column=0, columnspan=2)
    tk.Button(frame, text="Delete Surface Point", command=delete_surface_point).grid(row=4, column=0, columnspan=2)
    tk.Button(frame, text="Load CSV File", command=load_csv_file).grid(row=5, column=2)

    surface_listbox = tk.Listbox(frame, width=40)
    surface_listbox.grid(row=5, column=0, columnspan=2)

    # Contacts
    tk.Label(frame, text="Contact Management:").grid(row=6, column=0, columnspan=2)
    contact_name_entry = tk.Entry(frame)
    contact_name_entry.grid(row=7, column=0, columnspan=2)

    tk.Button(frame, text="Start New Contact", command=start_new_contact).grid(row=8, column=0, columnspan=2)

    tk.Label(frame, text="Distance (m):").grid(row=9, column=0)
    contact_distance_entry = tk.Entry(frame)
    contact_distance_entry.grid(row=9, column=1)

    tk.Label(frame, text="Elevation (m):").grid(row=10, column=0)
    contact_elevation_entry = tk.Entry(frame)
    contact_elevation_entry.grid(row=10, column=1)

    tk.Button(frame, text="Add Contact Point", command=add_contact_point).grid(row=11, column=0, columnspan=2)
    tk.Button(frame, text="Save Contact", command=save_contact).grid(row=12, column=0, columnspan=2)

    contact_listbox = tk.Listbox(frame, width=40)
    contact_listbox.grid(row=13, column=0, columnspan=2)

    contact_points_listbox = tk.Listbox(frame, width=40)
    contact_points_listbox.grid(row=14, column=0, columnspan=2)

    # Rock Layers
    tk.Label(frame, text="Create Rock Layer:").grid(row=15, column=0, columnspan=2)
    layer_top_contact_dropdown = tk.Entry(frame)
    layer_top_contact_dropdown.grid(row=16, column=0)
    layer_bottom_contact_dropdown = tk.Entry(frame)
    layer_bottom_contact_dropdown.grid(row=16, column=1)

    rock_type_var = tk.StringVar()
    rock_type_dropdown = ttk.Combobox(frame, textvariable=rock_type_var, values=rock_types, state="readonly")
    rock_type_dropdown.grid(row=17, column=0, columnspan=2)

    tk.Button(frame, text="Create Layer", command=create_new_layer).grid(row=18, column=0, columnspan=2)

    layers_listbox = tk.Listbox(frame, width=40)
    layers_listbox.grid(row=19, column=0, columnspan=2)

    tk.Button(frame, text="Plot Section", command=lambda: advanced_plot_section(topography, contacts, rock_layers)
).grid(row=20, column=0, columnspan=2)

# === GUI Callbacks (shortened versions) ===

def add_surface_point():
    try:
        distance = float(distance_entry.get())
        elevation = float(elevation_entry.get())
        existing_distances, _ = topography.get_profile()
        if distance in existing_distances:
            messagebox.showerror("Duplicate Distance", "Point exists.")
            return
        topography.add_point(distance, elevation)
        surface_listbox.insert(tk.END, f"{distance}m, {elevation}m")
        distance_entry.delete(0, tk.END)
        elevation_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid numbers.")

def delete_surface_point():
    selection = surface_listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "No point selected.")
        return
    index = selection[0]
    surface_listbox.delete(index)
    topography.points.pop(index)

def start_new_contact():
    global current_contact
    name = contact_name_entry.get()
    if not name:
        messagebox.showerror("Error", "Name contact first.")
        return
    current_contact = Contact(name)
    contact_listbox.insert(tk.END, f"Started: {name}")

def add_contact_point():
    try:
        distance = float(contact_distance_entry.get())
        elevation = float(contact_elevation_entry.get())
        current_contact.add_point(distance, elevation)
        contact_points_listbox.insert(tk.END, f"{distance}m, {elevation}m")
        contact_distance_entry.delete(0, tk.END)
        contact_elevation_entry.delete(0, tk.END)
    except Exception:
        messagebox.showerror("Error", "Start a contact first.")

def save_contact():
    if current_contact is None:
        messagebox.showerror("Error", "No contact to save.")
        return
    contacts.append(current_contact)
    contact_listbox.insert(tk.END, f"Saved: {current_contact.name}")

def create_new_layer():
    try:
        top_idx = int(layer_top_contact_dropdown.get())
        bottom_idx = int(layer_bottom_contact_dropdown.get())
        rock_type = rock_type_var.get()

        if top_idx >= len(contacts) or bottom_idx >= len(contacts):
            messagebox.showerror("Error", "Wrong contact index.")
            return

        new_layer = RockLayer(contacts[top_idx], contacts[bottom_idx], rock_type)
        rock_layers.append(new_layer)
        layers_listbox.insert(tk.END, f"{rock_type}: {contacts[top_idx].name} → {contacts[bottom_idx].name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_csv_file():
    global current_contact
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if not file_path:
        return

    df = pd.read_csv(file_path)

    # Reset current memory
    topography.clear()
    surface_listbox.delete(0, tk.END)
    contacts.clear()
    contact_listbox.delete(0, tk.END)
    contact_points_listbox.delete(0, tk.END)

    contact_dict = {}  # Name -> Contact object

    for idx, row in df.iterrows():
        row_type = row["type"]
        distance = row["distance"]
        elevation = row["elevation"]

        if row_type == "surface":
            topography.add_point(distance, elevation)
            surface_listbox.insert(tk.END, f"{distance}m, {elevation}m")

        elif row_type == "contact":
            name = row["contact_name"]
            if name not in contact_dict:
                contact = Contact(name)
                contact_dict[name] = contact
                contacts.append(contact)
                contact_listbox.insert(tk.END, f"Loaded: {name}")
            contact_dict[name].add_point(distance, elevation)

    messagebox.showinfo("Loaded", "CSV loaded successfully!")
