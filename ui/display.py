# coding=utf-8
# display.py
#
# Data display and analysis tab for the application
# Written by Kyle McDonell
#
# CS 251
# Spring 2016

import tkinter as tk
import uuid
from dataclasses import asdict
from pprint import pprint

import PIL
import PIL.ImageTk
import math
import hallucinator as hl

from ui import controls, objects, dialogs
from ui.objects import ViewSettings, ColorStyle, PlotStyle, ComputedObject


class DisplayTab:

    # Initializes the display
    def __init__(self, notebook, root):
        # Parents
        self.root = root
        self.notebook = notebook

        # Data
        self.view_settings, default_objects = self.default_settings()
        self.objects = {uuid.uuid1(): obj for obj in default_objects}

        # Build the parts of the tab
        self.frame = tk.Frame(notebook)
        self.build_controls()
        self.build_canvas()
        self.set_mouse_bindings()

        # Render :D
        self.render()

    def default_settings(self):
        view_settings = ViewSettings()
        objs = [ComputedObject.new(name=name, func=func) for name, func in objects.available_objects.items()]
        return view_settings, objs

    #################################
    #       Controls # FIXME This area will never be beautiful :(
    #################################

    def build_controls(self):
        # FIXME setting class variables in each function. Complicated, but stateless is harder.
        #  Would need refresh functions. Probably needs to be rethought...
        self.build_control_frame()
        self.build_control_panel()

        controls.create_separator(self.control_panel)
        self.build_view_controls()
        controls.create_separator(self.control_panel)
        self.build_object_selector()

        self.build_object_controls()
        self.build_rendering_controls()

    # Create a separator and a control frame on the right side of the window
    def build_control_frame(self):
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        # Separator between the controls and the main window
        sep = tk.Frame(self.frame, height=3000, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

    # Build a titled frame for controls to be put in
    def build_control_panel(self):
        self.control_panel = tk.Frame(self.control_frame)
        self.control_panel.pack(side=tk.TOP, fill=tk.Y)
        controls.create_title(self.control_panel, "Control Panel")

    def build_view_controls(self):
        controls.create_header(self.control_panel, "View Settings")
        self.view_controls = controls.build_controls_for_dataclass(
            self.control_panel, self.view_settings, self.autorender
        )

    def build_object_selector(self):
        values = [obj.name for obj_id, obj in self.objects.items()]

        # On first run, record the row so the selector can be rebuilt in the same place
        if not hasattr(self, "object_selector_row"):
            self.object_selector_row = self.control_panel.grid_size()[1]
            self.selected_object_string = tk.StringVar()
            self.selected_object_string.set(values[0])
            self.selected_object_string.trace_add("write", lambda *_: self.build_object_controls())

        # Set selected obj to the first object name if invalid
        # FIXME There should be a function to select an object, not just done implicitly
        if self.selected_object_string.get() not in values:
            self.selected_object_string.set(values[0] if values else "")

        label, self.object_selector = controls.create_combo_box(
            self.control_panel, text="Object", row=self.object_selector_row,
            variable=self.selected_object_string, values=values
        )

    # Build object controls for all objects at the current row of the control_panel if they don't exist and then hide them
    # FIXME I don't like the way this is done. This should probably be multiple functions (create, update, ...?)
    # TODO Scroll bar
    def build_object_controls(self):
        # On first run, create the object_controls dict uuid->controls
        if not hasattr(self, "object_controls"):
            self.object_control_frame = tk.Frame(self.control_frame)
            self.object_control_frame.pack(side=tk.TOP, fill=tk.Y)
            self.object_controls = {}

        # Hide all existing object controls
        for c in self.object_control_frame.children.values():
            c.grid_remove()

        # Create controls for any object that doesn't have them and hide them
        for obj_id, obj in self.objects.items():
            if obj_id not in self.object_controls:
                self.object_controls[obj_id] = controls.build_controls_for_dataclass(
                    self.object_control_frame, obj.params, self.autorender
                )
                for c in self.object_control_frame.children.values():
                    c.grid_remove()

        # Show active object controls
        if self.current_object:
            hl.recursive_map(lambda con: con.grid(), self.object_controls[self.current_object[1]])
        self.autorender()

    # Build a control panel for the user
    def build_rendering_controls(self):
        self.rendering_controls = tk.Frame(self.control_frame, width=2, bd=1)
        self.rendering_controls.pack(side=tk.BOTTOM, fill=tk.X)
        self.rendering_controls.grid_columnconfigure(0, weight=1)
        self.rendering_controls.grid_columnconfigure(1, weight=1)

        button = tk.Button(self.rendering_controls, text="Create Object", command=self.open_create_object_dialog)
        button.grid(row=0, column=0, sticky="ew")

        button = tk.Button(self.rendering_controls, text="Delete", command=self.delete_current_object)
        button.grid(row=0, column=1, sticky="ew")

        button = tk.Button(self.rendering_controls, text="Render", command=self.render)
        button.grid(row=1, column=0, columnspan=2, sticky="ew")
        # rendering_controls.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.Y)

    # TODO Set up user bindings
    def set_mouse_bindings(self):
        pass

    #########################################
    #   Dialogs
    #########################################

    # Create a dialog box to adjust mouse sensitivity for viewing control
    def open_create_object_dialog(self):
        dialogs.SelectorDialog(self.root, "Create Object",
                               choices=list(objects.available_objects.keys()),
                               callback=self.create_object)

    #########################################
    #   Util
    #########################################

    # Returns a tuple (object, uuid) FIXME This is a dangerous way to do this. Asking for a stack overflow...
    @property
    def current_object(self):
        self.build_object_selector()
        object_list = list(self.objects.items())
        return object_list[self.object_selector.current()][::-1] if len(self.objects.items()) > 0 else None

    def create_object(self, obj_name):
        obj = ComputedObject.new(name=obj_name, func=objects.available_objects[obj_name])
        self.objects[uuid.uuid1()] = obj
        self.refresh()

    def delete_current_object(self):
        obj, obj_id = self.current_object
        self.objects.pop(obj_id)
        self.object_controls.pop(obj_id)
        self.refresh()

    def refresh(self):
        self.build_object_selector()
        self.build_object_controls()
        self.autorender()

    #########################################
    #   Visuals
    #########################################

    # Build the canvas on which data is drawn
    def build_canvas(self):
        self.canvas = tk.Canvas(self.frame, width=500, height=500)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def autorender(self, *args):
        if self.view_settings.autorender and hasattr(self, "canvas"):  # FIXME Ugh. This is called before the canvas is built
            self.render(*args)

    # TODO Optimize - imagify all at once, make style flexible
    def render(self, *args):
        def obj_to_image(obj):
            f = obj.func(**asdict(obj.params), view_settings=self.view_settings)
            # f = hl.contour(f, threshold=2*math.pi)
            # return hl.imagify(f, bwref=[0, 2*math.pi], hsv=self.view_settings.style == ColorStyle.HSV)

            # It's objects job to return an image
            return f

        self.canvas.delete("image")
        if len(self.objects) > 0:
            if self.view_settings.render_all and len(self.objects) > 1:
                object_images = [obj_to_image(obj) for obj_id, obj in self.objects.items()]
                image = hl.tile_images(object_images)  # TODO This function sucks
            else:
                image = obj_to_image(self.current_object[0])
            image = hl.np.swapaxes(image, 0, 1)
            tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))

            # Save the image or python will garbage collect, even if tk is displaying it...
            self.image = tk_image
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW, tag="image")

    #################################
    #      File I/O actions TODO
    #################################

    # Load a data file and open plotting options
    # def loadData(self, event=None):
    #     options = {'parent': self.root, 'title': "Choose a data set",
    #                'filetypes': [('csv files', '.csv'),
    #                              ('xml files', '.xml')]}
    #     filename = filedialog.askopenfilename(**options)
    #     if filename:
    #         self.clearData()
    #         self.plotSettings = {}
    #         self.regressionSettings = {}
    #         self.analysisList = []
    #         self.rawData = ...
    #         self.notebook.tab(self.frame, text=filename.split('/')[-1])
    #
    # # Save the opened data set to a csv file
    # def saveData(self, event=None):
    #     if self.rawData is None:
    #             messagebox.showwarning("Error", "There is no data to save")
    #             return
    #     file = filedialog.asksaveasfilename(defaultextension='.csv')
    #     if file:
    #         self.rawData.save_csv(file)
