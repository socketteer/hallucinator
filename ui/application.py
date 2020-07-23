# application.py
#
# GUI Application for Data Visualization
# Written by Kyle McDonell
#
# CS 251
# Spring 2016

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ui.display import DisplayTab




class Application(object):

    # Create the application window
    def __init__(self, width, height):

        # Create the root
        self.root = tk.Tk()
        self.root.geometry("%dx%d+50+30" % (width, height))
        self.root.title("ADAPT - A Data Analysis and Plotting Tool")
        self.root.maxsize(2000, 900)

        # Create the notebook and add a tab to it
        self.displayTabs = []
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.create_tab()

        # Bind Button-1 to tab click so tabs can be closed
        self.notebook.bind('<Button-1>', self.tab_cick)
        self.notebook.bind()

        # Do final root prep
        self.root.lift()
        self.root.update_idletasks()

    # Forward the given command to the current display tab
    def forward_command(self, command):
        if len(self.displayTabs) == 0:
            messagebox.showwarning("Error", "There is no data.")
        else:
            command(self.displayTabs[self.notebook.index("current")])

    # Create a tab
    def create_tab(self, event=None):
        display = DisplayTab(self.notebook, self.root)
        display.frame.pack()
        self.notebook.add(display.frame, text='No Data')
        self.displayTabs.append(display)

    # If the user clicks a close button, get the tab at that position and close it
    def tab_click(self, event):
        if "close" in event.widget.identify(event.x, event.y):
            index = self.notebook.index("@{},{}".format(event.x, event.y))
            self.notebook.forget(index)
            self.displayTabs.pop(index)

    # Handle the user quitting the application
    def quit_app(self, event=None):
        self.root.destroy()

    # Let the application run
    def main(self):
        self.root.mainloop()


# Create the display application and run it
if __name__ == "__main__":
    app = Application(1200, 675)
    app.main()
