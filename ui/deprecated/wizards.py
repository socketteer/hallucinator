import tkinter as tk
from tkinter import ttk
import time

# Wizard class which allows complex user input using a sequence of WizardFrames objects
class Wizard(tk.Toplevel):
    # Create wizard with the given frame sequence
    def __init__(self, parent, frameList, options=None, title=None):

        # Initialize popup window
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.wm_resizable(height=False, width=False)
        if title is not None:
            self.title(title)
        self.parent = parent
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.maxsize(width=800, height=600)

        # Allow the frame to resize
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        # Initialize the wizard settings
        self.frameList = frameList
        self.currentIndex = -1
        if options is None:
            self.options = {}
        else:
            self.options = options

        # Build the button bar
        self.buildButtons().grid(row=1, column=0)
        # Build each frame of the wizard and then hide them
        for wizFrame in frameList:
            wizFrame.build(self)
            wizFrame.frame.grid(row=0, column=0, sticky='nsew')
            wizFrame.frame.grid_remove()

        # Start the wizard
        self.nextFrame()

        # Wait for the wizard to complete
        self.wait_window(self)

    # Get the index of the next frame to be shown
    def getNextIndex(self):
        index = self.currentIndex
        while True:
            index += 1
            if index >= len(self.frameList) or self.frameList[index].shouldDisplay():
                return index

    # Get the index of the previous frame to be shown
    def getPrevIndex(self):
        index = self.currentIndex
        while True:
            index -= 1
            if index < 0 or self.frameList[index].shouldDisplay():
                return index

    # Show the next frame in the frameList or close the dialog if there are no more
    def nextFrame(self, event=None):
        # Hide the previous frame
        if self.currentIndex >= 0:
            self.frameList[self.currentIndex].frame.grid_remove()
            self.frameList[self.currentIndex].updateControls()

        # Get the next frame index
        self.currentIndex = self.getNextIndex()

        # If there are no more frames to show, close the wizard and return
        if self.currentIndex >= len(self.frameList):
            self.ok()

        # Otherwise show the next frame and update it
        else:
            self.frameList[self.currentIndex].frame.grid()
            self.frameList[self.currentIndex].updateControls()
            self.updateButtons()

    # Show the previous frame
    def prevFrame(self, event=None):
        # If there are no previous frames, return
        if self.currentIndex < 0:
            return

        # Hide the current frame
        self.frameList[self.currentIndex].frame.grid_remove()
        self.frameList[self.currentIndex].updateControls()
        # Show the previous frame and update it
        self.currentIndex = self.getPrevIndex()
        self.frameList[self.currentIndex].frame.grid()
        self.frameList[self.currentIndex].updateControls()
        self.updateButtons()

    # Update the wizard buttons
    def updateButtons(self, event=None):

        # Disable next if the current selection isn't valid
        if self.frameList[self.currentIndex].validate():
            self.nextButton.configure(state=tk.NORMAL)
        else:
            self.nextButton.configure(state=tk.DISABLED)

        # Change the next button text if the last frame is shown
        if self.getNextIndex() < len(self.frameList):
            self.nextButton.configure(text="Next")
        else:
            self.nextButton.configure(text="Finish")

        # Disable the previous button if there are no previous frames
        if self.getPrevIndex() < 0:
            self.prevButton.configure(state=tk.DISABLED)
        else:
            self.prevButton.configure(state=tk.NORMAL)



    # Create the buttons to navigate the dialog box
    def buildButtons(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="Cancel", width=8, command=self.cancel)
        w.pack(side=tk.RIGHT, padx=5, pady=5)

        self.nextButton = tk.Button(box, text="Next", width=8, command=self.nextFrame,
                                    default=tk.ACTIVE)
        self.nextButton.pack(side=tk.RIGHT, padx=(0, 5), pady=5)

        self.prevButton = tk.Button(box, text="Back", width=8, command=self.prevFrame)
        self.prevButton.pack(side=tk.RIGHT, padx=(10, 0), pady=5)

        self.bind("<Return>", self.nextFrame)
        self.bind("<Escape>", self.cancel)
        self.bind("<BackSpace>", self.prevButton)

        return box

    def cancel(self, event=None):
        self.options['Complete'] = False
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def ok(self, event=None):
        self.options['Complete'] = True
        self.withdraw()
        self.update_idletasks()
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()


# A frame to be used in a wizard above
class WizardFrame():

    # Override.  Build the components on this frame.
    def build(self, wizard):
        pass

    # Override.  Should control selection invariants given the current option dict.
    # Called automatically when the frame is shown.  This should update the wizard with
    # current frame selections
    def updateControls(self):
        pass

    # Override if the frame has certain wizard conditions in which it should be shown
    def shouldDisplay(self):
        return True

    # Whether or not the selection is valid and the wizard may continue
    def validate(self):
        return True



#############################################################################
# Example wizard frames
#############################################################################
#
#
# # Allows the user to select which dimensions they would like to plot with
# class DimensionSelection(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.frameDict = {}
#         self.dims = ['x', 'y', 'z', 'color', 'size']
#
#
#     # Build the frame
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         l = tk.Label(self.frame, text="Choose the dimensions to plot:")
#         l.grid(row=0, column=0, columnspan=2, pady=5)
#
#         for index, dim in enumerate(self.dims):
#             self.buildSelectorWidgets(dim, index+1)
#
#     # Build a checkbox and a combobox for a dimension
#     def buildSelectorWidgets(self, dim, row):
#         headers = self.wizard.options['headers']
#         headCount = len(headers)
#
#         # Use the previous selection as the default value, or if no dimensions we
#         # selected before (the wizard has never been opened), select all
#         defaultSelect = headers[(row - 1) % headCount]
#         if self.wizard.options.get(dim) is not None:
#             defaultBool = 1
#             if self.wizard.options[dim] in headers:
#                 defaultSelect = self.wizard.options[dim]
#         else:
#             defaultBool = 1 if 'dimensions' not in self.wizard.options else 0
#
#
#         v = tk.IntVar(value=defaultBool)
#         c = tk.Checkbutton(self.frame, text=dim.ljust(6), variable=v, width=7,
#                            anchor=tk.W, command=self.updateControls)
#         c.grid(row=row, column=0, pady=5)
#         self.frameDict[dim + 'Bool'] = v
#         self.frameDict[dim + 'Check'] = c
#
#         # Make a selection box for the item
#         s = tk.StringVar(value=defaultSelect)
#         b = ttk.Combobox(self.frame, textvariable=s, state='readonly', width=25,
#                          values=headers)
#         b.grid(row=row, column=1)
#         self.frameDict[dim] = s
#         self.frameDict[dim + 'Box'] = b
#
#     # Disable selections which are not allowed and update the wizard buttons
#     def updateControls(self, event=None):
#         # Prevent x from being disabled
#         self.frameDict['xBool'].set(1)
#         self.frameDict['xCheck'].configure(state=tk.DISABLED)
#
#         # Force y until a histrogram is implemented
#         self.frameDict['yBool'].set(1)
#         self.frameDict['yCheck'].configure(state=tk.DISABLED)
#
#         # Allow Z only if y is also selected
#         zAllowed = self.frameDict['yBool'].get()
#         if not zAllowed:
#             self.frameDict['zCheck'].configure(state=tk.DISABLED)
#             self.frameDict['zBool'].set(0)
#         else:
#             self.frameDict['zCheck'].configure(state=tk.NORMAL)
#
#         # Allow color and size only if all spatial dimensions are selected
#         xtraDimsAllowed = self.frameDict['zBool'].get()
#         if not xtraDimsAllowed:
#             for dim in ['color', 'size']:
#                 self.frameDict[dim + 'Check'].configure(state=tk.DISABLED)
#                 self.frameDict[dim + 'Bool'].set(0)
#         else:
#             for dim in ['color', 'size']:
#                 self.frameDict[dim + 'Check'].configure(state=tk.NORMAL)
#
#         # Update the wizard buttons to reflect these changes
#         selected = []
#         for dim in self.dims:
#             if self.frameDict[dim + 'Bool'].get():
#                 selected.append(dim)
#                 self.wizard.options[dim] = self.frameDict[dim].get()
#             else:
#                 self.wizard.options[dim] = None
#         self.wizard.options['dimensions'] = selected
#         self.wizard.updateButtons()
#
#
# # Allows the user to select a group of spatial axes to be normalized together
# class NormalizeTogetherSelection(WizardFrame):
#
#     def __init__(self):
#         self.frame = None
#         self.wizard = None
#         self.listBox = None
#         self.listBoxItems = []
#
#
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         l = tk.Label(self.frame, text="Select which axes should be normalized together:")
#         l.grid(row=0, pady=5)
#
#         self.listBox = tk.Listbox(self.frame, width=40, height=4, selectmode=tk.MULTIPLE)
#         self.listBox.grid(row=1, padx=25, pady=5)
#         self.listBox.bind('<<ListboxSelect>>', self.updateControls)
#
#     # Add possible dimension selections to the listbox
#     def updateControls(self, *args):
#         # Add selections to the dictionary
#         if len(self.listBoxItems) > 0:
#             selections = [self.listBoxItems[i] for i in self.listBox.curselection()]
#             self.wizard.options['normalizeTogether'] = selections
#
#         # Build the listbox
#         self.listBox.delete(0, tk.END)
#         self.listBoxItems = []
#         selected = self.wizard.options.get('normalizeTogether')
#         for dim in ['x', 'y', 'z']:
#             header = self.wizard.options.get(dim)
#             if header is not None:
#                 self.listBox.insert(tk.END, ' {0} - {1}'.format(dim, header))
#                 self.listBoxItems.append(dim)
#
#                 # If the header was previously selected, reselect it
#                 if selected is not None and dim in selected:
#                     self.listBox.select_set(len(self.listBoxItems) - 1)
#         self.wizard.updateButtons()
#
#
#     # Display only if at least two spatial dims have been selected
#     def shouldDisplay(self):
#         count = 0
#         for dim in ['x', 'y', 'z']:
#             if self.wizard.options[dim] is not None:
#                 count += 1
#         return count > 1
#
# # Allow different color plotting styles to be selected
# class ColorSelection(WizardFrame):
#
#     def __init__(self):
#         self.frame = None
#         self.wizard = None
#         self.frameDict = {}
#         self.types = ['hue', 'gradient', 'discrete']
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         # Add a label for the menu
#         l = tk.Label(self.frame, text="Choose color plot type:")
#         l.grid(row=0, pady=5)
#
#         # Add a selector for plot type:
#         default = self.wizard.options['colorPlot'] if \
#             'colorPlot' in self.wizard.options else self.types[0]
#         s = tk.StringVar(value=default)
#         b = ttk.Combobox(self.frame, textvariable=s, state='readonly', width=8,
#                          values=self.types)
#         b.grid(row=0, column=1, padx=10)
#         b.bind('<<ComboboxSelected>>', self.updateControls)
#         self.frameDict['type'] = s
#
#         # Add a frame for types which require it:
#         f = self.buildGradientSelection()
#         f.grid(row=1, columnspan=2)
#         self.frameDict['gradientFrame'] = f
#
#
#     def buildGradientSelection(self):
#         frame = tk.Frame(self.frame)
#
#         # Get default colors
#         sels = self.wizard.options
#         color1 = sels['gradientColor1'] if 'gradientColor1' in sels else '#FFFFFF'
#         color2 = sels['gradientColor2'] if 'gradientColor2' in sels else '#000000'
#
#         # Create a color selector for the first color
#         s = tk.StringVar(value=color1)
#         controls.createColorPicker(frame, s, 0, 1)
#         self.frameDict['color1'] = s
#         # Create a label between the selectors
#         controls.createLabel(frame, '---▶', 0, col=2, columnspan=1)
#         # Create a color selector for the second color
#         s = tk.StringVar(value=color2)
#         controls.createColorPicker(frame, s, 0, 4)
#         self.frameDict['color2'] = s
#
#         return frame
#
#
#     def updateControls(self, event=None):
#         # Hide and show frames corresponding to plot types
#         for plottype in self.types:
#             if (plottype + 'Frame') in self.frameDict:
#                 if self.frameDict['type'].get() == plottype:
#                     self.frameDict[plottype + 'Frame'].grid()
#                 else:
#                     self.frameDict[plottype + 'Frame'].grid_remove()
#
#         # Add the results to the wizard
#         sels = self.wizard.options
#         sels['colorPlot'] = self.frameDict['type'].get()
#         sels['gradientColor1'] = self.frameDict['color1'].get()
#         sels['gradientColor2'] = self.frameDict['color2'].get()
#         self.wizard.updateButtons()
#
#
#     # Display only if the user has chosen to plot color
#     def shouldDisplay(self):
#         return self.wizard.options['color'] is not None
#
#
#
# # Frame to select regression type
# class RegressionSelection(WizardFrame):
#
#     def __init__(self):
#         self.frame = None
#         self.wizard = None
#         self.selection = None
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         # Add a label for the menu
#         l = tk.Label(self.frame, text="Select Regression Type:")
#         l.grid(row=0, columnspan=2, pady=5)
#
#         # Make a selection variable
#         self.selection = tk.IntVar(value=0)
#         lasttype = self.wizard.options.get('type')
#
#         # Add a radio button for manual linear regression
#         b = ttk.Radiobutton(self.frame, variable=self.selection, value=1,
#                             command=self.updateControls)
#         b.grid(row=1, padx=5, pady=5)
#         if lasttype == 'manual' or lasttype is None:
#             b.invoke()
#
#         l = tk.Label(self.frame, text='Manual Linear Regression')
#         l.grid(row=1, column=1, pady=5)
#
#
#         # Add a radio button for shotgun regression
#         b = ttk.Radiobutton(self.frame, variable=self.selection, value=2,
#                             command=self.updateControls)
#         b.grid(row=2, padx=5, pady=5)
#         if lasttype == 'shotgun':
#             b.invoke()
#
#         l = tk.Label(self.frame, text='Shotgun Regression')
#         l.grid(row=2, column=1, pady=5)
#
#
#
#     def updateControls(self, event=None):
#         # Add the results to the wizard
#         if self.selection.get() == 1:
#             self.wizard.options['type'] = 'manual'
#         elif self.selection.get() == 2:
#             self.wizard.options['type'] = 'shotgun'
#         else:
#             self.wizard.options['type'] = 'unknown'
#
#         self.wizard.updateButtons()
#
# # Frame to select variables for multiple linear regression
# class ManualRegressionSelection(WizardFrame):
#
#     def __init__(self):
#         self.frame = None
#         self.wizard = None
#         self.selections = []
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         # Add a label for the menu
#         l = tk.Label(self.frame, text="Select Variables For Linear Regression:")
#         l.grid(row=0, pady=5)
#
#         rawHeaders = [self.wizard.options[dim] for dim in ['x', 'y', 'z'] \
#                         if self.wizard.options[dim] is not None]
#         headers = [dim + " - " + self.wizard.options[dim] for dim in ['x', 'y', 'z'] \
#                         if self.wizard.options[dim] is not None]
#
#         hWithNone = headers[:] + ['None']
#         headNum = len(headers)
#
#         # Make box to select independent variables
#         defaultSelect = headers[0]
#         if self.wizard.options.get('dependent') is not None:
#             for dim in ['x', 'y', 'z']:
#                 if self.wizard.options[dim] == self.wizard.options['dependent']:
#                     defaultSelect = dim + " - " + self.wizard.options[dim]
#
#         s1 = tk.StringVar(value=defaultSelect)
#         b1 = ttk.Combobox(self.frame, textvariable=s1, state='readonly', width=10,
#                           values=headers)
#         b1.grid(row=1, column=1)
#         b1.bind('<<ComboboxSelected>>', self.updateControls)
#         l1 = tk.Label(self.frame, text='Dependent Variable:')
#         l1.grid(row=1, column=0)
#         self.selections.append(s1)
#
#         # Make box to select independent variable 1
#         indep1 = self.wizard.options.get('independent1')
#         defaultSelect = headers[1%headNum]
#         if indep1 is not None and indep1 in rawHeaders:
#             for dim in ['x', 'y', 'z']:
#                 if self.wizard.options[dim] == indep1:
#                     defaultSelect = dim + " - " + indep1
#
#         s2 = tk.StringVar(value=defaultSelect)
#         b2 = ttk.Combobox(self.frame, textvariable=s2, state='readonly', width=10,
#                           values=headers)
#         b2.grid(row=2, column=1)
#         b2.bind('<<ComboboxSelected>>', self.updateControls)
#         l2 = tk.Label(self.frame, text='Independent Variable:')
#         l2.grid(row=2, column=0)
#         self.selections.append(s2)
#
#         # Make box to select independent variable 2
#         indep2 = self.wizard.options.get('independent2')
#         defaultSelect = 'None'
#         if indep2 is not None and indep2 in rawHeaders:
#             for dim in ['x', 'y', 'z']:
#                 if self.wizard.options[dim] == indep2:
#                     defaultSelect = dim + " - " + indep2
#
#         s3 = tk.StringVar(value=defaultSelect)
#         b3 = ttk.Combobox(self.frame, textvariable=s3, state='readonly', width=10,
#                           values=hWithNone)
#         b3.grid(row=3, column=1)
#         b3.bind('<<ComboboxSelected>>', self.updateControls)
#         l3 = tk.Label(self.frame, text='Independent Variable 2:')
#         l3.grid(row=3, column=0)
#         self.selections.append(s3)
#
#         # Create a label explaining the options
#         l = tk.Label(self.frame, text="Note all selections must be different.")
#         l.grid(row=4, pady=15)
#
#
#     # Update the wizard
#     def updateControls(self, event=None):
#         self.wizard.options['dependent'] = self.selections[0].get().split()[-1]
#         self.wizard.options['independent1'] = self.selections[1].get().split()[-1]
#         self.wizard.options['independent2'] = None if self.selections[2].get() == 'None' \
#             else self.selections[2].get().split()[-1]
#
#         self.wizard.updateButtons()
#
#     def shouldDisplay(self):
#         return self.wizard.options.get('type') == 'manual'
#
#     # Validate only if all three choices are unique
#     def validate(self):
#         choices = [x.get() for x in self.selections]
#         return len(choices) == len(set(choices))
#
# # Options for selecting a shotgun regression
# class ShotgunRegressionSelection(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.dep = None
#         self.listBox = None
#         self.listBoxItems = []
#
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         # Add a label for the menu
#         l = tk.Label(self.frame, text="Select Variables For Shotgun Regression:")
#         l.grid(row=0, pady=5)
#
#         headers = self.wizard.options['headers']
#         # Make box to select dependent variable
#         defaultSelect = headers[0]
#         if self.wizard.options.get('shotgun dependent') is not None \
#                 and self.wizard.options['shotgun dependent' in headers]:
#             defaultSelect = self.wizard.options['shotgun dependent']
#
#         s = tk.StringVar(value=defaultSelect)
#         b = ttk.Combobox(self.frame, textvariable=s, state='readonly', width=10,
#                          values=headers)
#         b.grid(row=1, column=1)
#         b.bind('<<ComboboxSelected>>', self.updateControls)
#         l = tk.Label(self.frame, text='Dependent Variable:')
#         l.grid(row=1, column=0)
#         self.dep = s
#
#         # Create a list box to select indep vars
#         height = min(15, max(4, len(headers)))
#         l = tk.Label(self.frame, text="Independent Variables:")
#         l.grid(row=2, columnspan=2, pady=5)
#         self.listBox = tk.Listbox(self.frame, width=25, height=height,
#                                   selectmode=tk.MULTIPLE)
#         self.listBox.grid(row=3, columnspan=2, padx=25, pady=5)
#         self.listBox.bind('<<ListboxSelect>>', self.updateControls)
#
#         # Build the listbox
#         self.listBox.delete(0, tk.END)
#         self.listBoxItems = []
#         selected = self.wizard.options.get('shotgun independent')
#         for header in self.wizard.options['headers']:
#             self.listBox.insert(tk.END, header)
#             self.listBoxItems.append(header)
#
#             # If the header was previously selected, reselect it
#             if selected is not None and header in selected:
#                 self.listBox.select_set(len(self.listBoxItems) - 1)
#
#         # Create a label explaining the options
#         l = tk.Label(self.frame, text="Note a variable cannot be selected \n" \
#                                       "as independent and dependent.")
#         l.grid(row=4, pady=15)
#
#
#
#     # Update the wizard
#     def updateControls(self, event=None):
#
#         # Add selections to the dictionary
#         self.wizard.options['shotgun dependent'] = self.dep.get()
#         if len(self.listBoxItems) > 0:
#             selections = [self.listBoxItems[i] for i in self.listBox.curselection()]
#             self.wizard.options['shotgun independent'] = selections
#
#         self.wizard.updateButtons()
#
#     # Display if shotgun was selected
#     def shouldDisplay(self):
#         return self.wizard.options.get('type') == 'shotgun'
#
#     # Validate only if dependent is not selected as an independent
#     def validate(self):
#         dep = self.wizard.options.get('shotgun dependent')
#         indep = self.wizard.options.get('shotgun independent')
#         if dep is None or indep is None:
#             return True
#         else:
#             return dep not in indep
#
# # Allows the user to run a PCA on the data set
# class PCAPrompt(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.listBox = None
#         self.listBoxItems = []
#         self.normalize = None
#         self.name = None
#
#     # Build the selection panel
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         l = tk.Label(self.frame, text="Select which columns to use in the analysis:")
#         l.grid(row=0, pady=2, columnspan=4)
#
#         # Build the listbox
#         height = min(15, max(4, len(self.wizard.options['data'].get_headers())))
#         self.listBox = tk.Listbox(self.frame, width=40, height=height,
#                                   selectmode=tk.MULTIPLE)
#         self.listBox.grid(row=1, padx=25, pady=5, columnspan=4)
#         self.listBox.bind('<<ListboxSelect>>', self.updateControls)
#
#         # Build the listbox
#         self.listBox.delete(0, tk.END)
#         self.listBoxItems = []
#         selected = self.wizard.options.get('headers')
#         for header in self.wizard.options['data'].get_headers():
#             self.listBox.insert(tk.END, header)
#             self.listBoxItems.append(header)
#
#             # If the header was previously selected, reselect it
#             if selected is not None and header in selected:
#                 self.listBox.select_set(len(self.listBoxItems) - 1)
#
#         # Build buttons to select all and reset selection
#         b = tk.Button(self.frame, text="Select all", width=12,
#                       command=lambda: (self.listBox.select_set(0, tk.END), self.updateControls()))
#         b.grid(row=2, column=0, columnspan=2, padx=5)
#         b = tk.Button(self.frame, text="Reset", width=12,
#                       command=lambda: (self.listBox.select_clear(0, tk.END), self.updateControls()))
#         b.grid(row=2, column=2, columnspan=2, padx=5)
#
#
#         # Build a box to entry a name
#         l = tk.Label(self.frame, text="Name:")
#         l.grid(row=3, column=0, pady=20, padx=2)
#         self.name = tk.StringVar(value=time.strftime("PCA %m/%d/%y %H:%M:%S"))
#         e = tk.Entry(self.frame, width=25, textvariable=self.name)
#         e.grid(row=3, column=1, columnspan=2, padx=2)
#
#         # Build the checkbox
#         default = self.wizard.options.get('normalize')
#         if default is None:
#             default = 1
#         self.normalize = tk.IntVar(value=default)
#         c = tk.Checkbutton(self.frame, variable=self.normalize, text="Normalize")
#         c.grid(row=3, column=3)
#
#     # Update the wizard
#     def updateControls(self, event=None):
#
#         # Add selections to the dictionary
#         self.wizard.options['normalize'] = self.normalize.get()
#         if len(self.listBoxItems) > 0:
#             selections = [self.listBoxItems[i] for i in self.listBox.curselection()]
#             self.wizard.options['headers'] = selections
#
#         # If the name is empty, use a timestamp
#         if self.name.get().isspace() or len(self.name.get()) == 0:
#             self.wizard.options['name'] = time.strftime("PCA %m/%d/%y %H:%M:%S")
#         else:
#             self.wizard.options['name'] = self.name.get()
#
#         self.wizard.updateButtons()
#
#         # Run the PCA
#         if self.validate():
#             # Get the selected headers
#             headers = [self.listBox.get(i) for i in self.listBox.curselection()]
#             # Build the pcaData object
#             self.wizard.options['PCA'] = analysis.pca(
#                 self.wizard.options['data'], headers, self.normalize.get())
#
#
#     # Some header must be selected
#     def validate(self):
#         return len(self.listBox.curselection()) > 0
#
# # Display a table showing the results of a PCA
# class PCAInfoDisplay(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.pca = None
#         # Tree to display the results
#         self.tree = None
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#         # Allow the frame to resize
#         self.frame.rowconfigure(0, weight=1)
#         self.frame.columnconfigure(0, weight=1)
#
#     # Build the table to display the component information
#     def createTreeView(self):
#         if self.tree is not None:
#             self.tree.grid_remove()
#         self.tree = dialogs.TreeViewFrame(self.frame, self.pca.getInfoTable())
#         self.tree.grid()
#
#
#     # Update the wizard
#     def updateControls(self, event=None):
#         # Build the table if the pca is done and it hasn't been built
#         pca = self.wizard.options.get('PCA')
#         if pca is not None and pca != self.pca:
#             self.pca = pca
#             self.createTreeView()
#         self.wizard.updateButtons()
#
# # Allows the user to select headers for a cluster analysis
# class ClusterHeaderSelection(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.listBox = None
#         self.listBoxItems = []
#
#     # Build the selection panel
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         l = tk.Label(self.frame, text="Select which columns to use in the analysis:")
#         l.grid(row=0, pady=2, columnspan=3)
#
#         # Build the listbox
#         height = min(15, max(4, len(self.wizard.options['data'].get_headers())))
#         self.listBox = tk.Listbox(self.frame, width=40, height=height,
#                                   selectmode=tk.MULTIPLE)
#         self.listBox.grid(row=1, padx=25, pady=5, columnspan=3)
#         self.listBox.bind('<<ListboxSelect>>', self.updateControls)
#
#         # Build the listbox
#         self.listBox.delete(0, tk.END)
#         self.listBoxItems = []
#         selected = self.wizard.options.get('headers')
#         for header in self.wizard.options['data'].get_headers():
#             self.listBox.insert(tk.END, header)
#             self.listBoxItems.append(header)
#
#             # If the header was previously selected, reselect it
#             if selected is not None and header in selected:
#                 self.listBox.select_set(len(self.listBoxItems) - 1)
#
#         # Build buttons to select all and reset selection
#         b = tk.Button(self.frame, text="Select all", width=10,
#                       command=lambda: (self.listBox.select_set(0, tk.END), self.updateControls()))
#         b.grid(row=2, column=0, padx=5)
#         b = tk.Button(self.frame, text="Reset", width=10,
#                       command=lambda: (self.listBox.select_clear(0, tk.END), self.updateControls()))
#         b.grid(row=2, column=1, padx=5)
#
#
#     # Update the wizard
#     def updateControls(self, event=None):
#         # Add selections to the dictionary
#         if len(self.listBoxItems) > 0:
#             selections = [self.listBoxItems[i] for i in self.listBox.curselection()]
#             self.wizard.options['headers'] = selections
#         self.wizard.updateButtons()
#
#
#     # Some header must be selected
#     def validate(self):
#         return len(self.listBox.curselection()) > 0
#
# # Allows the user to select an algorithm and a metric for clustering
# class ClusterAlgorithmSelection(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.normalize = None
#         self.algorithm = None
#         self.metric = None
#         self.slider = None
#         self.name = None
#
#     # Build the selection panel
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#
#         # Algorithm label
#         l = tk.Label(self.frame, text="Select an algorithm:")
#         l.grid(row=0, column=0, pady=5, padx=10)
#
#         # Build the algorithm selection
#         defaultSelect = self.wizard.options.get('algorithm')
#         if defaultSelect is None:
#             defaultSelect = clustering.algorithmNames[0]
#         self.algorithm = tk.StringVar(value=defaultSelect)
#         b = ttk.Combobox(self.frame, textvariable=self.algorithm, state='readonly',
#                          width=25, values=clustering.algorithmNames)
#         b.grid(row=0, column=1, pady=5, padx=10)
#
#
#         # Metric label
#         l = tk.Label(self.frame, text="Select a metric:")
#         l.grid(row=1, pady=5, padx=10)
#
#         # Build the metric selection
#         defaultSelect = self.wizard.options.get('metric')
#         if defaultSelect is None:
#             defaultSelect = metrics.metricNames[0]
#         # Build the algorithm selection
#         self.metric = tk.StringVar(value=defaultSelect)
#         b = ttk.Combobox(self.frame, textvariable=self.metric, state='readonly', width=25,
#                          values=metrics.metricNames)
#         b.grid(row=1, column=1, pady=5, padx=10)
#
#
#         # Cluster number selection
#         l = tk.Label(self.frame, text="Number of clusters:")
#         l.grid(row=2, pady=2)
#         self.slider = tk.Scale(self.frame, orient=tk.HORIZONTAL, resolution=1, from_=2,
#                                to=min(30, self.wizard.options['data'].get_num_rows()))
#         self.slider.grid(row=2, column=1, pady=2, padx=10)
#
#         # Build a box to entry a name
#         l = tk.Label(self.frame, text="Name:")
#         l.grid(row=3, column=0, pady=30, padx=2)
#         self.name = tk.StringVar(value=time.strftime("Cluster %m/%d/%y %H:%M:%S"))
#         e = tk.Entry(self.frame, width=25, textvariable=self.name)
#         e.grid(row=3, column=1, padx=2)
#
#     # Update the wizard
#     def updateControls(self, event=None):
#         # Add selections to the dictionary
#         self.wizard.options['algorithm'] = self.algorithm.get()
#         self.wizard.options['metric'] = self.metric.get()
#
#         # If the name is empty, use a timestamp
#         if self.name.get().isspace() or len(self.name.get()) == 0:
#             self.wizard.options['name'] = time.strftime("Cluster %m/%d/%y %H:%M:%S")
#         else:
#             self.wizard.options['name'] = self.name.get()
#
#         self.wizard.updateButtons()
#
#         # Run the clustering
#         data = self.wizard.options['data']
#         headers = self.wizard.options['headers']
#         algorithm = clustering.algorithms[
#             clustering.algorithmNames.index(self.algorithm.get())]
#         metric = metrics.metrics[metrics.metricNames.index(self.metric.get())]
#
#         codebook, codes, error = algorithm(data, self.slider.get(), headers, metric)
#
#         # Build the clusterAnalysis object
#         self.wizard.options['Cluster'] = analyses.ClusterAnalysis(data, headers, codebook,
#                                                                   codes, error)
#
# # Display a table showing the results of a Cluster analysis
# class ClusterInfoDisplay(WizardFrame):
#
#     def __init__(self):
#         self.wizard = None
#         self.frame = None
#         self.cluster = None
#         # Tree to display the results
#         self.tree = None
#
#     def build(self, wizard):
#         self.wizard = wizard
#         self.frame = tk.Frame(wizard)
#         # Allow the frame to resize
#         self.frame.rowconfigure(0, weight=1)
#         self.frame.columnconfigure(0, weight=1)
#
#     # Build the table to display the component information
#     def createTreeView(self):
#         if self.tree is not None:
#             self.tree.grid_remove()
#         self.tree = dialogs.TreeViewFrame(self.frame, self.cluster.getInfoTable())
#         self.tree.grid()
#
#
#     # Update the wizard
#     def updateControls(self, event=None):
#         # Build the table if the pca is done and it hasn't been built
#         cluster = self.wizard.options.get('Cluster')
#         if cluster is not None and cluster != self.cluster:
#             self.cluster = cluster
#             self.createTreeView()
#         self.wizard.updateButtons()
