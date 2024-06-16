import tkinter as tk

def open_hotkey_window():
    # Code to open the hotkey window goes here
    pass

def add_item():
    # Code to add an item from the first list to the second list goes here
    pass

# Create the main window
window = tk.Tk()
window.title("Settings")
window.geometry("400x300")

# Create the list view for the first list
list_view_1 = tk.Listbox(window)
list_view_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the list view for the second list
list_view_2 = tk.Listbox(window)
list_view_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the label for the current hotkey
hotkey_label = tk.Label(window, text="Current Hotkey: ")
hotkey_label.pack()

# Create the button to show the current hotkey
# Variable name current_hotkey will get the currenthotkey from a file called hotkey.txt in the current directory
current_hotkey = "Ctrl + F12"
hotkey_button = tk.Button(window, text="Show Hotkey", command=get_audio_devices)
hotkey_button.pack()

# Create the button to add an item from the first list to the second list
add_button = tk.Button(window, text="Add Item", command=add_item)
add_button.pack()

# Start the main loop
window.mainloop()