import tkinter as tk
from tkinter import *
from pycaw.pycaw import AudioUtilities
import os
import pystray
from PIL import Image
import sys
import darkdetect
#TODO: Update .txt to .json (May not be necessary)
#TODO: Add a service to run a new script in the background using this information. 
image = None
if darkdetect.isDark():
    image = Image.open("icon_dark.png")
else:
    image = Image.open("icon.png")
hotkey_win = None
ctrl_pressed = False
alt_pressed = False
shift_pressed = False
super_pressed = False
current_hotkey = ""
num_modifiers = 0
num_keys = 0
hotkey_text = ""
hotkey_label = None
window = None
hotkey_button = None
list_view_1 = None
list_view_2 = None
def key_pressed(event):
    global ctrl_pressed
    global alt_pressed
    global hotkey_button
    global hotkey_label
    global shift_pressed
    global super_pressed
    global hotkey_text
    global num_modifiers
    global num_keys
    if event.keysym == "Control_L" or event.keysym == "Control_R":
        if not "Ctrl" in hotkey_text and not num_modifiers == 2:
            ctrl_pressed = True
            num_modifiers += 1
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Ctrl"
            else:
                hotkey_text = hotkey_text + "Ctrl"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Alt_L" or event.keysym == "Alt_R":
        if not "Alt" in hotkey_text and not num_modifiers == 2:
            num_modifiers += 1
            alt_pressed = True
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Alt"
            else:
                hotkey_text = hotkey_text + "Alt"
            hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
        if not "Shift" in hotkey_text and not num_modifiers == 2:
            shift_pressed = True
            num_modifiers += 1
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Shift"
            else:
                hotkey_text = hotkey_text + "Shift"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    elif event.keysym == "Win_L":
        if not "Super" in hotkey_text and not num_modifiers == 2:
            super_pressed = True
            num_modifiers += 1
            if hotkey_text != "":
                hotkey_text = hotkey_text + " + " + "Super"
            else:
                hotkey_text = hotkey_text + "Super"
        hotkey_label.config(text="Current Hotkey: " + hotkey_text)
    else:
        if event.keysym == "Return":
            with open("hotkey.txt", "w") as file:
                file.write(hotkey_text)
            hotkey_win.withdraw()
            hotkey_button.config(text=hotkey_text)
        elif event.keysym == "BackSpace":
            if num_keys + num_modifiers == 1:
                hotkey_text = ""
                hotkey_label.config(text="Current Hotkey: " + hotkey_text)
            else:
                hotkey_text = hotkey_text.rsplit(" + ", 1)[0]
                hotkey_label.config(text="Current Hotkey: " + hotkey_text)
            if num_keys > 0:
                num_keys -= 1
            else:
                num_modifiers -= 1
        elif not event.keysym in hotkey_text and not num_keys == 1 and not event.keysym == "Delete" and not event.keysym == "Escape":
            num_keys += 1
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
    global num_modifiers
    global num_keys
    global current_hotkey
    global hotkey_label
    if event.keysym == "Escape" or event.keysym == "Delete":
        hotkey_text = ""
        hotkey_label.config(text="Current Hotkey: " + current_hotkey)
        alt_pressed = False
        ctrl_pressed = False
        shift_pressed = False
        super_pressed = False
        num_modifiers = 0
        num_keys = 0

def get_audio_devices():
    devices = AudioUtilities.GetAllDevices()

    return devices

def open_hotkey_window():
    global hotkey_win
    try:
        hotkey_win.deiconify()
    except tk.TclError:
        hotkey_win = create_hotkey_window() 

def create_hotkey_window():
    global list_view_1
    global window
    global hotkey_win
    global hotkey_label
    global current_hotkey
    hotkey_win = tk.Toplevel(window)
    hotkey_win.title("Set Hotkey")
    hotkey_win.geometry("225x100")
    hotkey_win.bind("<Key>", key_pressed)
    hotkey_win.bind("<KeyRelease>", key_released)

    hotkey_label = tk.Label(hotkey_win, text="Current Hotkey: " + current_hotkey)
    hotkey_label.pack()

    line = tk.Frame(hotkey_win, height=1, bg='gray')
    line.pack(fill='x', padx=5, pady=5)

    tip1 = tk.Label(hotkey_win, text="Press Backspace to delete the last key")
    tip2 = tk.Label(hotkey_win, text="Press Escape/Delete to clear the hotkey")
    tip3 = tk.Label(hotkey_win, text="Press Enter to set the hotkey")
    tip1.pack()
    tip2.pack()
    tip3.pack()

    window.update_idletasks()
    x = (hotkey_win.winfo_screenwidth() - hotkey_win.winfo_reqwidth()) / 2
    y = (hotkey_win.winfo_screenheight() - hotkey_win.winfo_reqheight()) / 2
    hotkey_win.geometry("+%d+%d" % (x, y))

    return hotkey_win

def add_item():
    global list_view_1
    global list_view_2
    selected = list_view_1.curselection()
    if selected:
        nSelected = list_view_1.get(selected)
        list_view_2.insert(tk.END, nSelected) # insert the selected item into the second list
        list_view_1.delete(selected)
        with open("current_devices.txt", "a") as file:
            if (os.path.getsize("current_devices.txt") > 0):
                file.write(f'\n{nSelected}')
            else:
                file.write(f'{nSelected}')

def remove_item():
    global list_view_1
    global list_view_2
    total_lines = 0
    current_position = 0
    with open("current_devices.txt", "r") as file:
        for line in file:
            total_lines += 1
    selected = list_view_2.curselection()
    if selected:
        list_view_1.insert(tk.END, list_view_2.get(selected)) # insert the selected item into the second list
        list_view_2.delete(selected)
        with open("current_devices.txt", "w") as file:
            for device in list_view_2.get(0, tk.END):
                if not current_position == total_lines - 1:
                    file.write(f'{device}\n')
                else:
                    file.write(f'{device}')
def create_preferences_window():
    # Create the main window
    global window
    global list_view_1
    global list_view_2
    global hotkey_button
    global hotkey_win
    global hotkey_label
    global current_hotkey
    window = tk.Tk()
    window.title("WinAudioSwitcher")
    window.geometry("1000x400")

    devices = get_audio_devices()
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
        with open("current_devices.txt", "r") as file:
            for line in file.readlines():
                list_2_devices.append(line)

    for device in list_2_devices:
        list_view_2.insert(tk.END, device)
    list_view_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    list_view_1_items = list(list_view_1.get(0, tk.END))

    deletion_count = 0
    for item in list_view_2.get(0, tk.END):
        for item_1 in list_view_1.get(0, tk.END):
            if item.strip() == item_1.strip():
                deletion_count += 1
                list_view_1.delete(list_view_1_items.index(item_1))

    window.update_idletasks()
    # Create the label for the current hotkey
    hotkey_label_main = tk.Label(window, text="Current Hotkey: ")
    hotkey_label_main.pack()

    # Create the button to show the current hotkey
    # Variable name current_hotkey will get the currenthotkey from a file called hotkey.txt in the current directory
    try:
        with open("hotkey.txt", "r") as file:
            current_hotkey = file.read()
    except FileNotFoundError:
        current_hotkey = "Ctrl + F12"
        with open("hotkey.txt", "w") as file:
            file.write(current_hotkey)
    hotkey_button = tk.Button(window, text=current_hotkey, command=open_hotkey_window)
    hotkey_button.pack()

    # Create the button to add an item from the first list to the second list
    add_button = tk.Button(window, text="Add Item", command=add_item)
    add_button.pack()


    remove_button = tk.Button(window, text="Remove Item", command=remove_item)
    remove_button.pack()
    hotkey_win = create_hotkey_window()
    hotkey_win.withdraw()
    # Start the main loop
    window.mainloop()


def after_click(icon, query):
    if str(query) == "Preferences":
        create_preferences_window()
    elif str(query) == "Exit":
        icon.stop()
        sys.exit()

icon = pystray.Icon("WinAudioSwitcher", image, "WinAudioSwitcher",
                    menu=pystray.Menu(
                        pystray.MenuItem("Preferences", create_preferences_window),
                        pystray.MenuItem("Exit", after_click)
                    )
                    )
icon.run()