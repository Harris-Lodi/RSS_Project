# region imports

from tkinter import *
import tkinter as tk 
from tkinter import ttk
import sqlite3
# from RSS_Tag_Reader import *

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

# database view 

# WHERE type='table'
con = sqlite3.connect('Database.db')
mycur = con.cursor() 
mycur.execute("SELECT indx, title, dates, id FROM Feed_table ORDER BY indx;")
rows = mycur.fetchall()

frm = tk.Frame(root)
frm.pack(padx=5, pady=100)

# style the output graph, style name is "Treeview" as defined in style.configure
style = ttk.Style()
style.configure(".", font=('Helvetica', 8), foreground="white")
style.configure("Treeview", foreground='red')
style.layout("Treeview", [("Treeview.treearea", {'sticky':'nswe'})])
style.configure("Treeview.Heading", foreground='green', font='bold', stretch=tk.YES)

tv = ttk.Treeview(frm, columns=(1,2,3,4), show="headings", height="20", style="Treeview")
tv.pack()

tv.heading(1, text="Index")
tv.column("1", minwidth=0, width=50, stretch=NO)
tv.heading(2, text="Title")
tv.column("2", minwidth=0, width=400, stretch=YES)
tv.heading(3, text="Date")
tv.column("3", minwidth=0, width=200, stretch=YES)
tv.heading(4, text="Link")
tv.column("4", minwidth=0, width=500, stretch=YES)

for i in rows:
    tv.insert('', 'end', values = i)

# endregion

# region execute

root.mainloop()

# endregion