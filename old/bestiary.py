import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

# --- JSON URL ---
MOBS_JSON_URL = "https://raw.githubusercontent.com/scagnut/autobeast/main/mobs.json"

# --- Load JSON ---
def load_mobs():
    """Fetch the mobs JSON from the GitHub source."""
    try:
        resp = requests.get(MOBS_JSON_URL)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return {}

# --- Open Map in New Window ---
def open_map_window(map_url):
    """Opens a new window to display the map."""
    if not map_url:
        messagebox.showerror("Error", "No map available for this monster.")
        return

    try:
        # Fetch the map image
        resp = requests.get(map_url, timeout=5)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content))

        # Create a new popup window
        map_window = tk.Toplevel()
        map_window.title("Monster Map")
        map_window.geometry("800x800")  # Set size of the popup window
        map_window.configure(bg="#000000")
        map_window.grab_set()  # Make the popup modal

        # Resize the image to fit the window
        img_resized = img.resize((780, 780), Image.Resampling.LANCZOS)
        tkimg = ImageTk.PhotoImage(img_resized)

        # Display the image
        map_label = tk.Label(map_window, image=tkimg, bg="#000000")
        map_label.image = tkimg  # Keep a reference to avoid garbage collection
        map_label.pack(padx=10, pady=10, expand=True, fill="both")

        # Add a Close button
        close_button = tk.Button(
            map_window,
            text="Close",
            command=map_window.destroy,
            bg="#00FF00",
            fg="#000000",
            font=("Lucida Console", 12)
        )
        close_button.pack(pady=10)

    except Exception as e:
        print(f"Error loading map image: {e}")
        messagebox.showerror("Error", "Failed to load the map.")

# --- Search Function ---
def search_monster(name, lvl_range, div, typ, search_results, map_button, exact_var, mobs_data):
    """Search for a monster based on the given criteria."""
    search_results.config(state=tk.NORMAL)
    search_results.delete("1.0", tk.END)
    map_button.pack_forget()  # Hide the map button initially

    name_l = name.strip().lower()

    # Parse level range input
    min_level, max_level = None, None
    if "-" in lvl_range:
        try:
            min_level, max_level = map(int, lvl_range.split("-"))
        except ValueError:
            messagebox.showerror("Invalid Range", "Please enter a valid level range (e.g., 3-18).")
            return
    elif lvl_range.isdigit():
        min_level = max_level = int(lvl_range)

    candidates = {}
    for n, info in mobs_data.items():
        mob_level_raw = info.get("Level", "0")  # Default to "0" if missing
        mob_level = int(mob_level_raw) if isinstance(mob_level_raw, str) and mob_level_raw.isdigit() else 0

        if (not name or name_l in n.lower()) and \
           (min_level is None or (min_level <= mob_level <= max_level)) and \
           (not div or div.strip() == info.get("Divinity", "")) and \
           (not typ or typ.strip() == info.get("Type", "")):
            candidates[n] = info

    if exact_var.get():
        candidates = {n: info for n, info in candidates.items() if n.lower() == name_l}

    if candidates:
        for m, info in candidates.items():
            search_results.insert(tk.END, f"Monster: {m}\n")
            for k, v in info.items():
                if k == "Map":  # Skip displaying the "Map" field in the text area
                    continue
                search_results.insert(tk.END, f"  {k}: {v}\n")
            search_results.insert(tk.END, "\n")

        if len(candidates) == 1:  # Display the map button only if a single mob is found
            only = next(iter(candidates.values()))
            if "Map" in only and only["Map"]:
                map_button.config(command=lambda: open_map_window(only["Map"]))
                map_button.pack(side="left", padx=5)  # Show the map button inline with "Prefer Exact Match"
    else:
        messagebox.showwarning("Not Found", "No matching monsters found.")

    search_results.config(state=tk.DISABLED)

# --- Create Bestiary Tab ---
def create_bestiary_tab(parent):
    """Creates the Bestiary tab in the GUI."""
    tab_bestiary = ttk.Frame(parent)
    parent.add(tab_bestiary, text="📖 Bestiary")

    mobs_data = load_mobs()

    # Extract unique Types and Divinities from mobs_data
    all_divinities = sorted({info.get("Divinity", "").strip() for info in mobs_data.values() if info.get("Divinity")})
    all_types = sorted({info.get("Type", "").strip() for info in mobs_data.values() if info.get("Type")})

    # Create Main Frame
    main_frame = tk.Frame(tab_bestiary, bg="#000000")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Search Form
    form = tk.Frame(main_frame, bg="#000000")
    form.pack(fill="x", pady=(5, 10))

    tk.Label(form, text="Name:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    name_entry = tk.Entry(form, font=("Lucida Console", 12), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
    name_entry.pack(fill="x", pady=(0, 5))

    tk.Label(form, text="Level Range (e.g., 1-10):", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    level_entry = tk.Entry(form, font=("Lucida Console", 12), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
    level_entry.pack(fill="x", pady=(0, 5))

    tk.Label(form, text="Divinity:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    div_var = tk.StringVar()
    ttk.Combobox(form, textvariable=div_var, values=[""] + all_divinities).pack(fill="x", pady=(0, 5))

    tk.Label(form, text="Type:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    type_var = tk.StringVar()
    ttk.Combobox(form, textvariable=type_var, values=[""] + all_types).pack(fill="x", pady=(0, 5))

    # Create a row for "Prefer Exact Match" and "Show Map" inline
    inline_frame = tk.Frame(form, bg="#000000")
    inline_frame.pack(fill="x", pady=(5, 10))

    exact_var = tk.BooleanVar(value=True)
    tk.Checkbutton(inline_frame, text="✅ Prefer Exact Match", variable=exact_var, fg="#00FF00", bg="#000000", selectcolor="#000000", font=("Lucida Console", 10)).pack(side="left", padx=5)

    # Map Button (Initially Hidden)
    map_button = tk.Button(inline_frame, text="Show Map", bg="#00FF00", fg="#000000", font=("Lucida Console", 10))
    map_button.pack(side="left", padx=5)
    map_button.pack_forget()  # Hidden initially

    button_frame = tk.Frame(form, bg="#000000")
    button_frame.pack(fill="x", pady=(5, 10))

    search_results = tk.Text(main_frame, wrap=tk.WORD, font=("Lucida Console", 12), fg="#00FF00", bg="#000000", insertbackground="#00FF00")
    search_results.pack(fill="both", expand=True, padx=10, pady=5)

    search_button = tk.Button(button_frame, text="🔎 Search", bg="#00FF00", fg="#000000", font=("Lucida Console", 10),
                               command=lambda: search_monster(name_entry.get(), level_entry.get(), div_var.get(), type_var.get(),
                                                              search_results, map_button, exact_var, mobs_data))
    search_button.pack(side="left", expand=True, fill="x", padx=5)

    clear_button = tk.Button(button_frame, text="🧹 Clear", bg="#555555", fg="#00FF00", font=("Lucida Console", 10),
                              command=lambda: [name_entry.delete(0, tk.END), level_entry.delete(0, tk.END),
                                               div_var.set(""), type_var.set(""), exact_var.set(True),
                                               search_results.config(state=tk.NORMAL), search_results.delete("1.0", tk.END),
                                               search_results.config(state=tk.DISABLED), map_button.pack_forget()])
    clear_button.pack(side="left", expand=True, fill="x", padx=5)
