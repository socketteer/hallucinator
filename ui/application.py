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

from ui import controls
from ui.display import DisplayTab


# Needed for the tab bar style. It looks bad without it.
def create_style():
    close_image = tk.PhotoImage("closeImage", file="static/close.gif")
    style = ttk.Style()
    style.element_create("close", "image", "closeImage", border=0, sticky='')
    style.layout("TNotebook", [("TNotebook.client", {"sticky": "nswe"})])
    style.layout("TNotebook.Tab", [("TNotebook.tab",
                                    {"sticky": "nswe",
                                     "children": [("TNotebook.label", {"side": "left"}),
                                                  ("TNotebook.close", {"side": "left"})]
                                     }
                                    )])
    return close_image


class Application:

    # Create the application window
    def __init__(self, width, height):

        # Create the root
        self.root = tk.Tk()
        self.root.geometry("%dx%d+50+30" % (width, height))
        self.root.title("Hallucinating")
        # self.root.maxsize(2000, 900)
        self.close_image = create_style()

        # Create the notebook and add a tab to it
        self.display_tabs = []
        self.tab_count = 0
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        s = ttk.Style()
        s.configure('TNotebook', tabposition='nw')
        self.create_tab()

        # Bind Button-1 to tab click so tabs can be closed
        self.notebook.bind('<Button-1>', self.tab_click)
        self.notebook.bind()

        # Build the menu bar
        self.build_menus()

        # Do final root prep
        self.root.update_idletasks()
        self.root.attributes('-topmost', True)
        self.root.update()
        self.root.attributes('-topmost', False)

    # Build the applications menubar
    def build_menus(self):
        menu_list = [("File",
                     [('New Tab', 'Ctrl+N', '<Control-n>', self.create_tab),
                      ('Quit', 'Ctrl+Q', '<Control-q>', self.quit_app)]),
                    ]
        controls.create_menubar(self.root, menu_list)

    # Forward the given command to the current display tab
    def forward_command(self, command):
        if len(self.display_tabs) == 0:
            messagebox.showwarning("Error", "There is no data.")
        else:
            command(self.display_tabs[self.notebook.index("current")])

    # Create a tab
    def create_tab(self, event=None):
        display = DisplayTab(self.notebook, self.root)
        display.frame.pack()
        self.tab_count += 1
        self.notebook.add(display.frame, text=f"Tab {self.tab_count}")
        self.display_tabs.append(display)

    # If the user clicks a close button, get the tab at that position and close it
    def tab_click(self, event):
        if "close" in event.widget.identify(event.x, event.y):
            index = self.notebook.index("@{},{}".format(event.x, event.y))
            self.notebook.forget(index)
            self.display_tabs.pop(index)

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
