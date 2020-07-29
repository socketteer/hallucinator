# coding=utf-8
# display.py
#
# Data display and analysis tab for the application
# Written by Kyle McDonell
#
# CS 251
# Spring 2016
import tkinter as tk
from dataclasses import asdict
from pprint import pprint

import PIL
import PIL.ImageTk
import math
import hallucinator as hl


from ui import controls, objects
from ui.objects import ViewSettings, ColorStyle, PlotStyle, ComputedObject


class DisplayTab(object):

    # Initializes the display
    def __init__(self, notebook, root):
        self.root = root
        self.notebook = notebook
        self.frame = tk.Frame(notebook)

        # Data
        self.view_settings, self.objects = self.default_settings()
        self.info_label = tk.StringVar(value="")

        # Build the parts of the application
        self.build_controls()
        self.build_info_bar()
        self.build_canvas()
        self.set_mouse_bindings()

        # Render :D
        self.render()

    def default_settings(self):
        view_settings = ViewSettings()
        objs = [ComputedObject.new(name=name, func=func) for name, func in objects.available_objects.items()]
        return view_settings, objs

    #################################
    #       Build components
    #################################

    # Build a control panel for the user
    def build_controls(self):
        # Create a separator and a control frame on the right side of the window
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        sep = tk.Frame(self.frame, height=3000, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        self.control_panel = tk.Frame(self.control_frame)
        self.control_panel.pack(side=tk.TOP, fill=tk.Y)

        # Separator between the controls and the main window
        controls.create_title(self.control_panel, "Control Panel")

        # Build View Controls
        controls.create_separator(self.control_panel)
        controls.create_header(self.control_panel, "View Settings")
        self.view_setting_controls = controls.build_controls_for_dataclass(
            self.control_panel, self.view_settings, self.autorender
        )

        # Object selector
        controls.create_separator(self.control_panel)
        self.object_selector_row = self.control_panel.grid_size()[1]
        self.object_selector = self.build_object_selector()

        # Object controls
        self.build_object_controls()

        # Rendering controls # TODO make a grid, split into section s
        self.rendering_controls = tk.Frame(self.control_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.rendering_controls.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.X)
        button = controls.create_button(self.rendering_controls, "Render", lambda: self.render)
        button.pack()
        button = controls.create_button(self.rendering_controls, "Delete", lambda: self.objects.pop(self.object_selector.current_index))
        button.pack()
        # rendering_controls.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.Y)


    def build_object_selector(self):
        values = [obj.name for obj in self.objects]

        if not hasattr(self, "selected_object_string"):
            self.selected_object_string = tk.StringVar()
            self.selected_object_string.set(values[0])
            self.selected_object_string.trace_add("write", lambda *_: self.build_object_controls())

        label, control = controls.create_combo_box(
            self.control_panel, text="Object", row=self.object_selector_row,
            variable=self.selected_object_string, values=values
        )
        return control

    def build_object_controls(self):
        if hasattr(self, "object_controls"):  # FIXME I should probably just define everything in init...
            def destroyer(x):
                if hasattr(x, "destroy"):
                    x.destroy()
            hl.recursive_map(destroyer, self.object_controls)

        selected_object = self.objects[self.object_selector.current()]
        self.object_controls = controls.build_controls_for_dataclass(
            self.control_panel, selected_object.params, self.autorender
        )


        # self.param_defaults, param_types = get_param_info(ViewSettings)
        # for i, (param_name, param_default) in enumerate(self.param_defaults.items()):
        #     print(param_name, param_types[param_name])
        #     var, control = build_control_row_for_parameter(
        #         cFrame,
        #         row=i+2,
        #         param_name=param_name,
        #         param_default=param_default,
        #         param_type=param_types[param_name],
        #         param_dict=self.param_defaults)
        #     self.x.append((var, control))

    # Build an info bar below the canvas to display info variables
    def build_info_bar(self):
        bar = tk.Frame(self.frame)
        bar.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.X)
        # make a separator frame
        sep = tk.Frame(self.frame, width=2000, height=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.Y)
        # create a label to display info on the canvas
        tk.Label(bar, textvariable=self.info_label).pack(side=tk.LEFT)
        self.updateInfoBar()

    # Build the canvas on which data is drawn
    def build_canvas(self):
        self.canvas = tk.Canvas(self.frame, width=500, height=500)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    # TODO Set up user bindings
    def set_mouse_bindings(self):
        pass

    #########################################
    #      Build and Update Visuals
    #########################################



    def autorender(self, *args):
        if self.view_settings.autorender:
            self.render()

    # TODO Optimize - imagify all at once, make style flexible
    def render(self, *args):
        def obj_to_image(obj):
            f = obj.func(**asdict(obj.params), view_settings=self.view_settings)
            # f = hl.contour(f, threshold=2*math.pi)
            # return hl.imagify(f, bwref=[0, 2*math.pi], hsv=self.view_settings.style == ColorStyle.HSV)

        # It's objects job to return an image
            return f


        if self.view_settings.render_all and len(self.objects) > 1:
            object_images = [obj_to_image(obj) for obj in self.objects]
            image = hl.tile_images(object_images)
        else:
            image = obj_to_image(self.objects[self.object_selector.current()])
        image = hl.np.swapaxes(image, 0, 1)
        tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))


        # Save the image or python will garbage collect, even if tk is displaying it...
        self.canvas.delete("image")
        self.image = tk_image
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW, tag="image")
        self.updateInfoBar()

    def update_controls(self):
        self.build_object_selector()
        self.build_object_controls()

    # Update the info bar below the canvas
    def updateInfoBar(self):
        self.info_label.set("I can put an info string here")


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
    #         self.updateInfoBar()
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




