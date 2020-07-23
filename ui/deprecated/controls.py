# controls.py
#
# Methods to modularly create control components in a grid with 2 columns
# Written by Kyle McDonell
#
# CS 251
# Spring 2016

import tkinter as tk
from enum import Enum
from functools import partial
from tkinter import ttk, colorchooser


# Creates a label centered on the row
from ui.util import get_param_info, convert_to_builtin


def createLabel(frame, text, row=None, underline=False, size=12, col=0, columnspan=2, pady=3, padx=8, **kwargs):
    row = frame.grid_size()[1] if row is None else row
    label = tk.Label(frame, text=text)
    label_font = tk.font.Font(label, label.cget("font"))
    label_font.configure(underline=underline, size=size)
    label.configure(font=label_font)
    label.grid(row=row, column=col, columnspan=columnspan, padx=padx, pady=pady, **kwargs)
    return label


# Create a title on with the given text on the specified row
def createTitle(frame, text, row=None):
    return createLabel(frame, text, row, size=14, columnspan=10, pady=3)


# Creates a label centered on the row
def createHeader(frame, text, row=None):
    return createLabel(frame, text, row, size=12, columnspan=10, pady=4, sticky=tk.W)


# Creates a label on the first column of the frame
def createSideLabel(frame, text, row=None, col=0):
    return createLabel(frame, text, row, col=col, columnspan=1)


# Create a label which is updated with a variable
def createVariableLabel(frame, variable, row=None):
    label = tk.Label(frame, textvariable=variable)
    label.grid(row=row, columnspan=2, pady=5)
    return label


# Create a button on the specified row with the specified text and function call
def createButton(frame, text, function, row=None):
    row = frame.grid_size()[1] if row is None else row
    button = tk.Button(frame, text=text, command=function, width=18)
    button.grid(row=row, columnspan=2, pady=3)
    return button


# # Create a checkbox on the specified row with the specified text, var, and function call
# def createCheckButton(frame, text, variable, row, function=None):
#     check = tk.Checkbutton(frame, text=text, variable=variable, function=function)
#     check.grid(row=row, column=0, pady=3)
#     return check
#
#
# # Create a color selection box with the specified label
# def createColorPicker(frame, variable, row, col=1, text=None):
#     if text is not None:
#         createSideLabel(frame, text, row, col=col - 1)
#     button = tk.Button(frame, bg=variable.get(), width=2,
#                        command=lambda: openColorPicker(button, variable))
#     button.grid(row=row, column=col, pady=5)
#     return button
#
#
# # Create a combobox with a text label, specified values, and selected variable
# def createComboBox(frame, text, variable, values, row, width=10):
#     createSideLabel(frame, text, row)
#     combo = ttk.Combobox(frame, textvariable=variable, state='readonly', width=width,
#                          values=values)
#     combo.grid(row=row, column=1, pady=2)
#     return combo
#
#
# # Create a slider with a text label, value pair defining its range, and selected variable
# def createSlider(frame, text, variable, valuePair, row):
#     createSideLabel(frame, text, row)
#     slider = tk.Scale(frame, from_=valuePair[0], to=valuePair[1],
#                       variable=variable, orient=tk.HORIZONTAL, resolution=-1)
#     slider.grid(row=row, column=1, pady=3)
#     return slider
#
#
# def createSpinBox(frame, text, row, command, valuePair=None, values=None):
#     assert valuePair is not None != values is not None
#     createSideLabel(frame, text, row)
#     if valuePair:
#         spin = ttk.Spinbox(frame, from_=valuePair[0], to=valuePair[1], command=command)
#     elif values:
#         spin = ttk.Spinbox(frame, values=values, command=command)
#     spin.grid(row=row, column=1, pady=5)
#     return spin
#
#
# def createEntry(frame, label_text, text_variable, row, col=1, width=8, create_label=True):
#     if create_label:
#         createSideLabel(frame, label_text, row)
#     entry = ttk.Entry(frame, textvariable=text_variable, width=width)
#     entry.grid(row=row, column=col, pady=2, padx=5)
#     return entry


# Creates a separator on the given row
def createSeparator(frame, row=None):
    row = frame.grid_size()[1] if row is None else row
    sep = ttk.Separator(frame, orient=tk.HORIZONTAL)
    sep.grid(row=row, columnspan=10, sticky='ew', pady=3)
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
#
#
# # Open a color picker to allow the user to select a color
# def openColorPicker(button, variable):
#     chosenColor = colorchooser.askcolor(initialcolor=variable.get())[0]
#     if chosenColor is not None:
#         variable.set(rgbToString(chosenColor))
#         button.configure(bg=variable.get())
#
#
# # Convert hex string to an RGB tuple
# def stringToRGB(s):
#     if s[0] == '#':
#         s = s[1:]
#     assert(len(s) == 6)
#     return int(s[:2], 16), int(s[2:4], 16), int(s[4:6], 16)
#
#
# # Convert an rgb tuple to a hex string
# def rgbToString(rgb):
#     rgb = [int(c) for c in rgb]
#     r, g, b = rgb
#     return f'#{r:03}{g:03}{b:03}'
#




def build_control_row_entry(frame, label_text, default="", callback=None, width=8):
    row = frame.grid_size()[1]
    createSideLabel(frame, label_text, row)

    variable = tk.StringVar(value=default)
    if callback:
        variable.trace_add("write", lambda *_: callback(variable.get()))

    control = ttk.Entry(frame, textvariable=variable, width=width)
    control.grid(row=row, column=1, columnspan=2, padx=1, sticky=tk.W)
    return variable, control


# Create a row with a label and multiple entry boxes with the given defaults.
# Callback called with tuple of values
def build_control_row_multi_entry(frame, label_text, num_entries, defaults=None, callback=None, width=5):
    row = frame.grid_size()[1]
    createSideLabel(frame, label_text, row)

    if defaults is None:
        defaults = [""]*num_entries

    variables = [tk.StringVar(value=default) for default in defaults]
    if callback is not None:
        for variable in variables:
            variable.trace_add("write", lambda *_: callback([var.get() for var in variables]))

    controls = [ttk.Entry(frame, textvariable=variable, width=width) for variable in variables]
    for i, control in enumerate(controls):
        control.grid(row=row, column=1+i, padx=2, sticky=tk.W)

    return variables, controls


def build_control_row_for_complex(frame, label_text, default=0+0j, callback=None):
    wrapped_callback = None if callback is None else \
        lambda complex_str: callback(complex(f"{complex_str[0].strip()}+{complex_str[1].strip()}"))
    variables, controls = build_control_row_multi_entry(
        frame, label_text, 2, defaults=(default.real, f"{default.imag}j"), callback=wrapped_callback
    )

    # TODO Validation
    return variables, controls


def build_control_row_for_list(frame, label_text, default=("", ""), callback=None):
    variables, controls = build_control_row_multi_entry(
        frame, label_text, len(default), default, callback
    )
    return variables, controls


def build_control_row_for_enum(frame, label_text, default, callback=None):
    row = frame.grid_size()[1]
    createSideLabel(frame, label_text, row)

    enum_type = default.__class__
    enum_values = [e.value for e in enum_type]
    variable = tk.StringVar(value=default.value)
    variable.trace_add("write", lambda *_: callback(enum_type(variable.get())))

    combo = ttk.Combobox(frame, textvariable=variable, values=enum_values, state='readonly', width=10)
    combo.grid(row=row, column=1, columnspan=10, sticky=tk.W)

    return variable, combo


def build_control_row_for_bool(frame, label_text, default=False, callback=None):
    row = frame.grid_size()[1]
    createSideLabel(frame, label_text, row)

    variable = tk.BooleanVar(default)
    variable.trace_add("write", lambda *_: callback(variable.get()))

    checkbox = tk.Checkbutton(frame, variable=variable)
    checkbox.grid(row=row, column=1, sticky=tk.W)
    return variable, checkbox


control_types = {
    bool: build_control_row_for_bool,
    str: build_control_row_entry,
    int: build_control_row_entry,
    float: build_control_row_entry,
    complex: build_control_row_for_complex,
    list: build_control_row_for_list,
    Enum: build_control_row_for_enum,
}


def build_controls_for_object(frame, obj, callback):
    def set_and_call(_obj, _param_name, val):
        setattr(_obj, _param_name, val)
        callback(obj)

    # Loop over each param type and create a control row for it
    # Collect the tkVariables and control widgets
    var_control_tuples = []
    param_defaults, param_types = get_param_info(obj.__class__)
    for param_name, param_default in param_defaults.items():
        param_type = convert_to_builtin(param_types[param_name])
        var_control_tuples.append(
            control_types[param_type](
                frame, label_text=param_name, default=param_default,
                callback=partial(set_and_call, obj, param_name)
            )
        )

    # Turn list of tuples into two lists, variables and controls
    return tuple(zip(*var_control_tuples))
