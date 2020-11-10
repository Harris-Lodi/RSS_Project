from Json import JsonMaker
import tkinter as tk
from tkinter import messagebox, Listbox, Label, GROOVE, CENTER, Entry, END

js = JsonMaker()

# region variables, https://lukesmith.xyz/rss.xml

entry = ""
name = ""
DatabaseName = ""

# endregion

class Application(tk.Frame):

    def __init__(self, master):

        # master is set to root(tk.TK()) at the bottom
        super().__init__(master)
        self.master = master

        # Widget Title
        master.title('RSS Feed Reader')
        # Width height
        master.geometry("1280x720")
        # change background color of root, color from https://html-color-codes.info/
        master.configure(bg = "#4B088A")
        # set title bar icon
        master.iconbitmap('Icons/RSS_Icon.ico')
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    # region Functions

    # Create GUI
    def create_widgets(self):

        self.frm = tk.Frame(self.master, bg = "#4B088A")
        self.frm.pack()

        self.spaceFrame = tk.Label(self.frm, text="RSS Entries Viewer", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 0, column = 1, columnspan=5, pady = 10, ipadx = 10)

        self.optionListbox = Listbox(self.frm, bg = '#D8D8D8', height=20, width=150, border=0)
        self.optionListbox.grid(row=9, column=0, columnspan=10, rowspan=6, pady=20, padx=20)

        self.enterString = Entry(self.frm, width=90)
        self.enterString.grid(row=4, column=2, columnspan=2, pady=5)

        self.clearInput = tk.Button(self.frm, text="Clear Text")
        self.clearInput.grid(row=4, column=5, pady = 10, padx=10)

        self.enterString_label = Label(self.frm, text="Enter RSS URL and Strings:", bg = '#424242', fg = '#FFFFFF')
        self.enterString_label.grid(row=4, column=1, pady=10, padx=10)

        self.inputURL = tk.Button(self.frm, text="Enter RSS URL", command=self.enterURL)
        self.inputURL.grid(row=5, column=1, pady = 10)

        self.cdbBtn = tk.Button(self.frm, text="Create DB", command=self.CreateDB)
        self.cdbBtn.grid(row=5, column=4, pady = 10)

        self.copyBtn = tk.Button(self.frm, text="Copy URL")
        self.copyBtn.grid(row=5, column=3, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Enter Name", command=self.getName)
        self.clearGridBtn.grid(row=5, column=2, pady = 10)

        self.optionsunoBtn = tk.Button(self.frm, text="From Directory", command=self.findDirectory)
        self.optionsunoBtn.grid(row=6, column=1, pady = 10)

        self.JSONBtn = tk.Button(self.frm, text="Make JSON", command=self.makeJson)
        self.JSONBtn.grid(row=6, column=2, pady = 10)

        self.simpleBtn = tk.Button(self.frm, text="JSON Entries", command=self.makeJsonEntries)
        self.simpleBtn.grid(row=6, column=3, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Clear Grid")
        self.clearGridBtn.grid(row=6, column=4, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="test vars", command=self.testVar)
        self.clearGridBtn.grid(row=6, column=6, pady = 10)

        self.DBNameBtn = tk.Button(self.frm, text="DB Name", command=self.nameDB)
        self.DBNameBtn.grid(row=7, column=1, pady = 10)

        self.EditDBBtn = tk.Button(self.frm, text="Edit DB", command=self.editDBWindow)
        self.EditDBBtn.grid(row=7, column=2, pady = 10)

        self.clearJSONBtn = tk.Button(self.frm, text="Clear JSON", command=self.ClearJSON)
        self.clearJSONBtn.grid(row=7, column=3, pady = 10)

        self.clearCSVBtn = tk.Button(self.frm, text="Clear CSV", command=self.ClearCSV)
        self.clearCSVBtn.grid(row=7, column=4, pady = 10)

    # region button functions

    # function to handle event that the user enters the RSS URL in textbox
    def enterURL(self):

        global entry

        if not self.enterString.get() == "":

            entry = self.enterString.get()
            self.clearTextbox()

    # function to get names from entry box
    def getName(self):

        global name 

        if not self.enterString.get() == "":

            name = self.enterString.get()
            self.clearTextbox()

    # function to clear the textbox
    def clearTextbox(self):

        self.enterString.delete(0, END)

    # function to populate listbox with data from database if availible
    def populate_list(self):
        pass

    # function to take in url and convert it to json
    def makeJson(self):

        js.makeWholeJSON(name, entry)
    
    # function to make json file for each entry in the feed
    def makeJsonEntries(self):

        js.getEntries()
    
    # function to set NewsFeed in Json.py to the main.JSON file located in directory specificed by user input
    def findDirectory(self):

        if not self.enterString.get() == "":

            indexValue = self.enterString.get()
            js.readFromJson(indexValue)
            # print('Find directory activated!')
            self.clearTextbox()

    # function to get Database name from User
    def nameDB(self):

        global DatabaseName

        if not self.enterString.get() == "":

            DatabaseName = self.enterString.get()
            self.clearTextbox()

    # function to create database
    def CreateDB(self):

        if not DatabaseName == "":

            if not self.enterString.get() == "":

                table = str(self.enterString.get())
                js.makeDB(DatabaseName, table)
                js.convertToSQL(DatabaseName, table)
                self.clearTextbox()
            else:
                print("Database creation failed!")
        else:
            print("Database name was null!")

    # function to create edit DB window:
    def editDBWindow(self):

        newWindow = tk.Toplevel(app)
        labelExample = tk.Label(newWindow, text = "New Window")
        buttonExample = tk.Button(newWindow, text = "New Window button")

        labelExample.pack()
        buttonExample.pack()
    
    # function to clear the JSON files from the directory
    def ClearJSON(self):

        js.wipeJSON()
    
    # function to clear the CSV files from the directory
    def ClearCSV(self):

        js.wipeCSV()

    # function to test the values of all variables
    def testVar(self):

        print("URL is: ", entry)
        print("Name is: ",name)
        print("Database Name is: ",DatabaseName)
        js.testVariables()
    
    # endregion

    # endregion

# Driver code
root = tk.Tk()
app = Application(master=root)
app.mainloop()