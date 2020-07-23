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


# Create the close button style using the close image at imgs/close.png
from ui import controls
from ui.display import DisplayTab


def create_style():
    closeImage = tk.PhotoImage("closeImage", file="../imgs/close.gif")
    style = ttk.Style()
    style.element_create("close", "image", "closeImage", border=0, sticky='')
    style.layout("TNotebook", [("TNotebook.client", {"sticky": "nswe"})])
    style.layout("TNotebook.Tab", [("TNotebook.tab",
                   {"sticky": "nswe",
                    "children": [("TNotebook.label", {"side": "left"}),
                                 ("TNotebook.close", {"side": "left"})]
                    }
                 )])

    return closeImage


class Application(object):

    # Create the application window
    def __init__(self, width, height):

        # Create the root
        self.root = tk.Tk()
        self.root.geometry("%dx%d+50+30" % (width, height))
        self.root.title("ADAPT - A Data Analysis and Plotting Tool")
        self.root.maxsize(2000, 900)
        self.close_image = create_style()

        # Create the notebook and add a tab to it
        self.displayTabs = []
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.createTab()

        # Build the menu bar
        self.buildMenus()

        # Bind Button-1 to tab click so tabs can be closed
        self.notebook.bind('<Button-1>', self.tabClick)
        self.notebook.bind()

        # Do final root prep
        self.root.lift()
        self.root.update_idletasks()

    # Build the applications menubar
    def buildMenus(self):
        menuList = [("File",
                     [('New Tab', 'Ctrl+N', '<Control-n>', self.createTab),
                      ('Quit', 'Ctrl+Q', '<Control-q>', self.quitApp)]),
                    ("Data",
                     [('Open Data Set', 'Ctrl+O', '<Control-o>',
                       lambda event=None: self.forwardCommand(DisplayTab.loadData)),
                      ('Save Data Set', 'Ctrl+S', '<Control-s>',
                       lambda event=None: self.forwardCommand(DisplayTab.saveData)),
                      ('Plotting Options', 'Ctrl+P', '<Control-p>',
                       lambda event=None: self.forwardCommand(DisplayTab.
                                                              plottingOptionsDialog)),
                      ('Clear Data', 'Ctrl+C', '<Control-c>',
                       lambda event=None: self.forwardCommand(DisplayTab.clearData))
                      ]),
                    ("Analysis",
                     [('Principle Component Analysis', None, None,
                       lambda event=None: self.forwardCommand(DisplayTab.pcaDialog)),
                      ('Cluster Analysis', None, None,
                       lambda event=None: self.forwardCommand(DisplayTab.clusterDialog)),
                      ('Linear Regression', 'Ctrl+L', '<Control-l>',
                       lambda event=None: self.forwardCommand(DisplayTab.regressionDialog)),
                      ]),
                    ("View",
                     [('Reset view', 'Ctrl+T', '<Control-t>',
                       lambda event=None: self.forwardCommand(DisplayTab.resetView)),
                      ('Align to X-Y plane', 'Ctrl+1', '<Control-Key-1>',
                       lambda event=None: self.forwardCommand(DisplayTab.resetView)),
                      ('Align to X-Z plane', 'Ctrl+2', '<Control-Key-2>',
                       lambda event=None: self.forwardCommand(DisplayTab.gotoXZ)),
                      ('Align to Y-Z plane', 'Ctrl+3', '<Control-Key-3>',
                       lambda event=None: self.forwardCommand(DisplayTab.gotoYZ)),
                      ('Change mouse sensitivity', 'Ctrl+S', '<Control-s>',
                       lambda event=None: self.forwardCommand(DisplayTab.
                                                              mouseSensitivityDialog))
                      ])
                    ]
        controls.create_menubar(self.root, menuList)

    # Forward the given command to the current display tab
    def forwardCommand(self, command):
        if len(self.displayTabs) == 0:
            messagebox.showwarning("Error", "There is no data.")
        else:
            command(self.displayTabs[self.notebook.index("current")])

    # Create a tab
    def createTab(self, event=None):
        display = DisplayTab(self.notebook, self.root)
        display.frame.pack()
        self.notebook.add(display.frame, text='No Data')
        self.displayTabs.append(display)

    # If the user clicks a close button, get the tab at that position and close it
    def tabClick(self, event):
        if "close" in event.widget.identify(event.x, event.y):
            index = self.notebook.index("@{},{}".format(event.x, event.y))
            self.notebook.forget(index)
            self.displayTabs.pop(index)


    # Handle the user quitting the application
    def quitApp(self, event=None):
        self.root.destroy()

    # Let the application run
    def main(self):
        self.root.mainloop()


# Create the display application and run it
if __name__ == "__main__":
    app = Application(1200, 675)
    app.main()
