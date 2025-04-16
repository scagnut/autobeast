import os
import tkinter as tk
from tkinter import ttk

# Import the refactored modules
from abdetect import create_detect_tab
from bestiary import create_bestiary_tab
from quest import create_quest_tab
from crafting import create_crafting_tab  # Import the crafting tab


def create_gui():
    """Create the unified GUI with tabs for Detect, Bestiary, Quest, and Crafting."""
    root = tk.Tk()
    root.title("Autobeast Unified GUI")
    root.geometry("800x600")
    root.configure(bg="#2B2B2B")
    root.attributes("-topmost", True)  # Always keep the GUI on top of other windows

    # Create a notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Add tabs from each module
    try:
        create_detect_tab(notebook)
    except Exception as e:
        print(f"Error loading Detect tab: {e}")

    try:
        create_bestiary_tab(notebook)
    except Exception as e:
        print(f"Error loading Bestiary tab: {e}")

    try:
        create_quest_tab(notebook)
    except Exception as e:
        print(f"Error loading Quest tab: {e}")

    try:
        create_crafting_tab(notebook)  # Add the crafting tab
    except Exception as e:
        print(f"Error loading Crafting tab: {e}")

    return root


if __name__ == "__main__":
    # Launch the GUI
    root = create_gui()
    root.mainloop()
