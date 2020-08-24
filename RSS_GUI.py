# region imports

from tkinter import *
import tkinter as tk 
from RSS_Tag_Reader import *

# endregion

# region GUI Code

root = tk.Tk()
# creating fixed geometry of the 
# tkinter window with dimensions 1280x720 
root.geometry('1280x720')
# change background color of root, color from https://html-color-codes.info/
root.configure(bg = "#4B088A")
# set title bar icon
root.iconbitmap('Icons/RSS_Icon.ico')
# change title on top bar
root.title("RSS_Database_Reader!")

# endregion

# region execute

root.mainloop()

# endregion