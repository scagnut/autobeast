import tkinter as tk
from tkinter import ttk
import requests  # For fetching data from online sources

# Global variables to store user selections
selected_files = {
    "alchemy.txt": True,
    "armor.txt": True,
    "weapons.txt": True,
    "jewel.txt": True
}
selected_tiers = {
    "Tier 1": True,
    "Tier 2": True,
    "Tier 3": True,
    "Tier 4": True,
    "Tier 5": True,
    "Tier 6": True
}

# Base URL for online files
BASE_URL = "https://raw.githubusercontent.com/scagnut/Mort-s-Crafting-Calculator/main/"

# Function to parse tiers and recipes from an online text file
def parse_online_file(file_path):
    tiers = {}
    recipes = {}
    try:
        response = requests.get(BASE_URL + file_path)
        response.raise_for_status()
        file_content = response.text
        for line in file_content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty lines or comments
                continue

            # Parse tiers (e.g., "Tier 1 , Level 1, Green , Level 20")
            if "Tier" in line and "," in line and "Level" in line:
                parts = line.split(',')
                if len(parts) == 4:
                    tier_name = parts[0].strip()
                    level = parts[1].strip().replace("Level ", "")
                    color = parts[2].strip()
                    crafting_level = parts[3].strip().replace("Level ", "")

                    tiers[tier_name] = {
                        "level": int(level),
                        "color": color,
                        "crafting_level": int(crafting_level),
                    }

            # Parse recipes
            elif "," in line:
                parts = line.split(',')
                recipe_name = parts[0].strip()
                materials = {}
                for material in parts[1:]:
                    material = material.strip()
                    if '(' in material and ')' in material:
                        item_name, quantity = material.split('(')
                        item_name = item_name.strip()
                        # Skip "Violent Essence" and "Vigor Essence"
                        if item_name in ["Violent Essence", "Vigor Essence"]:
                            continue
                        quantity = int(quantity.replace(')', '').strip())
                        materials[item_name] = quantity
                if materials:  # Only add recipes with valid materials
                    recipes[recipe_name] = materials
    except requests.RequestException as e:
        print(f"Error fetching {file_path}: {e}")
    return tiers, recipes

# Function to parse selected files and tiers
def parse_files(selected_files):
    tiers = {}
    recipes = {}
    for file, include in selected_files.items():
        if include:
            file_tiers, file_recipes = parse_online_file(file)
            tiers.update(file_tiers)
            recipes.update(file_recipes)
    return tiers, recipes

# Function to filter recipes based on selected tiers
def filter_by_tiers(recipes, selected_tiers):
    filtered_recipes = {}
    for recipe_name, materials in recipes.items():
        for tier in selected_tiers:
            if selected_tiers[tier] and tier in recipe_name:
                filtered_recipes[recipe_name] = materials
    return filtered_recipes

# Function to generate crafting report
def crafting_report(tiers, recipes, inventory):
    craftable_items = {}
    for recipe_name, materials in recipes.items():
        max_count = float("inf")
        for item, required_amount in materials.items():
            available_amount = inventory.get(item, 0)
            max_count = min(max_count, available_amount // required_amount)
        if max_count > 0:
            craftable_items[recipe_name] = max_count
    return craftable_items

# Function to parse inventory
def parse_inventory(raw_inventory):
    inventory = {}
    for line in raw_inventory.strip().split('\n'):
        parts = line.split(']')
        if len(parts) > 1:
            item_data = parts[1].strip()
        else:
            item_data = line.strip()
        if '(' in item_data and ')' in item_data:
            item_name, quantity = item_data.split('(')
            item_name = item_name.strip()
            quantity = int(quantity.replace(')', '').strip())
            inventory[item_name] = quantity
    return inventory

# Function to run the crafting calculation
def run_crafting(inventory_text, output_text):
    # Parse inventory from user input
    raw_inventory = inventory_text.get("1.0", tk.END)
    inventory = parse_inventory(raw_inventory)

    # Parse selected files and tiers
    tiers, recipes = parse_files(selected_files)
    filtered_recipes = filter_by_tiers(recipes, selected_tiers)

    # Generate crafting report
    report = crafting_report(tiers, filtered_recipes, inventory)

    # Display report in the output text widget
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    if report:
        for recipe, count in report.items():
            output_text.insert(tk.END, f"{recipe}: Can craft {count}\n")
    else:
        output_text.insert(tk.END, "No craftable items found.\n")
    output_text.config(state=tk.DISABLED)

# Function to toggle file selection
def toggle_file_selection(file):
    selected_files[file] = not selected_files[file]

# Function to toggle tier selection
def toggle_tier_selection(tier):
    selected_tiers[tier] = not selected_tiers[tier]

# Create the Crafting Tab
def create_crafting_tab(parent):
    """Creates the Crafting tab in the GUI."""
    tab_crafting = ttk.Frame(parent, style="Dark.TFrame")
    parent.add(tab_crafting, text="🛠️ Crafting")

    # Apply black and green theme with Lucida Console font
    style = ttk.Style()
    style.configure("Dark.TFrame", background="#000000")
    style.configure("Dark.TLabel", background="#000000", foreground="#00FF00", font=("Lucida Console", 11))
    style.configure("Dark.TButton", background="#00FF00", foreground="#000000", font=("Lucida Console", 10))
    style.configure("Dark.TCheckbutton", background="#000000", foreground="#00FF00", font=("Lucida Console", 10))

    # Top Section: Options and Run Button
    top_frame = ttk.Frame(tab_crafting, style="Dark.TFrame")
    top_frame.pack(padx=10, pady=10, fill="x")

    # File Selection Checkboxes
    file_frame = ttk.LabelFrame(top_frame, text="Select Files", style="Dark.TLabel")
    file_frame.grid(row=0, column=0, padx=5, sticky="nsew")
    for file in selected_files:
        var = tk.BooleanVar(value=selected_files[file])
        cb = ttk.Checkbutton(file_frame, text=file, variable=var, style="Dark.TCheckbutton",
                             command=lambda f=file: toggle_file_selection(f))
        cb.pack(anchor="w")

    # Tier Selection Checkboxes
    tier_frame = ttk.LabelFrame(top_frame, text="Select Tiers", style="Dark.TLabel")
    tier_frame.grid(row=0, column=1, padx=5, sticky="nsew")
    for tier in selected_tiers:
        var = tk.BooleanVar(value=selected_tiers[tier])
        cb = ttk.Checkbutton(tier_frame, text=tier, variable=var, style="Dark.TCheckbutton",
                             command=lambda t=tier: toggle_tier_selection(t))
        cb.pack(anchor="w")

    # Run Button
    run_button = ttk.Button(top_frame, text="Run Crafting Calculation", style="Dark.TButton",
                            command=lambda: run_crafting(inventory_text, output_text))
    run_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # Inventory Input
    inventory_frame = ttk.LabelFrame(tab_crafting, text="Enter Inventory", style="Dark.TLabel")
    inventory_frame.pack(padx=10, pady=10, fill="x")
    inventory_text = tk.Text(inventory_frame, height=10, bg="#000000", fg="#00FF00", font=("Lucida Console", 10),
                             insertbackground="#00FF00")
    inventory_text.pack(fill="x")

    # Crafting Report Output
    output_frame = ttk.LabelFrame(tab_crafting, text="Crafting Report", style="Dark.TLabel")
    output_frame.pack(padx=10, pady=10, fill="x")
    output_text = tk.Text(output_frame, height=10, bg="#000000", fg="#00FF00", font=("Lucida Console", 10),
                          insertbackground="#00FF00")
    output_text.pack(fill="x")
    output_text.config(state=tk.DISABLED)
