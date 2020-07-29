# import tkinter as tk
# from enum import Enum
# from functools import partial
# from tkinter import ttk, font
#
# from ui.util import convert_to_builtin, get_param_info_dataclass
#
#
# ##################################################################
# # Labels
# ##################################################################
#
# def create_label(frame, text, row=None, underline=False, size=12, col=0, columnspan=2, pady=3, padx=8, **kwargs):
#     row = frame.grid_size()[1] if row is None else row
#     label = tk.Label(frame, text=text)
#     label_font = tk.font.Font(label, label.cget("font"))
#     label_font.configure(underline=underline, size=size)
#     label.configure(font=label_font)
#     label.grid(row=row, column=col, columnspan=columnspan, padx=padx, pady=pady, **kwargs)
#     return label
#
#
# # Creates a label on the first column of the frame
# def create_side_label(frame, text, row=None, col=0):
#     return create_label(frame, text, row, col=col, columnspan=1)
#
#
# # Create a label which is updated with a variable
# def create_variable_label(frame, variable, row=None):
#     label = tk.Label(frame, textvariable=variable)
#     label.grid(row=row, columnspan=2, pady=5)
#     return label
#
#
# # Create a title on with the given text on the specified row
# def create_title(frame, text, row=None):
#     return create_label(frame, text, row, size=14, columnspan=10, pady=3)
#
#
# # Creates a label centered on the row
# def create_header(frame, text, row=None):
#     return create_label(frame, text, row, size=12, columnspan=10, pady=4, sticky=tk.W)
#
#
# # Creates a separator on the given row
# def create_separator(frame, row=None):
#     row = frame.grid_size()[1] if row is None else row
#     sep = ttk.Separator(frame, orient=tk.HORIZONTAL)
#     sep.grid(row=row, columnspan=10, sticky='ew', pady=3)
#     return sep
#
#
# ##################################################################
# # Control primitives
# ##################################################################
#
#
# # Creates a menubar on the root given a menu dictionary with the follow format:
# # i.e. a list of pairs containing menu headers and a list of (menuitem, command) pairs
# # and '-' as a separator
# # e.g. [ ('File', [('Item1', 'BindingText', 'Binding', Cmd1), '-',
# #                  ('Item2', 'BindingText', 'Binding', Cmd2)] ),
# #           ('Edit', [ .... ] ) ]
# def create_menubar(root, menu_list):
#     # Create a new menu bar and add it to root
#     menu_bar = tk.Menu(root)
#     root.config(menu=menu_bar)
#     # Create each sub menu and fill it with its items
#     for menuTitle, menuItems in menu_list:
#         # Add the menu to the menu bar
#         menu = tk.Menu(menu_bar)
#         menu_bar.add_cascade(label=menuTitle, menu=menu)
#         for item in menuItems:
#             if item == '-':
#                 menu.add_separator()
#             else:
#                 # justification doesn't work with menus?
#                 label = item[0] + '     ' + item[1] if item[1] is not None else item[0]
#                 menu.add_command(label=label,
#                                  command=item[3])
#                 if item[2] is not None:
#                     root.bind(item[2], item[3])
#     return menu_bar
#
#
# # Create a button on the specified row with the specified text and function call
# def create_button(frame, text, function, row=None):
#     row = frame.grid_size()[1] if row is None else row
#     button = tk.Button(frame, text=text, command=function, width=18)
#     button.grid(row=row, columnspan=2, pady=3)
#     return button
#
#
# # Create a combobox with a text label, specified values, and selected variable
# def create_combo_box(frame, text, variable, values, row=None, width=10):
#     row = frame.grid_size()[1] if row is None else row
#     column = 0
#     if text != "":
#         label = create_side_label(frame, text, row)
#         column += 1
#     else:
#         label = None
#     combo = ttk.Combobox(frame, textvariable=variable, state='readonly', width=width, values=values)
#     combo.grid(row=row, column=column, columnspan=10, pady=3)
#     return label, combo
#
#
# def build_control_row_entry(frame, label_text, default="", callback=None, width=12):
#     row = frame.grid_size()[1]
#     label = create_side_label(frame, label_text, row)
#
#     variable = tk.StringVar(value=default)
#     if callback:
#         variable.trace_add("write", lambda *_: callback(variable.get()))
#
#     control = ttk.Entry(frame, textvariable=variable, width=width)
#     control.grid(row=row, column=1, columnspan=2, padx=1, sticky=tk.W)
#     return label, variable, control
#
#
# # Create a row with a label and multiple entry boxes with the given defaults.
# # Callback called with tuple of values
# def build_control_row_multi_entry(frame, label_text, num_entries, defaults=None, callback=None, data_type=str, width=5):
#     row = frame.grid_size()[1]
#     label = create_side_label(frame, label_text, row)
#
#     if defaults is None:
#         defaults = [""]*num_entries
#
#     variables = [tk.StringVar(value=default) for default in defaults]
#     if callback is not None:
#         for variable in variables:
#             variable.trace_add("write", lambda *_: callback([data_type(var.get()) for var in variables]))
#
#     controls = [ttk.Entry(frame, textvariable=variable, width=width) for variable in variables]
#     for i, control in enumerate(controls):
#         control.grid(row=row, column=1+i, padx=2, sticky=tk.W)
#
#     return label, variables, controls
#
#
# def build_control_row_for_complex(frame, label_text, default=0+0j, callback=None):
#     wrapped_callback = None if callback is None else \
#         lambda complex_str: callback(complex(f"{complex_str[0].strip()}+{complex_str[1].strip()}"))
#     label, variables, controls = build_control_row_multi_entry(
#         frame, label_text, 2, defaults=(default.real, f"{default.imag}j"), callback=wrapped_callback
#     )
#
#     # TODO Validation
#     return label, variables, controls
#
#
# def build_control_row_for_list(frame, label_text, default=("", ""), callback=None):
#     label, variables, controls = build_control_row_multi_entry(
#         frame, label_text, len(default), default, callback
#     )
#     return label, variables, controls
#
#
# def build_control_row_for_enum(frame, label_text, default, callback=None):
#     row = frame.grid_size()[1]
#     label = create_side_label(frame, label_text, row)
#
#     enum_type = default.__class__
#     enum_values = [e.value for e in enum_type]
#     variable = tk.StringVar(value=default.value)
#     variable.trace_add("write", lambda *_: callback(enum_type(variable.get())))
#
#     combo = ttk.Combobox(frame, textvariable=variable, values=enum_values, state='readonly', width=10)
#     combo.grid(row=row, column=1, columnspan=10, sticky=tk.W)
#
#     return label, variable, combo
#
#
# def build_control_row_for_bool(frame, label_text, default=False, callback=None):
#     row = frame.grid_size()[1]
#     label = create_side_label(frame, label_text, row)
#
#     variable = tk.BooleanVar()
#     variable.set(default)
#     variable.trace_add("write", lambda *_: callback(variable.get()))
#
#     checkbox = tk.Checkbutton(frame, variable=variable)
#     checkbox.grid(row=row, column=1, sticky=tk.W)
#     return label, variable, checkbox
#
#
# def build_slider_control(frame, label_text, default="", callback=None):
#     pass
#
# control_types = {
#     bool: build_control_row_for_bool,
#     str: build_control_row_entry,
#     int: build_control_row_entry,
#     float: build_control_row_entry,
#     complex: build_control_row_for_complex,
#     list: build_control_row_for_list,
#     Enum: build_control_row_for_enum,
# }
# def build_controls_for_dataclass(frame, obj, callback):
#     def set_and_call(_obj, _param_name, data_type, subtypes, val):
#         if subtypes:
#             val = [subtype(v) for subtype, v in zip(subtypes, val)]
#         elif data_type != Enum: # ugh... This has become terrible
#             val = data_type(val)
#         setattr(_obj, _param_name, val)
#         callback(obj)
#
#     # Loop over each param type and create a control row for it
#     # Collect the tkVariables and control widgets
#     label_var_control_tuples = []
#     param_defaults, param_types = get_param_info_dataclass(obj.__class__)
#     for param_name, param_type in param_types.items():
#         param_type, param_subtypes = convert_to_builtin(param_type)
#         print(param_name, param_defaults)
#         control_func = control_types[param_type]
#         label_var_control_tuples.append(control_func(
#             frame,
#             label_text=param_name,
#             default=getattr(obj, param_name),
#             callback=partial(set_and_call, obj, param_name, param_type, param_subtypes)
#         ))
#
#     # # Turn list of tuples into two lists, variables and controls
#     # return tuple(zip(*var_control_tuples))
#     return label_var_control_tuples
#
