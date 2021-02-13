import tkinter as tk

import PIL
import PIL.ImageTk
import math
import hallucinator as hl


from ui import controls
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
        controls.build_controls_for_dataclass(control_frame, self.view_settings, self.autorender)


        controls.create_header(control_frame, "Objects")

        controls.create_header(control_frame, "Objects")

        # print("3", cFrame.grid_size())
        # controls.build_control_row_entry(cFrame, "test1", "d1", callback=lambda x: print(f"t1 {x}"))
        # print("4", cFrame.grid_size())
        # controls.build_control_row_multi_entry(
        #     cFrame, "test2", 2, defaults=("d21", "d22"), callback=lambda x: print(f"t2 {x}"))
        # print("5", cFrame.grid_size())
        # controls.build_control_row_for_complex(cFrame, "test3", callback=lambda x: print(f"t3 {x}"))
        # print("6", cFrame.grid_size())
        # controls.build_control_row_for_tuple(cFrame, "test4", default=(0, 2, 3), callback=lambda x: print(f"t4 {x}"))
        # print("7", cFrame.grid_size())
        # controls.build_control_row_for_enum(cFrame, "test5", ColorStyle, callback=lambda x:print(f"t5 {x}"))
        # print(cFrame.grid_size())
        # controls.build_control_row_for_bool(cFrame, "test6", callback=lambda x: print(f"t6 {x}"))



        # controls.build_control_row_entry(cFrame, 1, "Test 1", "Default 1", callback=lambda x: print(f"test 1 {x}"))
        # controls.build_control_row_entry(cFrame, 1, "Test 1", "Default 1", callback=lambda x: print(f"test 1 {x}"))
        # View controls
        # self.bool = tk.BooleanVar()
        # controls.createCheckButton(cFrame, "HSV", self.bool, function=print, row=1)
        # self.bool.trace_add("write", lambda *_: print(self.bool.get()))
        # self.x= []
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


        # controls.createButton(cFrame, "Plotting Options", self.plottingOptionsDialog, 1)
        # controls.createButton(cFrame, "Manage Analyses", self.analysisDialog, 2)
        # controls.createButton(cFrame, "Clear Data", self.clearData, 3)
        # controls.createButton(cFrame, "Reset View", self.resetView, 4)
        # controls.createSlider(cFrame, "Size:", self.sizeCoeff, (.2, 6), 6)
        # self.sizeCoeff.trace('w', self.updateVisuals)
        # controls.createVariableLabel(cFrame, self.regressionStats, 7)
        # controls.createVariableLabel(cFrame, self.pointInfo, 8)

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

    # Set up user bindings
    def set_mouse_bindings(self):
        pass
    #     # bind mouse motions to the canvas
    #     self.canvas.bind('<Button-1>', self.updateClickInfo)
    #     self.canvas.bind('<B1-Motion>', self.translateCanvas)
    #
    #     self.canvas.bind('<Button-3>', self.updateClickInfo)
    #     self.canvas.bind('<B3-Motion>', self.scaleCanvas)
    #
    #     self.canvas.bind('<Button-2>', self.updateClickInfo)
    #     self.canvas.bind('<B2-Motion>', self.rotateCanvas)
    #     self.canvas.bind('<Control-Button-1>', self.updateClickInfo)
    #     self.canvas.bind('<Control-B1-Motion>', self.rotateCanvas)
    #
    #     self.canvas.bind('<Double-Button-1>', self.updatePointInfo)

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
            ComputedObject.new(name="Zone plate", func=zoneplate)
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
        tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))

        # Save the image or python will garbage collect, even if tk is displaying it...
        self.image = tk_image
        self.canvas.delete("image")
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW, tag="image")
        self.update_controls()
        self.updateInfoBar()

    def update_controls(self):
        pass # TODO

    # Update the info bar below the canvas
    def updateInfoBar(self):
        self.info_label.set("I can put an info string here")


    #########################################
    #       Manipulate view  TODO, mousebindings
    #########################################


    # # Stores data information at the time of a click
    # def updateClickInfo(self, event=None):
    #     if event is not None:
    #         self.baseClick = np.array([event.x, event.y], dtype=float)
    #     self.origExtent = np.copy(self.view.extent)
    #     self.origView = self.view.clone()
    #     self.origScale = self.scale
    #     self.origRot = np.copy(self.rotation)
    #
    # # Pans the canvas relative to the scan mark created when the mouse is clicked
    # def translateCanvas(self, event):
    #     motion = np.subtract([event.x, event.y], self.baseClick)
    #     motion = np.divide(motion, [800, 600])
    #     motion = np.multiply(motion, self.view.extent[:2]) * self.sensValues[0] / 25.0
    #     self.view.vrp += motion[0] * self.view.u + motion[1] * self.view.vup
    #     self.updateVisuals()
    #     self.updateClickInfo(event)
    #
    # # Scale the canvas
    # def scaleCanvas(self, event):
    #     factor = (event.y - self.baseClick[1]) / 600 \
    #              * self.sensValues[1] / 10 + 1
    #     if factor > 0.01:
    #         self.scale = min(3.0, max(self.origScale / factor, 0.1))
    #         self.view.extent = self.origScale / self.scale * np.copy(self.origExtent)
    #         self.updateVisuals()


    ############################################
    #       Reset view
    ############################################

    # # Resets the viewing window to its original parameters
    # def resetView(self, event=None):
    #     self.view.reset()
    #     self.scale = 1
    #     self.rotation = np.array([0, 0], dtype=float)
    #     self.updateVisuals()
    #     self.updateClickInfo()
    #
    # # Resets the view and jumps to the XZ plane
    # def gotoXZ(self, event=None):
    #     self.resetView()
    #     self.rotateCanvas(rotU=0, rotVUP=math.pi / 2.0)
    #
    # # Resets the view and jumps to the YZ plane
    # def gotoYZ(self, event=None):
    #     self.resetView()
    #     self.rotateCanvas(rotU=-math.pi / 2.0, rotVUP=math.pi / 2.0)


    ###########################################
    #       Dialog boxes
    ###########################################

    # Examples
    # # Create a dialog box to adjust mouse sensitivity for viewing control
    # def mouseSensitivityDialog(self, event=None):
    #     dialog = dialogs.MouseSensitivityDialog(self.root, self.sensValues)
    #     if dialog.result is not None:
    #         self.sensValues = dialog.result
    #
    # # Create a dialog box to allow the user to select which headers of the data to plot
    # def plottingOptionsDialog(self, event=None):
    #     if self.rawData is None:
    #         self.loadData()
    #         # Return if no data is loaded
    #         if self.rawData is None:
    #             return
    #
    #     # Create a plot setting wizard
    #     wizDict = self.plotSettings.copy()
    #     wizDict['headers'] = self.rawData.get_headers()
    #     frames = [wizards.DimensionSelection(),
    #               wizards.NormalizeTogetherSelection(),
    #               wizards.ColorSelection()]
    #     wizards.Wizard(self.root, frames, options=wizDict,
    #                    title="Plotting Options")
    #
    #     if wizDict['Complete']:
    #         self.plotSettings = wizDict
    #         self.buildData()


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




