import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import requests

QUESTS_JSON_URL = "https://raw.githubusercontent.com/scagnut/autobeast/main/quests.json"

# --- Load JSON ---
def load_quests():
    """Fetch the quests JSON from the GitHub source."""
    try:
        resp = requests.get(QUESTS_JSON_URL)
        resp.raise_for_status()
        data = resp.json()

        # Ensure the data is a list of dictionaries
        if isinstance(data, list):
            return [q for q in data if isinstance(q, dict)]
        elif isinstance(data, dict):
            # Flatten nested categories into a single list
            flattened_data = []
            for category, quests in data.items():
                if isinstance(quests, list):
                    flattened_data.extend([q for q in quests if isinstance(q, dict)])
            return flattened_data
        else:
            raise ValueError("Unexpected data format")
    except Exception as e:
        print(f"Error fetching JSON: {e}")
        return []

# --- Search Function ---
def search_quests(qid, qtype, region, quest_results, quests_data):
    """Search for quests based on the given criteria."""
    quest_results.config(state=tk.NORMAL)
    quest_results.delete("1.0", tk.END)

    qid = qid.lower().strip()
    qtype = qtype.lower().strip()
    region = region.lower().strip()

    results = []
    for quest in quests_data:
        if (not qid or qid in quest.get("quest_#", "").lower()) and \
           (not qtype or qtype in quest.get("quest_name", "").lower()) and \
           (not region or region == quest.get("giver", "").lower()):
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

    style = ttk.Style()
    style.configure("Dark.TFrame", background="#000000")
    style.configure("Dark.TLabel", background="#000000", foreground="#00FF00", font=("Lucida Console", 11))
    style.configure("Dark.TButton", background="#00FF00", foreground="#000000", font=("Lucida Console", 10))

    quests_data = load_quests()

    form = tk.Frame(tab_quest, bg="#000000")
    form.pack(fill="x", padx=10, pady=5)

    tk.Label(form, text="Quest ID:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    qid_entry = tk.Entry(form, font=("Lucida Console", 12), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
    qid_entry.pack(fill="x", pady=(0, 5))

    tk.Label(form, text="Quest Name:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    qtype_entry = tk.Entry(form, font=("Lucida Console", 12), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
    qtype_entry.pack(fill="x", pady=(0, 5))

    tk.Label(form, text="Giver:", font=("Lucida Console", 12), fg="#00FF00", bg="#000000").pack(anchor="w")
    region_var = tk.StringVar()
    region_combo = ttk.Combobox(form, textvariable=region_var, values=[""] + sorted({q["giver"] for q in quests_data}))
    region_combo.pack(fill="x", pady=(0, 5))

    button_frame = tk.Frame(form, bg="#000000")
    button_frame.pack(fill="x", pady=(5, 10))

    quest_results = scrolledtext.ScrolledText(
        tab_quest, wrap=tk.WORD, font=("Lucida Console", 12), fg="#00FF00", bg="#000000", insertbackground="#00FF00"
    )
    quest_results.pack(fill="both", expand=True, padx=10, pady=5)

    search_button = tk.Button(
        button_frame, text="🔎 Search", bg="#00FF00", fg="#000000",
        font=("Lucida Console", 10),
        command=lambda: search_quests(qid_entry.get(), qtype_entry.get(), region_var.get(), quest_results, quests_data)
    )
    search_button.pack(side="left", expand=True, fill="x", padx=5)

    clear_button = tk.Button(
        button_frame, text="🧹 Clear", bg="#555555", fg="#00FF00",
        font=("Lucida Console", 10),
        command=lambda: [
            qid_entry.delete(0, tk.END),
            qtype_entry.delete(0, tk.END),
            region_var.set(""),
            quest_results.config(state=tk.NORMAL),
            quest_results.delete("1.0", tk.END),
            quest_results.config(state=tk.DISABLED),
        ]
    )
    clear_button.pack(side="left", expand=True, fill="x", padx=5)
