# region imports

from tkinter import *
import tkinter as tk 
from tkinter import ttk
import sqlite3
import pyperclip
from RSS_Tag_Reader import *

# endregion

# region GUI Code

# GUI class to handle all GUI related code
class GUI:

    rowSelection = {}

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

        # make GUI

        self.frm = tk.Frame(self.root)
        self.frm.pack()

        self.tv = ttk.Treeview(self.frm, columns=(1,2,3,4), show="headings", height="20", style="Treeview")

        self.optionListbox = Listbox(self.frm, bg = '#D8D8D8')

        self.spaceFrame = tk.Label(self.frm, text="RSS Entries Viewer", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 0, column = 1, columnspan=5, pady = 10, ipadx = 10)

        self.enterString = Entry(self.frm, width=90)
        self.enterString.grid(row=4, column=2, columnspan=2, pady=5)

        self.clearInput = tk.Button(self.frm, text="Clear Text", command=self.clearTextbox)
        self.clearInput.grid(row=4, column=5, pady = 10)

        self.enterString_label = Label(self.frm, text="Enter RSS URL and Strings:", bg = '#424242', fg = '#FFFFFF')
        self.enterString_label.grid(row=4, column=1, pady=10)

        self.inputURL = tk.Button(self.frm, text="Enter RSS URL", command=self.enterURL)
        self.inputURL.grid(row=5, column=1, pady = 10)

        self.cdbBtn = tk.Button(self.frm, text="Create DB", command=self.createDB)
        self.cdbBtn.grid(row=5, column=2, pady = 10)

        self.copyBtn = tk.Button(self.frm, text="Copy URL", command=self.copy_info)
        self.copyBtn.grid(row=5, column=3, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Show DB", command=self.loadDB)
        self.clearGridBtn.grid(row=5, column=4, pady = 10)

        self.optionsunoBtn = tk.Button(self.frm, text="Choose Key", command=self.optionsUno)
        self.optionsunoBtn.grid(row=6, column=1, pady = 10)

        self.JSONBtn = tk.Button(self.frm, text="Make JSON", command=sorter)
        self.JSONBtn.grid(row=6, column=2, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Clear Grid", command=self.clearGrid)
        self.clearGridBtn.grid(row=6, column=5, pady = 10)



        # run the GUI widget
        self.root.mainloop()

    # function to handle the creation of the database viewer widget
    def loadDB(self):

        # database view

        if not self.enterString.get() == "":

            name = self.enterString.get()

            self.con = sqlite3.connect('Database.db')
            self.mycur = self.con.cursor() 
            self.mycur.execute(f"SELECT indx, title, dates, id FROM {name} ORDER BY indx;")
            self.rows = self.mycur.fetchall()

            # style the output graph, style name is "Treeview" as defined in style.configure
            self.style = ttk.Style()
            self.style.configure(".", font=('Helvetica', 8), foreground="white")
            self.style.configure("Treeview", foreground='red')
            self.style.layout("Treeview", [("Treeview.treearea", {'sticky':'nswe'})])
            self.style.configure("Treeview.Heading", foreground='green', font='bold', stretch=tk.YES)

            self.tv.grid(row=3, column=1, columnspan = 5)

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
        
        self.clearTextbox()

    # function to clear the grid
    def clearGrid(self):

        self.tv.grid_remove()
        self.optionListbox.grid_remove()
        delLists()

    # function to handle options from the URL Feed
    def URLoptions(self):

        self.optionListbox.grid(row=3, column=1, columnspan = 5)
        
        find_url_tags()

        for items in simpletaglist:

            index = 0
            self.optionListbox.insert(index, items)
            index += 1

    # function to update keyindex from user input
    def optionsUno(self):
        
        if not self.enterString.get() == "":
            
            keyforuse = self.enterString.get()
            keyindex = simpletaglist.index(keyforuse)
            self.clearTextbox()
            self.optionListbox.grid_remove()

    # function to handle copying the URL of the entry from table the user wants
    def copy_info(self):

        if self.rowSelection:
            # save link from values to system clipboard
            pyperclip.copy(self.tv.item(self.rowSelection)['values'][3])

    # function to handle database creation from table name entered by user
    def createDB(self):

        if not self.enterString.get() == "":
            
            createDatabase(self.enterString.get())
            self.loadDB()
            self.clearTextbox()     

    # function to handle event that the user enters the RSS URL in textbox
    def enterURL(self):

        if not self.enterString.get() == "":

            intro(self.enterString.get())
            self.clearTextbox()
            self.URLoptions()

    # function to clear the textbox
    def clearTextbox(self):

        self.enterString.delete(0, END)

    # function to read info from selected row from table
    def select_item(self, a):
        
        # rowSelection is set to the row the user left clicks on
        self.rowSelection = self.tv.selection()[0]     

# endregion

# region execute

# execute code via main
if __name__ == '__main__':

    # invoke GUI class
    run = GUI()

# endregion

# region notes and reference

    # test_str_library = self.tv.item(self.tv.selection())# gets all the values of the selected row
    # print('The test_str = ', type(test_str_library), test_str_library, '\n')  # prints a dictionay of the selected row
    # print('item clicked ', item) # variable that represents the row you clicked on
    # print(self.tv.item(item)['values'][0]) # prints the first value of the values (the id value) 
    # item = self.tv.selection()[0] # which row did you click on

# endregion