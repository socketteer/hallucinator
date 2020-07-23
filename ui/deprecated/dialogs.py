# coding=utf-8
# dialogs.py
#
# Dialog boxes for display.py
# Written by Kyle McDonell
#
# CS 251
# Spring 2016

import tkinter as tk
from tkinter import ttk, font, filedialog
import csv
from ui import controls
from ui.deprecated import wizards


# Class to create a basic dialog pop-up box.  Designed for extension.
# From http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class Dialog(tk.Toplevel):
    def __init__(self, parent, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.wm_resizable(height=False, width=False)

        if title:
            self.title(title)

        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.initial_focus.focus_set()

        self.wait_window(self)

    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the standard buttons
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    # command hooks
    def validate(self):
        return 1  # override

    def apply(self):
        pass  # override


# Dialog box to select mouse sensitivities for various canvas controls
class MouseSensitivityDialog(Dialog):
    def __init__(self, parent, sensValues):
        self.sensVars = []
        for value in sensValues:
            self.sensVars.append(tk.DoubleVar(value=value))
        Dialog.__init__(self, parent, title="Change Mouse Sensitivity")

    # Creates sliders for each sensitivity slider
    def body(self, master):
        controls.createSlider(master, "Translation:", self.sensVars[0], (0, 100), 1)
        controls.createSlider(master, "Scaling:", self.sensVars[1], (0, 100), 2)
        controls.createSlider(master, "Rotation:", self.sensVars[2], (0, 100), 3)
        controls.create_button(master, "Reset", self.resetVariables, 4)

    # Reset all sliders to 50
    def resetVariables(self):
        for var in self.sensVars:
            var.set(50)

    # Put the slider values into the result field
    def apply(self):
        self.result = []
        for var in self.sensVars:
            self.result.append(var.get())


# Dialog box to select and manage analyses
class AnalysisManagementDialog(Dialog):
    def __init__(self, parent, display, analyses):
        self.listBox = None
        self.display = display
        self.analyses = analyses
        self.buttons = []
        self.appendButton = None
        Dialog.__init__(self, parent, title="Saved Analyses")

    # Create the selection listbox and buttons
    def body(self, master):
        # Build the listbox
        height = min(15, max(4, len(self.analyses)))
        self.listBox = tk.Listbox(master, width=40, height=height)
        for analysis in self.analyses:
            self.listBox.insert(tk.END, analysis['name'])
        self.listBox.grid(row=1, columnspan=4)
        self.listBox.bind('<<ListboxSelect>>', self.updateButtons)

        # Button to display the analysis info
        b = tk.Button(master, text="Info", width=6, command=self.showInfo)
        b.grid(row=2, column=0, padx=4, pady=5)
        self.buttons.append(b)

        # Button to plot an analysis
        b = tk.Button(master, text="Plot", width=6, command=self.plot)
        b.grid(row=2, column=1, padx=4, pady=5)
        self.buttons.append(b)

        # Button to save an analysis
        b = tk.Button(master, text="Export", width=6, command=self.save)
        b.grid(row=2, column=2, padx=4, pady=5)
        self.buttons.append(b)

        # Button to remove an analysis
        b = tk.Button(master, text="Delete", width=6, command=self.delete)
        b.grid(row=2, column=3, padx=4, pady=5)
        self.buttons.append(b)

        # Button to append an analysis to the data set
        b = tk.Button(master, text="Append to Data", width=12, command=self.append)
        b.grid(row=3, column=1, columnspan=2, padx=4, pady=5)
        self.buttons.append(b)
        self.appendButton = b

        self.updateButtons()


    # Disable buttons if nothing is selected
    def updateButtons(self, event=None):
        analysis = self.getSelection()
        if analysis is not None:
            state = tk.NORMAL
        else:
            state = tk.DISABLED
        for button in self.buttons:
            button.config(state=state)

        # Only allow the user to append not already appended analyses
        analysis = self.getSelection()
        if analysis is not None and analysis.get('appended'):
            self.appendButton.config(state=tk.DISABLED)


    # Get the currently selected analysis
    def getSelection(self):
        if len(self.listBox.curselection()) > 0:
            return self.analyses[self.listBox.curselection()[0]]
        else:
            return None


    # Plot the selected analysis
    def plot(self):
        analysis = self.getSelection()
        if analysis is None:
            return

        # Create a new data object which includes the analysis
        # Add a cluster column at the back and other analyses at the front
        if analysis['type'] == 'Cluster':
            dataObj = self.display.rawData.clone()
            dataObj.add_columns(analysis['analysis'].getData().raw_data)
        else:
            dataObj = analysis['analysis'].getData()
            dataObj.add_columns(self.display.rawData.raw_data)

        # Create a wizard to select the plotting options
        wizDict = self.display.plotSettings.copy()
        wizDict['headers'] = dataObj.get_headers()
        frames = [wizards.DimensionSelection(),
                  wizards.NormalizeTogetherSelection(),
                  wizards.ColorSelection()]
        wizards.Wizard(self, frames, options=wizDict,
                       title="Plotting Options")

        # If successful, have the display build the data
        if wizDict['Complete']:
            self.display.plotSettings = wizDict
            self.display.buildData(dataObj)
            # Close this prompt and exit
            self.ok()


    # Create a popup showing the info for the selected analysis
    def showInfo(self):
        analysis = self.getSelection()
        if analysis is not None:
            TableDialog(self, analysis['analysis'].getInfoTable(),
                        title=analysis['type'] + ' Info')


    # Save the currently selected analysis. Note this doesn't include original
    # column means as I didn't see a reason to include them.
    def save(self):
        analysis = self.getSelection()
        if analysis is None:
            return

        file = filedialog.asksaveasfilename(defaultextension='.csv')
        if file:
            with open(file, 'wb') as f:
                writer = csv.writer(f)
                writer.writerows(analysis['analysis'].getInfoTable())

    # Removed the currently selected analysis
    def delete(self):
        if len(self.listBox.curselection()) > 0:
            index = self.listBox.curselection()[0]
            self.listBox.delete(index)
            self.analyses.pop(index)
            self.updateButtons()

    # Append an analysis to the current dataset and note that it has been appended
    def append(self):
        analysis = self.getSelection()
        if analysis is not None and not analysis.get('appended'):
            self.display.rawData.add_columns(analysis['analysis'].getData().raw_data)
            analysis['appended'] = True
            self.updateButtons()

    # If the window is closed successfully, set the result to be the new analysis list
    def apply(self):
        self.result = self.analyses



# Dialog box to select mouse sensitivities for various canvas controls
class TableDialog(Dialog):
    def __init__(self, parent, table, title=None):
        self.table = table
        Dialog.__init__(self, parent, title=title)

    # Creates the treeview in the frame
    def body(self, master):
        frame = TreeViewFrame(master, self.table)
        self.maxsize(width=800, height=600)
        frame.pack()



# Create a Tree frame with scroll bars and sortable columns using the given table
class TreeViewFrame(tk.Frame):

    def __init__(self, master, table):
        tk.Frame.__init__(self, master)
        self.table = table
        self.descending = False
        self.tree = None
        self.build()

    # Build the table to display the component information
    def build(self):

        # Get a copy of the PCA table
        tableHeaders = self.table[0]
        table = self.table[1:]

        # Build a treeView to display it
        self.tree = ttk.Treeview(self, columns=tableHeaders, show='headings')
        self.tree.grid(row=0, column=0, sticky='NSEW')
        # Allow the treeview to resize with the window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Build column headings
        for header in tableHeaders:
            self.tree.heading(header, text=header,
                              command=lambda c=header: self.sortCol(c))
            self.tree.column(header, width=font.Font().measure(header))
        # Add column data
        for col in table:
            self.tree.insert('', 'end', values=col)
            # Make the col fit the maximum length string
            for i, string in enumerate(col):
                width = font.Font().measure(string)
                if self.tree.column(tableHeaders[i], 'width') < width:
                    self.tree.column(tableHeaders[i], width=width)


        # Add scroll bars
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')


    # Allows the user to sort columns
    def sortCol(self, columnHeader):
        # Get the values to sort as a tuple (value, column id)
        toSort = [(self.tree.set(child, columnHeader), child)
                for child in self.tree.get_children('')]
        toSort.sort(reverse=self.descending)
        for index, item in enumerate(toSort):
            self.tree.move(item[1], '', index)

        self.descending = not self.descending
