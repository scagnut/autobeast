import pywinauto
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import sys
import os
import json

# --- Local JSON Path ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOBS_JSON_PATH = os.path.join(BASE_DIR, "json", "mobs.json")

# --- ASCII Art ---
ASCII_ART = """
 ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||A |||u |||t |||o |||B |||e |||a |||s |||t ||
||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|
"""

# --- Load JSON ---
def load_mobs():
    """Fetch the mobs JSON from the local json directory."""
    try:
        with open(MOBS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading JSON: {e}\nFile expected at:\n{MOBS_JSON_PATH}")
        return {}

mobs_data = load_mobs()

# --- Scan Monsters ---
def scan_monsters(window, update_gui):
    """Scan for monsters and update the GUI."""
    previous_monsters = set()
    while True:
        controls = [ctrl for ctrl in window.children() if "STATIC" in ctrl.class_name() and ctrl.is_visible()]
        time.sleep(0.1)
        excluded_control_ids = [67742]
        excluded_texts = ["Pine Apple"]
        filtered_controls = [
            ctrl
            for ctrl in controls
            if ctrl.control_id() not in excluded_control_ids and ctrl.window_text().strip() not in excluded_texts
        ]
        monster_names = [ctrl.window_text().strip() for ctrl in filtered_controls]
        ui_keywords = [
            "HP:", "Gold:", "Ready", "Amount:", "Exp:", "Level:", "Hits:", "Mort",
            "Professions", "Skills/Spells", "Quests", "FP:", "ST:", "AD:", "Magic:",
            "Armor:", "STR", "WIS", "CHR", "END", "INT", "AGI", "Additional Bonuses"
        ]
        filtered_names = {
            name for name in monster_names if name and not any(keyword in name for keyword in ui_keywords) and not any(ch.isdigit() for ch in name)
        }
        matching_monsters = {name: mobs_data.get(name, {}) for name in filtered_names if name in mobs_data}
        if matching_monsters.keys() != previous_monsters:
            previous_monsters = matching_monsters.keys()
            update_gui(matching_monsters)
        time.sleep(2)

# --- Create Detector Tab ---
def create_detect_tab(parent):
    """Creates the Detect tab in the GUI."""
    tab_detector = ttk.Frame(parent, style="Dark.TFrame")
    parent.add(tab_detector, text="🧪 Detect")
    style = ttk.Style()
    style.configure("Dark.TFrame", background="#000000")
    style.configure("Dark.TLabel", background="#000000", foreground="#00FF00", font=("Lucida Console", 11))
    style.configure("Dark.TButton", background="#00FF00", foreground="#000000", font=("Lucida Console", 10))
    frame = tk.Frame(tab_detector, bg="#000000")
    frame.pack(fill="both", expand=True)
    text_area = scrolledtext.ScrolledText(
        frame, wrap=tk.WORD, font=("Lucida Console", 12), fg="#00FF00", bg="#000000", insertbackground="#00FF00"
    )
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, ASCII_ART)
    text_area.config(state=tk.DISABLED)
    def update_gui(monster_data):
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)
        if monster_data:
            for monster, info in monster_data.items():
                text_area.insert(tk.END, f"Detected: {monster}\n")
                for k, v in info.items():
                    if k == "Map":
                        continue
                    text_area.insert(tk.END, f"  {k}: {v}\n")
                text_area.insert(tk.END, "\n")
        else:
            text_area.insert(tk.END, ASCII_ART)
        text_area.config(state=tk.DISABLED)
    try:
        windows = pywinauto.findwindows.find_windows(title_re="Ember Online - .*")
        if windows:
            app = pywinauto.Application().connect(handle=windows[0])
            window = app.window(handle=windows[0])
            threading.Thread(target=scan_monsters, args=(window, update_gui), daemon=True).start()
        else:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "Ember Online window not found!\n")
            text_area.config(state=tk.DISABLED)
    except Exception as e:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"Error: {e}\n")
        text_area.config(state=tk.DISABLED)

# --- Main Function ---
def main():
    root = tk.Tk()
    root.title("Autobeast Detector")
    root.geometry("800x600")
    root.configure(bg="#2B2B2B")
    root.attributes("-topmost", True)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    create_detect_tab(notebook)
    root.mainloop()

if __name__ == "__main__":
    main()
