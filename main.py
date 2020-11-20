from Json import *
import tkinter as tk
from tkinter import messagebox, Listbox, Label, GROOVE, CENTER, Entry, END, NO, YES, Text, LEFT, RIGHT, BOTTOM, TOP
from tkinter import ttk
import pyperclip

# test RSS source: https://www.nasdaq.com/feed/rssoutbound?symbol=AMD

# region variables

entry = ""
name = ""
DatabaseName = ""

isSelected = bool()
currentIndex = 0
currentTitle = ""
currentDate = ""
currentLink = ""
cleansummary = ""

# endregion

class Application(tk.Frame):

    
    def __init__(self, master):

        # master is set to root(tk.TK()) at the bottom
        super().__init__(master)
        self.master = master
        self.js = JsonMaker()

        # init variables
        global isSelected
        isSelected = False

        # Widget Title
        master.title('RSS Feed Reader')
        # Width height
        master.geometry("1600x900")
        # change background color of root, color from https://html-color-codes.info/
        master.configure(bg = "#585858")
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

        # Frames

        self.frm = tk.Frame(self.master, bg = "#585858")
        self.frm.pack()

        # GUI elements

        self.spaceFrame = tk.Label(self.frm, text="RSS Entries Viewer", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 0, column = 3, columnspan=9, pady = 5, ipadx = 10)

        self.spaceFrame = tk.Label(self.frm, text="Create Databases!", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 1, column = 12, columnspan=3, pady = 5, ipadx = 10)

        self.spaceFrame = tk.Label(self.frm, text="Delete Files!", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 1, column = 1, columnspan=1, pady = 5, ipadx = 10, padx=40)

        self.optionListbox = Listbox(self.frm, bg = '#D8D8D8', height="25", width=150, border=0)
        self.optionListbox.grid(row=3, column=2, columnspan=10, rowspan=6, pady=5, padx=10)

        self.tv = ttk.Treeview(self.frm, columns=(1,2,3,4), show="headings", height="20", style="Treeview")

        self.SummaryBox = Text(self.frm, height = 10, width = 100) 
        self.SummaryBox.grid(row=10, column=2, columnspan=10, rowspan=6, pady=5, padx=20)

        self.enterString = Entry(self.frm, width=90)
        self.enterString.grid(row=1, column=4, columnspan=6, pady=5)

        self.clearInput = tk.Button(self.frm, text="Clear Text", command=self.clearTextbox)
        self.clearInput.grid(row=2, column=9, pady = 15, padx=10)

        self.enterString_label = Label(self.frm, text="Enter RSS URL and Strings:", bg = '#424242', fg = '#FFFFFF')
        self.enterString_label.grid(row=1, column=3, pady=5, padx=10, ipadx=20)

        self.inputURL = tk.Button(self.frm, text="Enter RSS URL", command=self.enterURL)
        self.inputURL.grid(row=2, column=5, pady = 15)

        self.cdbBtn = tk.Button(self.frm, text="Create DB", command=self.CreateDB)
        self.cdbBtn.grid(row=5, column=12, pady = 5, padx=60)

        self.clearDBBtn = tk.Button(self.frm, text="Clear DB", command=self.ClearDB)
        self.clearDBBtn.grid(row=4, column=1, pady = 5)

        self.clearGridBtn = tk.Button(self.frm, text="Table Name", command=self.getName)
        self.clearGridBtn.grid(row=2, column=3, pady = 15)

        # need to expand the functionality to work with multiple tables in the same DB before using this function in the full build!
        # self.optionsunoBtn = tk.Button(self.frm, text="From Directory", command=self.findDirectory)
        # self.optionsunoBtn.grid(row=8, column=1, pady = 5)

        self.JSONBtn = tk.Button(self.frm, text="Make JSON", command=self.makeJson)
        self.JSONBtn.grid(row=3, column=12, pady = 5)

        self.simpleBtn = tk.Button(self.frm, text="JSON Entries", command=self.makeJsonEntries)
        self.simpleBtn.grid(row=4, column=12, pady = 5)

        self.clearGridBtn = tk.Button(self.frm, text="Clear Grid", command=self.clearGrid)
        self.clearGridBtn.grid(row=7, column=1, pady = 5)

        # delete this button and all it's functions when the project is fully complete, this is for testing only!
        # self.clearGridBtn = tk.Button(self.frm, text="test vars", command=self.testVar)
        # self.clearGridBtn.grid(row=9, column=1, pady = 5)

        self.DBNameBtn = tk.Button(self.frm, text="DB Name", command=self.nameDB)
        self.DBNameBtn.grid(row=2, column=7, pady = 15)

        self.EditDBBtn = tk.Button(self.frm, text="Edit DB", command=self.editDBWindow)
        self.EditDBBtn.grid(row=6, column=12, pady = 5)

        self.clearJSONBtn = tk.Button(self.frm, text="Clear JSON", command=self.ClearJSON)
        self.clearJSONBtn.grid(row=5, column=1, pady = 5)

        self.clearCSVBtn = tk.Button(self.frm, text="Clear CSV", command=self.ClearCSV)
        self.clearCSVBtn.grid(row=6, column=1, pady = 5)

        self.copyLinkBtn = tk.Button(self.frm, text="Copy URL", command=self.copy_info)
        self.copyLinkBtn.grid(row=8, column=12, pady = 5)

        self.ShowDBBtn = tk.Button(self.frm, text="Show DB", command=self.showDB)
        self.ShowDBBtn.grid(row=7, column=12, pady = 5)

        self.removeEntryBtn = tk.Button(self.frm, text="Delete Entry!", command=self.deleteEntry)
        self.removeEntryBtn.grid(row=3, column=1, pady = 5)

        self.spaceFrame = tk.Label(self.frm, text="Instructions:", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 18, column = 3, columnspan=9, pady = 5, ipadx = 10)

        self.spaceFrame = tk.Label(self.frm, text="Enter names for Database, Table, and the URL for RSS Feed using the first three buttons in the top row!", relief=GROOVE, anchor=CENTER, font = 'Times 12', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 19, column = 3, columnspan=9, pady = 2, ipadx = 10)

        self.spaceFrame = tk.Label(self.frm, text="After the names/URL are inserted, Click on the right side, then 'Make JSON', then 'JSON Entries', and then 'Create DB' in order to show the entries in the RSS Feed!", relief=GROOVE, anchor=CENTER, font = 'Times 12', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 20, column = 3, columnspan=9, pady = 2, ipadx = 10)

        self.spaceFrame = tk.Label(self.frm, text="Use 'Find Directory' button to get the main.JSON file from another table name inserted if you want to select another table, the rest of the buttons can be figured out by testing them manually!", relief=GROOVE, anchor=CENTER, font = 'Times 12', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 21, column = 1, columnspan=17, pady = 2, ipadx = 10)

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

        global DatabaseName
        global name
        
        if os.path.isdir('DB_Files/'):
            if not len(os.listdir('DB_Files/')) == 0:
                if not name == "" and not DatabaseName == "":
                    self.showDB()
                else:
                    DatabaseName, name = self.js.getDBandName()
                    print(DatabaseName + " " + name)
                    self.populate_list()
            else:
                pass
        else:
            pass

    # function to take in url and convert it to json
    def makeJson(self):

        self.js.makeWholeJSON(name, entry)
    
    # function to make json file for each entry in the feed
    def makeJsonEntries(self):

        self.js.getEntries()
    
    # function to set NewsFeed in Json.py to the main.JSON file located in directory specificed by user input
    def findDirectory(self):

        if not self.enterString.get() == "":

            indexValue = self.enterString.get()
            self.js.readFromJson(indexValue)
            self.clearTextbox()

    # function to get Database name from User
    def nameDB(self):

        global DatabaseName

        if not self.enterString.get() == "":

            DatabaseName = self.enterString.get()
            self.clearTextbox()
    
    # function to handle copying the URL of the entry from table the user wants
    def copy_info(self):

        if not currentLink == "":
            # save link from values to system clipboard
            pyperclip.copy(currentLink)

    # function to clear the JSON files from the directory
    def ClearJSON(self):

        self.js.wipeJSON()
    
    # function to clear the CSV files from the directory
    def ClearCSV(self):

        self.js.wipeCSV()

        # function to create database
    
    # function to create the database!
    def CreateDB(self):

        if not DatabaseName == "":

            if not name == "":

                table = name
                self.js.makeDB(DatabaseName, table)
                self.js.convertToSQL(DatabaseName, table)
                self.showDB()
                self.clearTextbox()
            else:
                print("Database creation failed!")
        else:
            print("Database name was null!")

    # function to clear the DB files from the directory
    def ClearDB(self):

        self.js.wipeDB()
        self.clearGrid()

    # function to clear the grid
    def clearGrid(self):
        
        self.tv.delete(*self.tv.get_children()) # delete saved treeview children
        self.tv.grid_remove()
        self.optionListbox.grid_remove()
        self.SummaryBox.delete("1.0","end")
        self.optionListbox.grid(row=3, column=2, columnspan=10, rowspan=6, pady=5, padx=10)

    # function to display content from db
    def showDB(self):

        rows = []

        self.clearGrid()

        # style the output graph, style name is "Treeview" as defined in style.configure
        self.style = ttk.Style()
        self.style.configure(".", font=('Helvetica', 8), foreground="white")
        self.style.configure("Treeview", foreground='red')
        self.style.layout("Treeview", [("Treeview.treearea", {'sticky':'nswe'})])
        self.style.configure("Treeview.Heading", foreground='green', font='bold', stretch=tk.YES)

        self.tv.grid(row=3, column=2, columnspan=10, rowspan=6, pady=5, padx=10)

        self.tv.heading(1, text="Index")
        self.tv.column("1", minwidth=0, width=50, stretch=NO)
        self.tv.heading(2, text="Title")
        self.tv.column("2", minwidth=0, width=400, stretch=YES)
        self.tv.heading(3, text="Date")
        self.tv.column("3", minwidth=0, width=200, stretch=YES)
        self.tv.heading(4, text="Link")
        self.tv.column("4", minwidth=0, width=500, stretch=YES)

        self.tv.bind('<ButtonRelease-1>', self.select_item)

        rows = self.js.showTable(DatabaseName, name)

        for i in rows:
            self.tv.insert('', 'end', values = i)

        self.clearTextbox()

    # function to select row from list
    def select_item(self, a):
        
        global currentIndex 
        global currentTitle 
        global currentDate 
        global currentLink 
        global cleansummary 
        global isSelected

        isSelected = True
        # print(isSelected)

        # rowSelection is set to the row the user left clicks on
        self.rowSelection = self.tv.selection()[0] 
        cursel = self.tv.item(self.rowSelection)

        currentIndex = 0
        currentIndex = cursel['values'][0]
        # print("The Current Index is: ", currentIndex)

        currentTitle = ""
        currentTitle = cursel['values'][1]
        # print("The Current Title is: ", currentTitle)

        currentDate = ""
        currentDate = cursel['values'][2]
        # print("The Current Date is: ", currentDate)

        currentLink = ""
        currentLink = cursel['values'][3]
        # print("The Current Link is: ", currentLink)

        cleansummary = "" # init the textbox
        self.SummaryBox.delete("1.0","end")
        summary = cursel['values'][4]
        cleansummary = BeautifulSoup(summary, "lxml").text # clean summary text with BS4
        self.SummaryBox.insert(tk.END, cleansummary)
    
    # function to delete an entry
    def deleteEntry(self):

        global isSelected

        if isSelected == True:

            if not DatabaseName == "" and not name == "":

                self.js.deleteDatabaseEntry(DatabaseName, name, currentIndex)
                self.showDB()
            else:
                pass    
        else:
            pass
            print("isSelected was False")
        
        isSelected = False

    # region editDB window functions

    # function to create edit DB window:
    def editDBWindow(self):

        self.newWindow = tk.Toplevel(app)
        # Widget Title
        self.newWindow.title('Modify Database')
        # Width height
        self.newWindow.geometry("800x450")
        # change background color of root, color from https://html-color-codes.info/
        self.newWindow.configure(bg = "#585858")
        # set title bar icon
        self.newWindow.iconbitmap('Icons/RSS_Icon.ico')

        self.wfrm = tk.Frame(self.newWindow, bg = "#585858")
        self.wfrm.pack()

        self.wFrame = tk.Label(self.wfrm, text="Modify Database Entry!", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.wFrame.grid(row = 0, column = 2, columnspan=2, pady = 5, ipadx = 10)

        self.new_title_label = Label(self.wfrm, text="Enter new Title:", bg = '#424242', fg = '#FFFFFF')
        self.new_title_label.grid(row=1, column=1, pady=5, padx=10)

        self.new_title_String = Entry(self.wfrm, width=45)
        self.new_title_String.grid(row=1, column=3, columnspan=1, pady=5)

        self.new_date_label = Label(self.wfrm, text="Enter new Date:", bg = '#424242', fg = '#FFFFFF')
        self.new_date_label.grid(row=2, column=1, pady=5, padx=10)

        self.new_date_String = Entry(self.wfrm, width=45)
        self.new_date_String.grid(row=2, column=3, columnspan=1, pady=5)

        self.new_URL_label = Label(self.wfrm, text="Enter new URL:", bg = '#424242', fg = '#FFFFFF')
        self.new_URL_label.grid(row=3, column=1, pady=5, padx=10)

        self.new_URL_String = Entry(self.wfrm, width=45)
        self.new_URL_String.grid(row=3, column=3, columnspan=1, pady=5)

        self.new_summary_label = Label(self.wfrm, text="Enter new Summary:", bg = '#424242', fg = '#FFFFFF')
        self.new_summary_label.grid(row=4, column=1, pady=5, padx=10)

        self.new_summary_Box = Text(self.wfrm, height = 10, width = 70) 
        self.new_summary_Box.grid(row=5, column=1, columnspan=5, rowspan=6, pady=5, padx=20)

        self.saveChangesBtn = tk.Button(self.wfrm, text="Save Changes!", width=18, command=self.saveChanges)
        self.saveChangesBtn.grid(row=12, column=4, pady = 10)

        self.deleteEntryBtn = tk.Button(self.wfrm, text="Quit!", width=18, command=self.quitWindow)
        self.deleteEntryBtn.grid(row=12, column=1, pady = 10)
    
    # function to save changes to the database
    def saveChanges(self):

        global currentTitle
        global currentDate
        global currentLink
        global cleansummary
        global isSelected

        if isSelected == True:

            currentTitle = self.new_title_String.get()
            currentDate = self.new_date_String.get()
            currentLink = self.new_URL_String.get()
            cleansummary = self.new_summary_Box.get("1.0",END)

            self.new_title_String.delete(0, END)
            self.new_date_String.delete(0, END)
            self.new_URL_String.delete(0, END)
            self.new_summary_Box.delete("1.0","end")

            # print("")
            # print("Database name is ",DatabaseName)
            # print("Table name is ", name)
            # print("Current Index: ",currentIndex)
            # print("new Title: ",currentTitle)
            # print("new Date: ",currentDate)
            # print("new URL: ",currentLink)
            # print("new Summary: ",cleansummary)

            self.js.updateTable(DatabaseName, name, currentIndex, currentTitle, currentDate, currentLink, cleansummary)
            self.showDB()
        else:
            pass
            print("isSelected was False")
        
        isSelected = False

    # function to quit the newwindow
    def quitWindow(self):

        self.newWindow.destroy()

    # endregion

    # function to test the values of all variables
    def testVar(self):

        print("URL is: ", entry)
        print("Name is: ",name)
        print("Database Name is: ",DatabaseName)
        self.js.testVariables()

    # endregion

# execute code via main
if __name__ == '__main__':

    # Driver code
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()