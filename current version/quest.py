import os
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import json

LOCAL_JSON_DIR = "json"
QUESTS_JSON_PATH = os.path.join(LOCAL_JSON_DIR, "quests.json")

# --- Load JSON ---
def load_quests():
    """Fetch the quests JSON from the local json directory."""
    try:
        with open(QUESTS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure the data is a list of dictionaries
        if isinstance(data, list):
            return [q for q in data if isinstance(q, dict)]
        elif isinstance(data, dict):
            flattened_data = []
            for category, quests in data.items():
                if isinstance(quests, list):
                    flattened_data.extend([q for q in quests if isinstance(q, dict)])
            return flattened_data
        else:
            raise ValueError("Unexpected data format")
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# --- Parse Level Range ---
def parse_level_range(level_range):
    """Parse a level range string (e.g., '1-13') into min and max levels."""
    try:
        if "-" in level_range:
            min_level, max_level = map(int, level_range.split("-"))
            return min_level, max_level
        elif level_range.isdigit():
            return int(level_range), int(level_range)
        else:
            return None, None
    except ValueError:
        return None, None

# --- Search Function ---
def search_quests(qid, qtype, region, level_range, only_repeatable, quest_results, quests_data):
    """Search for quests based on the given criteria."""
    quest_results.config(state=tk.NORMAL)
    quest_results.delete("1.0", tk.END)

    qid = qid.lower().strip()
    qtype = qtype.lower().strip()
    region = region.lower().strip()
    min_level, max_level = parse_level_range(level_range.strip())

    results = []
    for quest in quests_data:
        quest_level = quest.get("lvl", "").strip()
        quest_level = int(quest_level) if quest_level.isdigit() else None

        if (not qid or qid in quest.get("quest_#", "").lower()) and \
           (not qtype or qtype in quest.get("quest_name", "").lower()) and \
           (not region or region == quest.get("giver", "").lower()) and \
           (not level_range or (quest_level is not None and min_level <= quest_level <= max_level)) and \
           (not only_repeatable or quest.get("repeatable", "").lower() == "yes"):
            results.append(quest)

    if results:
        for quest in results:
            quest_results.insert(tk.END, f"Quest ID: {quest['quest_#']}\n")
            for key in ['quest_name', 'lvl', 'giver', 'task', 'chain', 'repeatable', 'reward']:
                value = quest.get(key, 'Unknown')
                quest_results.insert(tk.END, f"  {key}: {value}\n")
            quest_results.insert(tk.END, "\n")
    else:
        quest_results.insert(tk.END, "No matching quests found.")

    quest_results.config(state=tk.DISABLED)

# --- Create Quest Tab ---
def create_quest_tab(parent):
    """Creates the Quest tab in the GUI."""
    tab_quest = ttk.Frame(parent, style="Dark.TFrame")
    parent.add(tab_quest, text="🗺️ Quest")

    # Load quest data
    quests_data = load_quests()

    # Extract unique values for dropdowns
    all_quest_ids = sorted({quest.get("quest_#", "").strip() for quest in quests_data if quest.get("quest_#")})
    all_quest_names = sorted({quest.get("quest_name", "").strip() for quest in quests_data if quest.get("quest_name")})
    all_quest_givers = sorted({quest.get("giver", "").strip() for quest in quests_data if quest.get("giver")})

    # Apply styling
    style = ttk.Style()
    style.configure("Dark.TFrame", background="#000000")
    style.configure("Dark.TLabel", background="#000000", foreground="#00FF00", font=("Lucida Console", 11))
    style.configure("Dark.TButton", background="#00FF00", foreground="#000000", font=("Lucida Console", 10))

    # Create form frame
    form = tk.Frame(tab_quest, bg="#000000")
    form.pack(fill="x", padx=10, pady=5)

    # Quest ID Dropdown
    tk.Label(form, text="Quest ID:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    qid_var = tk.StringVar()
    ttk.Combobox(form, textvariable=qid_var, values=[""] + all_quest_ids).pack(fill="x", pady=(0, 5))

    # Quest Name Dropdown
    tk.Label(form, text="Quest Name:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    qtype_var = tk.StringVar()
    ttk.Combobox(form, textvariable=qtype_var, values=[""] + all_quest_names).pack(fill="x", pady=(0, 5))

    # Quest Giver Dropdown
    tk.Label(form, text="Giver:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    region_var = tk.StringVar()
    ttk.Combobox(form, textvariable=region_var, values=[""] + all_quest_givers).pack(fill="x", pady=(0, 5))

    # Level Range Input
    tk.Label(form, text="Level Range (e.g., 1-13):", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    level_range_entry = tk.Entry(form, font=("Lucida Console", 12), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
    level_range_entry.pack(fill="x", pady=(0, 5))

    # Checkbox for Repeatable Quests
    only_repeatable_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        form, text="✅ Show Only Repeatable Quests", variable=only_repeatable_var,
        fg="#00FF00", bg="#000000", selectcolor="#000000", font=("Lucida Console", 10)
    ).pack(anchor="w", pady=(5, 10))

    # Button Frame
    button_frame = tk.Frame(form, bg="#000000")
    button_frame.pack(fill="x", pady=(5, 10))

    # Quest Results
    quest_results = scrolledtext.ScrolledText(
        tab_quest, wrap=tk.WORD, font=("Lucida Console", 12), fg="#00FF00", bg="#000000", insertbackground="#00FF00"
    )
    quest_results.pack(fill="both", expand=True, padx=10, pady=5)

    # Search Button
    search_button = tk.Button(
        button_frame, text="🔎 Search", bg="#00FF00", fg="#000000",
        font=("Lucida Console", 10),
        command=lambda: search_quests(
            qid_var.get(), qtype_var.get(), region_var.get(),
            level_range_entry.get(), only_repeatable_var.get(),
            quest_results, quests_data
        )
    )
    search_button.pack(side="left", expand=True, fill="x", padx=5)

    # Clear Button
    clear_button = tk.Button(
        button_frame, text="🧹 Clear", bg="#555555", fg="#00FF00",
        font=("Lucida Console", 10),
        command=lambda: [
            qid_var.set(""),
            qtype_var.set(""),
            region_var.set(""),
            level_range_entry.delete(0, tk.END),
            only_repeatable_var.set(False),
            quest_results.config(state=tk.NORMAL),
            quest_results.delete("1.0", tk.END),
            quest_results.config(state=tk.DISABLED),
        ]
    )
    clear_button.pack(side="left", expand=True, fill="x", padx=5)
