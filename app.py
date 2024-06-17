import tkinter as tk
from tkinter import *
from pycaw.pycaw import AudioUtilities
import os 

ctrl_pressed = False
alt_pressed = False
shift_pressed = False
super_pressed = False
num_modifiers = 0
hotkey_text = ""

#TODO: Add a way to save the hotkey to a file (low priority)
#TODO: Make it so that it maxes at 3 keys (2 modifiers and 1 key)
#TODO: Change it so that 'esc' clears the current hotkey, and 'enter' saves the hotkey
def key_pressed(event):
    global ctrl_pressed
    global alt_pressed
    global shift_pressed
    global super_pressed
    global hotkey_text
    if event.keysym == "Control_L":
        num_modifiers += 1
        ctrl_pressed = True
        if not "Ctrl" in hotkey_text:
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Ctrl"
            else:
                hotkey_text = hotkey_text + "Ctrl"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Alt_L":
        alt_pressed = True
        if not "Alt" in hotkey_text:
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Alt"
            else:
                hotkey_text = hotkey_text + "Alt"
            hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Shift_L":
        shift_pressed = True
        if not "Shift" in hotkey_text:
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Shift"
            else:
                hotkey_text = hotkey_text + "Shift"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Win_L":
        super_pressed = True
        if not "Super" in hotkey_text:
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Super"
            else:
                hotkey_text = hotkey_text + "Super"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    else:
        if not event.keysym in hotkey_text:
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + event.keysym
            else:
                hotkey_text = hotkey_text + event.keysym
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)

def key_released(event):
    global ctrl_pressed
    global alt_pressed
    global shift_pressed
    global super_pressed
    global hotkey_text
    if event.keysym == "Escape":
        hotkey_text = ""
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
        alt_pressed = False
        ctrl_pressed = False
        shift_pressed = False
        super_pressed = False

def get_audio_devices():
    devices = AudioUtilities.GetAllDevices()

    return devices

def open_hotkey_window():
    if hotkey_win.state() == "withdrawn":
        hotkey_win.deiconify()
    else:
        hotkey_win.withdraw()

def add_item():
    selected = list_view_1.curselection()
    if selected:
        nSelected = list_view_1.get(selected)
        list_view_2.insert(tk.END, nSelected) # insert the selected item into the second list
        list_view_1.delete(selected)
        with open("current_devices.txt", "a") as file:
            file.write(nSelected + "\n")

def remove_item():
    selected = list_view_2.curselection()
    print(selected)
    if selected:
        list_view_1.insert(tk.END, list_view_2.get(selected)) # insert the selected item into the second list
        list_view_2.delete(selected)
        with open("current_devices.txt", "w") as file:
            for device in list_view_2.get(0, tk.END):
                file.write(device + "\n")

# Create the main window
window = tk.Tk()
window.title("WinAudioSwitcher")
window.geometry("400x300")

devices = get_audio_devices()
print(devices)
# Create the list view for the first list
list_view_1 = tk.Listbox(window)
for device in devices:
    if device.FriendlyName not in list_view_1.get(0, tk.END):
        list_view_1.insert(tk.END, device.FriendlyName)
list_view_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the list view for the second list
list_view_2 = tk.Listbox(window)
list_2_devices = []
# I want to read from a file named "current_devices.txt"
# If the file does not exist, create it
# If the file does exist, read the devices from the file and add them to the list
if not os.path.exists("current_devices.txt"):
    pass
else:
    print("File exists")
    with open("current_devices.txt", "r") as file:
        for line in file.readlines():
            list_2_devices.append(line)

for device in list_2_devices:
    list_view_2.insert(tk.END, device)
list_view_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
list_view_1_items = list(list_view_1.get(0, tk.END))

print(list_2_devices)
deletion_count = 0
for item in list_view_2.get(0, tk.END):
    print("Item: " + item)
    for item_1 in list_view_1.get(0, tk.END):
        if item.strip() == item_1.strip():
            deletion_count += 1
            list_view_1.delete(list_view_1_items.index(item_1))
print("Deletion count: " + str(deletion_count))

# Create the label for the current hotkey
hotkey_label = tk.Label(window, text="Current Hotkey: ")
hotkey_label.pack()

# Create the button to show the current hotkey
# Variable name current_hotkey will get the currenthotkey from a file called hotkey.txt in the current directory
current_hotkey = "Ctrl + F12"
hotkey_button = tk.Button(window, text=current_hotkey, command=open_hotkey_window)
hotkey_button.pack()

# Create the button to add an item from the first list to the second list
add_button = tk.Button(window, text="Add Item", command=add_item)
add_button.pack()


remove_button = tk.Button(window, text="Remove Item", command=remove_item)
remove_button.pack()
hotkey_win = Toplevel(window)
hotkey_win.title("Set Hotkey")
hotkey_win.geometry("200x100")
hotkey_win.bind("<Key>", key_pressed)
hotkey_win.bind("<KeyRelease>", key_released)

current_pressed = "Ctrl + F12"
hotkey_label = tk.Label(hotkey_win, text="Current Hotkey: " + current_pressed)
hotkey_label.pack()
window.update_idletasks()
x = (hotkey_win.winfo_screenwidth() - hotkey_win.winfo_reqwidth()) / 2
y = (hotkey_win.winfo_screenheight() - hotkey_win.winfo_reqheight()) / 2
hotkey_win.geometry("+%d+%d" % (x, y))

hotkey_win.withdraw()
# Start the main loop
window.mainloop()