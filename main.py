import tkinter as tk
from tkinter import messagebox, Listbox, Label, GROOVE, CENTER, Entry

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

    # Create GUI
    def create_widgets(self):

        self.frm = tk.Frame(self.master, bg = "#4B088A")
        self.frm.pack()

        self.spaceFrame = tk.Label(self.frm, text="RSS Entries Viewer", relief=GROOVE, anchor=CENTER, font = 'Times 12 italic', bg = '#424242', fg = '#FFFFFF')
        self.spaceFrame.grid(row = 0, column = 1, columnspan=5, pady = 10, ipadx = 10)

        self.optionListbox = Listbox(self.frm, bg = '#D8D8D8', height=20, width=150, border=0)
        self.optionListbox.grid(row=8, column=0, columnspan=10, rowspan=6, pady=20, padx=20)

        self.enterString = Entry(self.frm, width=90)
        self.enterString.grid(row=4, column=2, columnspan=2, pady=5)

        self.clearInput = tk.Button(self.frm, text="Clear Text")
        self.clearInput.grid(row=4, column=5, pady = 10, padx=10)

        self.enterString_label = Label(self.frm, text="Enter RSS URL and Strings:", bg = '#424242', fg = '#FFFFFF')
        self.enterString_label.grid(row=4, column=1, pady=10, padx=10)

        self.inputURL = tk.Button(self.frm, text="Enter RSS URL")
        self.inputURL.grid(row=5, column=1, pady = 10)

        self.cdbBtn = tk.Button(self.frm, text="Create DB")
        self.cdbBtn.grid(row=5, column=2, pady = 10)

        self.copyBtn = tk.Button(self.frm, text="Copy URL")
        self.copyBtn.grid(row=5, column=3, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Show DB")
        self.clearGridBtn.grid(row=5, column=4, pady = 10)

        self.optionsunoBtn = tk.Button(self.frm, text="Choose Key")
        self.optionsunoBtn.grid(row=6, column=1, pady = 10)

        self.JSONBtn = tk.Button(self.frm, text="Make JSON")
        self.JSONBtn.grid(row=6, column=2, pady = 10)

        self.simpleBtn = tk.Button(self.frm, text="Simple")
        self.simpleBtn.grid(row=6, column=3, pady = 10)

        self.clearGridBtn = tk.Button(self.frm, text="Clear Grid")
        self.clearGridBtn.grid(row=6, column=4, pady = 10)
    
    # function to populate listbox with data from database if availible
    def populate_list(self):
        pass

# Driver code
root = tk.Tk()
app = Application(master=root)
app.mainloop()