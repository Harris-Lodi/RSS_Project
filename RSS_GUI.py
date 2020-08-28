# region imports

from tkinter import *
import tkinter as tk 
from tkinter import ttk
import sqlite3
import pyperclip
# from RSS_Tag_Reader import *

# endregion

# region GUI Code

# GUI class to handle all GUI related code
class GUI:

    # init function to run upon class invoke
    def __init__(self):

        self.root = tk.Tk()
        # creating fixed geometry of the 
        # tkinter window with dimensions 1280x720 
        self.root.geometry('1280x720')
        # change background color of root, color from https://html-color-codes.info/
        self.root.configure(bg = "#4B088A")
        # set title bar icon
        self.root.iconbitmap('Icons/RSS_Icon.ico')
        # change title on top bar
        self.root.title("RSS_Database_Reader!")

        # create the GUI widget 
        self.createWidget()

        # run the GUI widget
        self.root.mainloop()

    # function to create the GUI widget 
    def createWidget(self):

        # database view

        self.con = sqlite3.connect('Database.db')
        self.mycur = self.con.cursor() 
        self.mycur.execute("SELECT indx, title, dates, id FROM Feed_table ORDER BY indx;")
        self.rows = self.mycur.fetchall()

        self.frm = tk.Frame(self.root)
        self.frm.pack(padx=5, pady=100)

        # style the output graph, style name is "Treeview" as defined in style.configure
        self.style = ttk.Style()
        self.style.configure(".", font=('Helvetica', 8), foreground="white")
        self.style.configure("Treeview", foreground='red')
        self.style.layout("Treeview", [("Treeview.treearea", {'sticky':'nswe'})])
        self.style.configure("Treeview.Heading", foreground='green', font='bold', stretch=tk.YES)

        self.tv = ttk.Treeview(self.frm, columns=(1,2,3,4), show="headings", height="20", style="Treeview")
        self.tv.pack()

        self.tv.heading(1, text="Index")
        self.tv.column("1", minwidth=0, width=50, stretch=NO)
        self.tv.heading(2, text="Title")
        self.tv.column("2", minwidth=0, width=400, stretch=YES)
        self.tv.heading(3, text="Date")
        self.tv.column("3", minwidth=0, width=200, stretch=YES)
        self.tv.heading(4, text="Link")
        self.tv.column("4", minwidth=0, width=500, stretch=YES)

        self.tv.bind('<ButtonRelease-1>', self.select_item) 

        for i in self.rows:
            self.tv.insert('', 'end', values = i)
    
    # function to read info from selected row from table, inputs include self and 'a'(event)
    def select_item(self, a):

        test_str_library = self.tv.item(self.tv.selection())# gets all the values of the selected row
        print('The test_str = ', type(test_str_library), test_str_library, '\n')  # prints a dictionay of the selected row
        item = self.tv.selection()[0] # which row did you click on
        print('item clicked ', item) # variable that represents the row you clicked on
        print(self.tv.item(item)['values'][0]) # prints the first value of the values (the id value)

        # save link from values to system clipboard
        pyperclip.copy(self.tv.item(item)['values'][3])
        

# endregion

# region execute

# execute code via main
if __name__ == '__main__':

    # invoke GUI class
    run = GUI()

# endregion