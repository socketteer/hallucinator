# controls.py
#
# Methods to modularly create control components in a grid with 2 columns
# Written by Kyle McDonell
#
# CS 251
# Spring 2016

import tkinter as tk
from tkinter import ttk, colorchooser


# Creates a label centered on the row
def createLabel(frame, text, row, underline=False, size=10, col=0, columnspan=2):
    label = tk.Label(frame, text=text)
    # label_font = tk.font.Font(label, label.cget("font"))
    # label_font.configure(underline=underline, size=size)
    # label.configure(font=font)
    label.grid(row=row, column=col, columnspan=columnspan, pady=5)
    return label


# Create a title on with the given text on the specified row
def createTitle(frame, text, row):
    return createLabel(frame, text, row, size=14)


# Creates a label centered on the row
def createHeader(frame, text, row):
    return createLabel(frame, text, row, size=11)


# Creates a label on the first column of the frame
def createSideLabel(frame, text, row, col=0):
    return createLabel(frame, text, row, col=col, columnspan=1)


# Create a label which is updated with a variable
def createVariableLabel(frame, variable, row):
    # create a label to display mouse coordinates on the canvas
    label = tk.Label(frame, textvariable=variable)
    label.grid(row=row, columnspan=2, pady=5)
    return label


# Create a button on the specified row with the specified text and function call
def createButton(frame, text, function, row):
    button = tk.Button(frame, text=text, command=function, width=18)
    button.grid(row=row, columnspan=2, pady=3)
    return button


# Create a checkbox on the specified row with the specified text, var, and function call
def createCheckButton(frame, text, variable, function, row):
    check = tk.Checkbutton(frame, text=text, variable=variable, command=function)
    check.grid(row=row, col=0, pady=3)
    return check


# Create a color selection box with the specified label
def createColorPicker(frame, variable, row, col=1, text=None):
    if text is not None:
        createSideLabel(frame, text, row, col=col - 1)
    button = tk.Button(frame, bg=variable.get(), width=2,
                       command=lambda: openColorPicker(button, variable))
    button.grid(row=row, column=col, pady=5)
    return button


# Create a combobox with a text label, specified values, and selected variable
def createComboBox(frame, text, variable, values, row, width=10):
    createSideLabel(frame, text, row)
    combo = ttk.Combobox(frame, textvariable=variable, state='readonly', width=width,
                         values=values)
    combo.grid(row=row, column=1, pady=15)
    return combo


# Create a slider with a text label, value pair defining its range, and selected variable
def createSlider(frame, text, variable, valuePair, row):
    createSideLabel(frame, text, row)
    slider = tk.Scale(frame, from_=valuePair[0], to=valuePair[1],
                      variable=variable, orient=tk.HORIZONTAL, resolution=-1)
    slider.grid(row=row, column=1, pady=3)


# Creates a separator on the given row
def createSeparator(frame, row):
    sep = ttk.Separator(frame, orient=tk.HORIZONTAL)
    sep.grid(row=row, column=1, columnspan=2, sticky='ew')
    return sep


# Creates a menubar on the root given a menu dictionary with the follow format:
# i.e. a list of pairs containing menu headers and a list of (menuitem, command) pairs
# and '-' as a separator
# e.g. [ ('File', [('Item1', 'BindingText', 'Binding', Cmd1), '-',
#                  ('Item2', 'BindingText', 'Binding', Cmd2)] ),
#           ('Edit', [ .... ] ) ]
def createMenuBar(root, menuList):
    # Create a new menu bar and add it to root
    menuBar = tk.Menu(root)
    root.config(menu=menuBar)
    # Create each sub menu and fill it with its items
    for menuTitle, menuItems in menuList:
        # Add the menu to the menu bar
        menu = tk.Menu(menuBar)
        menuBar.add_cascade(label=menuTitle, menu=menu)
        for item in menuItems:
            if item == '-':
                menu.add_separator()
            else:
                # justification doesn't work with menus?
                label = item[0] + '     ' + item[1] if item[1] is not None else item[0]
                menu.add_command(label=label,
                                 command=item[3])
                if item[2] is not None:
                    root.bind(item[2], item[3])
    return menuBar


# Open a color picker to allow the user to select a color
def openColorPicker(button, variable):
    chosenColor = colorchooser.askcolor(initialcolor=variable.get())[0]
    if chosenColor is not None:
        variable.set(rgbToString(chosenColor))
        button.configure(bg=variable.get())


# Convert hex string to an RGB tuple
def stringToRGB(s):
    if s[0] == '#':
        s = s[1:]
    assert(len(s) == 6)
    return int(s[:2], 16), int(s[2:4], 16), int(s[4:6], 16)


# Convert an rgb tuple to a hex string
def rgbToString(rgb):
    rgb = [int(c) for c in rgb]
    r, g, b = rgb
    return f'#{r:03}{g:03}{b:03}'


