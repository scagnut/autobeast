import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load mobs.json
def load_mobs():
    try:
        with open("mobs.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save mobs.json
def save_mobs(mobs_data):
    with open("mobs.json", "w") as file:
        json.dump(mobs_data, file, indent=4)

# Add or Modify a Mob
def add_modify_mob():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Warning", "Mob name cannot be empty.")
        return

    mobs_data[name] = {
        "Level": entry_level.get().strip(),
        "Type": entry_type.get().strip(),
        "Divinity": entry_divinity.get().strip(),
        "Capturable": entry_capturable.get().strip(),
        "Location": entry_location.get().strip(),
        "Loot Drops": entry_loot.get().strip().split(",") if entry_loot.get().strip() else None
    }
    
    save_mobs(mobs_data)
    update_display()
    messagebox.showinfo("Success", f"'{name}' added/updated successfully!")

# Search Functionality
def search_mob():
    query = search_entry.get().strip().lower()
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)

    for mob, info in mobs_data.items():
        if query in mob.lower():
            text_area.insert(tk.END, f"{mob}\n", "title")
            for key, value in info.items():
                text_area.insert(tk.END, f"  {key}: {value}\n")
            text_area.insert(tk.END, "\n")

    text_area.config(state=tk.DISABLED)

# Update display
def update_display():
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)

    for mob, info in mobs_data.items():
        text_area.insert(tk.END, f"{mob}\n", "title")
        for key, value in info.items():
            text_area.insert(tk.END, f"  {key}: {value}\n")
        text_area.insert(tk.END, "\n")

    text_area.config(state=tk.DISABLED)

# Load data
mobs_data = load_mobs()

# GUI Setup
root = tk.Tk()
root.title("Autobeast Editor")
root.geometry("650x550")
root.configure(bg="#2B2B2B")

# ASCII Header (Centered)
ascii_art = """
 ____ ____ _________ ____ ____ ____ ____ ____ ____ 
||A |||B |||       |||E |||d |||i |||t |||o |||r ||
||__|||__|||_______|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|
"""

ascii_label = tk.Label(root, text=ascii_art, font=("Courier", 10), fg="white", bg="#1E1E1E", justify="center")
ascii_label.pack(pady=5)

# Search Frame
search_frame = tk.Frame(root, bg="#333333", padx=10, pady=5)
search_frame.pack(fill="x")

tk.Label(search_frame, text="Search Mob:", fg="white", bg="#333333").pack(side="left", padx=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)
btn_search = tk.Button(search_frame, text="Search", command=search_mob, bg="#444444", fg="white")
btn_search.pack(side="left", padx=5)

# Input Frame
input_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
input_frame.pack(fill="x")

tk.Label(input_frame, text="Name:", fg="white", bg="#333333").grid(row=0, column=0)
entry_name = tk.Entry(input_frame)
entry_name.grid(row=0, column=1)

tk.Label(input_frame, text="Level:", fg="white", bg="#333333").grid(row=1, column=0)
entry_level = tk.Entry(input_frame)
entry_level.grid(row=1, column=1)

tk.Label(input_frame, text="Type:", fg="white", bg="#333333").grid(row=2, column=0)
entry_type = tk.Entry(input_frame)
entry_type.grid(row=2, column=1)

tk.Label(input_frame, text="Divinity:", fg="white", bg="#333333").grid(row=3, column=0)
entry_divinity = tk.Entry(input_frame)
entry_divinity.grid(row=3, column=1)

tk.Label(input_frame, text="Capturable:", fg="white", bg="#333333").grid(row=4, column=0)
entry_capturable = tk.Entry(input_frame)
entry_capturable.grid(row=4, column=1)

tk.Label(input_frame, text="Location:", fg="white", bg="#333333").grid(row=5, column=0)
entry_location = tk.Entry(input_frame)
entry_location.grid(row=5, column=1)

tk.Label(input_frame, text="Loot Drops:", fg="white", bg="#333333").grid(row=6, column=0)
entry_loot = tk.Entry(input_frame)
entry_loot.grid(row=6, column=1)

# Buttons
btn_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
btn_frame.pack(fill="x")

btn_add = tk.Button(btn_frame, text="Add/Modify", command=add_modify_mob, bg="#444444", fg="white")
btn_add.pack(side="left", padx=5)

# Display Frame
text_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
text_frame.pack(expand=True, fill="both")

text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 12), fg="white", bg="#444444")
text_area.pack(expand=True, fill="both")

update_display()

# Run GUI
root.mainloop()
