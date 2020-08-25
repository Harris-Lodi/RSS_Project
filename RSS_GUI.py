# region imports

from tkinter import *
import tkinter as tk 
from tkinter import ttk
# from RSS_Tag_Reader import *
import mysql.connector

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
mydb = mysql.connector.connect(user="admin", password="pass", database="Database", host="localhost", auth_plugin="mysql_native_password")
cursor = mydb.cursor()

sql = "SELECT * FROM Feed_Table"
cursor.execute(sql)
rows = cursor.fetchall()
total = cursor.rowcount
print("Total Data Entries: " + str(total))

frm = tk.Frame(root)
frm.pack(side=tk.LEFT, padx=20)

tv = ttk.Treeview(frm, columns=(1,2,3), show="headings", height="5")
tv.pack()

tv.heading(1, text="title")
tv.heading(2, text="dates")
tv.heading(3, text="id")

for i in rows:
    tv.insert('', 'end', values = i)

# endregion

# region execute

root.mainloop()

# endregion