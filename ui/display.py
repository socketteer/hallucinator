# coding=utf-8
# display.py
#
# Data display and analysis tab for the application
# Written by Kyle McDonell
#
# CS 251
# Spring 2016
import tkinter as tk
from pprint import pprint

import PIL
import PIL.ImageTk
import math
import hallucinator as hl


from ui import controls, objects
from ui.shapes import ViewSettings, ColorStyle, PlotStyle, zoneplate, ComputedObject


class DisplayTab(object):

    # Initializes the display
    def __init__(self, notebook, root):
        self.root = root
        self.notebook = notebook
        self.frame = tk.Frame(notebook)

        # Data
        self.view_settings, self.shapes = self.default_settings()
        self.info_label = tk.StringVar(value="")

        # Build the parts of the application
        self.build_controls()
        self.build_info_bar()
        self.build_canvas()
        self.set_mouse_bindings()

        # Render :D
        self.render()

    #################################
    #       Build components
    #################################

    # Build a control panel for the user
    def build_controls(self):
        # make a control frame
        control_frame = tk.Frame(self.frame)
        control_frame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        # make a separator frame
        sep = tk.Frame(self.frame, height=2000, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # build control components
        controls.create_title(control_frame, "Control Panel")
        controls.create_separator(control_frame)

        controls.create_header(control_frame, "View Settings")
        view_setting_controls = controls.build_controls_for_object(control_frame, self.view_settings, self.autorender)

        controls.create_header(control_frame, "Objects")
        control_frame.grid_size()[1]

        build_object_controls =

    def build_object_controls(self):
        pass


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


    def default_settings(self):
        view_settings = ViewSettings(
            style=ColorStyle.HSV,
            plot_type=PlotStyle.CONTOUR,
            value_range=(-1, 1),
            resolution=500,
        )
        shapes = [
            ComputedObject.new(name=name, func=func) for name, func in objects.available_objects.items()
        ]
        return view_settings, shapes

    def autorender(self, *args):
        if self.view_settings.autorender:
            self.render()

    # TODO Optimize - imagify all at once, make style flexible
    def render(self, *args):
        shape_images = []
        for shape in self.shapes:
            f = shape.func(**shape.params, view_settings=self.view_settings)
            f = hl.contour(f, threshold=2*math.pi)
            shape_image = hl.imagify(f,
                                     bwref=[0, 2*math.pi],
                                     hsv=self.view_settings.style == ColorStyle.HSV)
            shape_images.append(shape_image)

        image = hl.tile_images(shape_images)
        print(image.shape, image.dtype)
        tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))


        # Save the image or python will garbage collect, even if tk is displaying it...
        self.canvas.delete("image")
        self.image = tk_image
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW, tag="image")
        self.update_controls()
        self.updateInfoBar()

    def update_controls(self):
        pass # TODO

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




