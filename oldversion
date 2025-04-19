import pywinauto
import json
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, Entry, Button
import threading
import requests

# URL of hosted JSON on GitHub (Raw)
JSON_URL = "https://raw.githubusercontent.com/scagnut/autobeast/main/mobs.json"

# Function to load mobs.json from GitHub
def load_mobs():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Convert response to Python dictionary
    except requests.RequestException as e:
        print(f"Error fetching mobs.json: {e}")
        return {}

# Function to refresh mobs.json
def refresh_mobs():
    global mobs_data
    mobs_data = load_mobs()
    update_gui({})
    messagebox.showinfo("Success", "Mobs JSON file refreshed successfully!")

# Find Ember Online window
windows = pywinauto.findwindows.find_windows(title_re="Ember Online - .*")
if windows:
    app = pywinauto.Application().connect(handle=windows[0])
    window = app.window(handle=windows[0])
else:
    print("Ember Online window not found!")
    exit()

# Store previous monsters detected
previous_monsters = set()

# ASCII Art for Autobeast (Fixed)
ascii_art = r"""
 ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||A |||u |||t |||o |||B |||e |||a |||s |||t ||
||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
"""

# Function to scan for monsters dynamically
def scan_monsters():
    global previous_monsters
    while True:
        controls = [ctrl for ctrl in window.children() if "STATIC" in ctrl.class_name() and ctrl.is_visible()]
        monster_names = [ctrl.window_text().strip() for ctrl in controls]

        ui_keywords = ["HP:", "Gold:", "Ready", "Amount:", "Exp:", "Level:", "Hits:", "Mort", "Professions", 
                       "Skills/Spells", "Quests", "FP:", "ST:", "AD:", "Magic:", "Armor:", "STR", "WIS", "CHR", 
                       "END", "INT", "AGI", "Additional Bonuses"]

        filtered_names = {name for name in monster_names if name and not any(keyword in name for keyword in ui_keywords) 
                          and not any(char.isdigit() for char in name)}

        matching_monsters = {name: mobs_data.get(name, {}) for name in filtered_names if name in mobs_data}

        if matching_monsters.keys() != previous_monsters:
            previous_monsters = matching_monsters.keys()
            update_gui(matching_monsters)

        time.sleep(2)

# GUI setup
root = tk.Tk()
root.title("Mort's Autobeast")
root.geometry("600x500")
root.resizable(True, True)  # Resizable window
root.attributes("-topmost", True)  # Always on top
root.configure(bg="#2B2B2B")  # Dark theme background

# Layout setup using grid
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# ASCII Title (Always Visible & Centered)
ascii_frame = tk.Frame(root, bg="#1E1E1E", padx=10, pady=5)
ascii_frame.grid(row=0, column=0, sticky="n")
ascii_label = tk.Label(ascii_frame, text=ascii_art, font=("Courier", 10), fg="white", bg="#1E1E1E", justify="center")
ascii_label.pack()

# Refresh Button
btn_frame = tk.Frame(root, bg="#333333", padx=10, pady=5)
btn_frame.grid(row=0, column=1, sticky="ne")
btn_refresh = tk.Button(btn_frame, text="Refresh JSON", command=refresh_mobs, bg="#444444", fg="white")
btn_refresh.pack()

# Frame for detected monsters
text_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
text_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 12), fg="white", bg="#444444")
text_area.pack(expand=True, fill="both")

# Search Box
search_frame = tk.Frame(root, bg="#333333", padx=10, pady=5)
search_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

search_entry = Entry(search_frame, font=("Courier", 12), fg="black", bg="white")
search_entry.pack(side="left", expand=True, fill="x")

search_button = Button(search_frame, text="Search", command=lambda: search_monster(search_entry.get()), bg="#444444", fg="white")
search_button.pack(side="right")

# Function to update detected monsters dynamically
def update_gui(monster_data):
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)

    if monster_data:
        for monster, info in monster_data.items():
            text_area.insert(tk.END, f"Detected: {monster}\n", "title")

            # Dynamically display ALL available fields
            for key, value in info.items():
                text_area.insert(tk.END, f"  {key}: {value}\n")

            text_area.insert(tk.END, "\n")
    else:
        text_area.insert(tk.END, "No matching monsters detected.\n")

    text_area.config(state=tk.DISABLED)

# Function to search for a monster manually
def search_monster(monster_name):
    monster_name = monster_name.strip()
    if monster_name in mobs_data:
        update_gui({monster_name: mobs_data[monster_name]})
    else:
        messagebox.showwarning("Not Found", f"No data found for '{monster_name}'.")

# Load mobs initially
mobs_data = load_mobs()

# Start scanning in a separate thread
threading.Thread(target=scan_monsters, daemon=True).start()

# Run the GUI loop
root.mainloop()
