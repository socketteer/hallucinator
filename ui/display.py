# coding=utf-8
# display.py
#
# Data display and analysis tab for the application
# Written by Kyle McDonell
#
# CS 251
# Spring 2016
import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox

import PIL
import cv2
import numpy as np
import math
import colorsys


# Data display and analysis tab object for the application

from ui import dialogs, wizards, controls, view

class DisplayTab(object):

    # Initializes the display
    def __init__(self, notebook, root):
        self.root = root
        self.notebook = notebook
        self.frame = tk.Frame(notebook)

        # Data
        self.rawData = None
        self.data = None
        self.plotSettings = {}
        self.spatialData = None
        self.dimDict = None

        # Regression Data
        self.regressionSettings = {}
        self.regression = None
        self.regressionPoints = None

        # Analysis list
        self.analysisList = []
        self.pcaSettings = {}
        self.clusterSettings = {}

        # View parameters
        self.view = view.View()
        self.origin = np.array([0, 0, 0, 1], dtype=float)
        self.axes = np.array([[1, 0, 0, 1],
                              [0, 1, 0, 1],
                              [0, 0, 1, 1]], dtype=float)
        # Scale coefficient
        self.sizeCoeff = tk.DoubleVar(value=1)

        # Objects on the canvas
        self.axisPoints = []
        self.axisLabels = []
        self.dataPoints = []
        self.regressionLines = []

        # Control Parameters and Variables
        self.baseClick = None
        self.origView = None
        self.origExtent = None
        self.scale = 1
        self.origScale = 1
        self.origRot = np.array([0, 0], dtype=float)
        self.rotation = np.array([0, 0], dtype=float)
        # Mouse sensitivity values
        self.sensValues = [50, 50, 50]

        # Info variables
        self.viewInfo = tk.StringVar(value='')
        self.fileInfo = tk.StringVar(value='')
        self.pointInfo = tk.StringVar(value='')
        self.regressionStats = tk.StringVar(value='')

        # Build the parts of the application
        self.buildControls()
        self.buildInfoBar()
        self.buildCanvas()
        self.buildAxes()
        self.setBindings()






    #################################
    #       Build components
    #################################

    # Build a control panel for the user
    def buildControls(self):
        # make a control frame
        cFrame = tk.Frame(self.frame)
        cFrame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        # make a separator frame
        sep = tk.Frame(self.frame, height=2000, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        # build control components
        controls.createLabel(cFrame, "Control Panel", 0)
        controls.createButton(cFrame, "Plotting Options", self.plottingOptionsDialog, 1)
        controls.createButton(cFrame, "Manage Analyses", self.analysisDialog, 2)
        controls.createButton(cFrame, "Clear Data", self.clearData, 3)
        controls.createButton(cFrame, "Reset View", self.resetView, 4)
        controls.createSlider(cFrame, "Size:", self.sizeCoeff, (.2, 6), 6)
        self.sizeCoeff.trace('w', self.updateVisuals)
        controls.createVariableLabel(cFrame, self.regressionStats, 7)
        controls.createVariableLabel(cFrame, self.pointInfo, 8)

    # Build an info bar below the canvas to display info variables
    def buildInfoBar(self):
        bar = tk.Frame(self.frame)
        bar.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.X)
        # make a separator frame
        sep = tk.Frame(self.frame, width=2000, height=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.Y)
        # create a label to display info on the canvas
        tk.Label(bar, textvariable=self.viewInfo).pack(side=tk.LEFT)
        tk.Label(bar, textvariable=self.fileInfo).pack(side=tk.RIGHT)
        self.updateInfoBar()

    # Build the canvas on which data is drawn
    def buildCanvas(self):
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    # Set up user bindings
    def setBindings(self):
        # bind mouse motions to the canvas
        self.canvas.bind('<Button-1>', self.updateClickInfo)
        self.canvas.bind('<B1-Motion>', self.translateCanvas)

        self.canvas.bind('<Button-3>', self.updateClickInfo)
        self.canvas.bind('<B3-Motion>', self.scaleCanvas)

        self.canvas.bind('<Button-2>', self.updateClickInfo)
        self.canvas.bind('<B2-Motion>', self.rotateCanvas)
        self.canvas.bind('<Control-Button-1>', self.updateClickInfo)
        self.canvas.bind('<Control-B1-Motion>', self.rotateCanvas)

        self.canvas.bind('<Double-Button-1>', self.updatePointInfo)



    #########################################
    #      Build and Update Visuals
    #########################################


    ############################
    #      Axes
    ############################

    # Build axes for the visualization
    def buildAxes(self):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        print(img.shape, img)
        self.cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        #self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))


        # Add a PhotoImage to the Canvas
        # self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        print("Built image")
        return

        # Labels and colors for the axes
        colors = ['red', 'green', 'blue']
        dims = ['x', 'y', 'z']
        vtm = self.view.build()
        tempOrigin = np.dot(vtm, self.origin)
        for index, point in enumerate(self.axes):
            tempPoint = np.dot(vtm, point)
            # Create the axis line from tempOrigin to tempPoint
            self.axisPoints.append(self.canvas.create_line(
                tempOrigin[0], tempOrigin[1], tempPoint[0], tempPoint[1],
                tag='axis', arrow=tk.LAST, fill=colors[index]))
            # Create a label for the axis slightly past the end of the axis
            text = self.plotSettings.get(dims[index])
            text = dims[index] if text is None else text
            self.axisLabels.append(self.canvas.create_text(
                (1 + 0.05) * tempPoint[0] - 0.05 * tempOrigin[0],
                (1 + 0.05) * tempPoint[1] - 0.05 * tempOrigin[1],
                tag='axislabel', fill=colors[index], text=text))


    # Update the axis lines for the visualization given the screen coordinates
    # for the origin and the axis endpoints in a list
    def updateAxes(self, origin, newAxisPoints):
        dims = ['x', 'y', 'z']
        # Update the coordinates of the axes and their labels
        for index, line in enumerate(self.axisPoints):
            # Update the line position
            point = newAxisPoints[index]
            self.canvas.coords(line, origin[0], origin[1], point[0], point[1])
            # Update the axis label
            self.canvas.coords(
                self.axisLabels[index],
                (1 + 0.05) * point[0] - 0.05 * origin[0],
                (1 + 0.05) * point[1] - 0.05 * origin[1])

            # Put the header name on the axis
            text = self.plotSettings.get(dims[index])
            text = dims[index] if text is None else text
            self.canvas.itemconfig(self.axisLabels[index], text=text)


    ##########################
    #      Data
    ##########################

    # Creates the data points on the canvas using the selected columns of the data
    def buildData(self, data=None):

        # Build the display using the raw data if no data is provided
        if data is None:
            self.data = self.rawData
        else:
            self.data = data

        # Delete all old data
        self.clearData()

        # TODO

        # Update the other visuals
        self.updateVisuals()

    # Move each data point to its new position.  Each column in plot points should be
    # a point
    def updateData(self, plotPoints):
        # Calculate the new radius for each point and move it
        for index, pt in enumerate(self.dataPoints):
            r = self.dimDict.get('size')[index]*6+1 if 'size' in self.dimDict else 4
            r *= self.scale * self.sizeCoeff.get()
            self.canvas.coords(pt, plotPoints[0, index]-r, plotPoints[1, index]-r,
                               plotPoints[0, index]+r, plotPoints[1, index]+r)

    # Remove all data from the canvas
    def clearData(self, event=None):
        self.canvas.delete("data")
        self.spatialData = None
        self.dataPoints = []
        self.updateVisuals()


    ###########################
    #      Update Visuals
    ###########################

    # Update all visuals on the canvas and the infobar given the current view orientation
    def updateVisuals(self, *args):
        vtm = self.view.build()

        axisPoints = np.dot(vtm, self.axes.T).T
        origin = np.dot(vtm, self.origin)

        plotPoints = None
        regressPoints = None

        # Axes
        self.updateAxes(origin, axisPoints)
        # Data
        if self.spatialData is not None:
            # Each point is a column
            plotPoints = np.dot(vtm, self.spatialData)
            self.updateData(plotPoints)
        # Reorder visuals
        self.reorderVisuals(origin, axisPoints, plotPoints, regressPoints)

        # Visualization info
        self.updateInfoBar()

    # Reorder the points so the closest points are drawn on top
    def reorderVisuals(self, origin, axisPoints, plotPoints, regressPoints):

        # Sort the axes by the z coord of their midpoint
        zCoords = [0.5 * (origin + pt)[2] for pt in axisPoints]
        ptsToSort = list(zip(zCoords, self.axisPoints))
        ptsToSort += zip(zCoords, self.axisLabels)

        # Sort the data points by their z-coord
        if plotPoints is not None:
            ptsToSort += zip(plotPoints[2,:].tolist(), self.dataPoints)

        # Sort the regression lines using the z coord of the midpoint
        if regressPoints is not None:
            zCoords = [0.5*(regressPoints[2,i]+regressPoints[2,i+1])
                       for i in range(0, regressPoints.shape[1], 2)]

            ptsToSort += zip(zCoords, self.regressionLines)


        sortedPts = [x for (y, x) in sorted(ptsToSort)]

        # Order the points by the sortedPts list
        for pt in sortedPts:
            self.canvas.tag_lower(pt)



    #########################################
    #       Manipulate view
    #########################################


    # Stores data information at the time of a click
    def updateClickInfo(self, event=None):
        if event is not None:
            self.baseClick = np.array([event.x, event.y], dtype=float)
        self.origExtent = np.copy(self.view.extent)
        self.origView = self.view.clone()
        self.origScale = self.scale
        self.origRot = np.copy(self.rotation)

    # Pans the canvas relative to the scan mark created when the mouse is clicked
    def translateCanvas(self, event):
        motion = np.subtract([event.x, event.y], self.baseClick)
        motion = np.divide(motion, [800, 600])
        motion = np.multiply(motion, self.view.extent[:2]) * self.sensValues[0] / 25.0
        self.view.vrp += motion[0] * self.view.u + motion[1] * self.view.vup
        self.updateVisuals()
        self.updateClickInfo(event)

    # Scale the canvas
    def scaleCanvas(self, event):
        factor = (event.y - self.baseClick[1]) / 600 \
                 * self.sensValues[1] / 10 + 1
        if factor > 0.01:
            self.scale = min(3.0, max(self.origScale / factor, 0.1))
            self.view.extent = self.origScale / self.scale * np.copy(self.origExtent)
            self.updateVisuals()

    # Rotate the canvas using a mouse event or with specified rotation values
    def rotateCanvas(self, event=None, rotU=0.0, rotVUP=0.0):
        # Rotate either using the event info or the provided values
        if event is not None:
            rotation = np.subtract([event.x, event.y], self.baseClick) \
                       * self.sensValues[2] / 50 * math.pi / 600
        else:
            rotation = np.array([rotU, -rotVUP], dtype=float)
        self.view = self.origView.clone()
        self.view.rotateOrigin(rotation[1], -rotation[0])
        # Update the rotation variable and the display
        self.rotation = np.mod(self.origRot + rotation / math.pi, 2)
        self.updateVisuals()

    # Get data about a point under the mouse
    def updatePointInfo(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        nearMouse = self.canvas.find_overlapping(x + 3, y + 3, x - 3, y - 3)

        tip = ''
        if len(nearMouse) > 0:
            # Get the nearest data point
            points = self.canvas.find_withtag('data')
            nearest = None
            for pt in nearMouse:
                if pt in points:
                    nearest = pt
                    break
            # Display information for it
            if nearest is not None:
                index = points.index(nearest)

                tip = 'Point Information:\n'
                xhead = self.plotSettings['x']
                yhead = self.plotSettings['y']
                tip += 'x: {0:.2f}\ny: {1:.2f}\n'.format(
                    self.data.get_value(xhead, index),
                    self.data.get_value(yhead, index))
                if len(self.plotSettings['dimensions']) > 2:
                    zhead = self.plotSettings['z']
                    tip += 'z: {0:.2f}\n'.format(self.data.get_value(zhead, index))
                if self.plotSettings.get('color') is not None:
                    chead = self.plotSettings['color']
                    tip += 'color: {0:.2f}\n'.format(self.data.get_value(chead, index))
                if self.plotSettings.get('size') is not None:
                    shead = self.plotSettings['size']
                    tip += 'size: {0:.2f}\n'.format(self.data.get_value(shead, index))

        self.pointInfo.set(tip)

    # Update the info bar below the canvas
    def updateInfoBar(self):
        pi = u'\u03C0'.encode('utf-8')
        xRot = "X-Rotation: {0:.2f}{1}".format(self.rotation[1], pi)
        yRot = "Y-Rotation: {0:.2f}{1}".format(self.rotation[0], pi)
        zoom = "Zoom: {0:1d}%".format(int(self.scale * 100))
        self.viewInfo.set("{0: <25} {1: <25} {2: <10}".format(xRot, yRot, zoom))

        filename = "No data file" if self.rawData is None \
            else self.rawData.get_filename().split('/')[-1]
        self.fileInfo.set(filename)




    ############################################
    #       Reset view
    ############################################

    # Resets the viewing window to its original parameters
    def resetView(self, event=None):
        self.view.reset()
        self.scale = 1
        self.rotation = np.array([0, 0], dtype=float)
        self.updateVisuals()
        self.updateClickInfo()

    # Resets the view and jumps to the XZ plane
    def gotoXZ(self, event=None):
        self.resetView()
        self.rotateCanvas(rotU=0, rotVUP=math.pi / 2.0)

    # Resets the view and jumps to the YZ plane
    def gotoYZ(self, event=None):
        self.resetView()
        self.rotateCanvas(rotU=-math.pi / 2.0, rotVUP=math.pi / 2.0)







    ###########################################
    #       Dialog boxes
    ###########################################

    # Create a dialog box to adjust mouse sensitivity for viewing control
    def mouseSensitivityDialog(self, event=None):
        dialog = dialogs.MouseSensitivityDialog(self.root, self.sensValues)
        if dialog.result is not None:
            self.sensValues = dialog.result

    # Create a dialog box to allow the user to select which headers of the data to plot
    def plottingOptionsDialog(self, event=None):
        if self.rawData is None:
            self.loadData()
            # Return if no data is loaded
            if self.rawData is None:
                return

        # Create a plot setting wizard
        wizDict = self.plotSettings.copy()
        wizDict['headers'] = self.rawData.get_headers()
        frames = [wizards.DimensionSelection(),
                  wizards.NormalizeTogetherSelection(),
                  wizards.ColorSelection()]
        wizards.Wizard(self.root, frames, options=wizDict,
                       title="Plotting Options")

        if wizDict['Complete']:
            self.plotSettings = wizDict
            self.buildData()

    # Create a dialog to select a regression
    def regressionDialog(self, event=None):
        if self.rawData is None:
            self.loadData()
            # Return if no data is loaded
            if self.rawData is None:
                return

        if self.spatialData is None:
            self.plottingOptionsDialog()
        if self.spatialData is None:
            return

        # Initialize the wizard dict
        wizDict = self.regressionSettings.copy()
        for dim in ['x', 'y', 'z']:
            wizDict[dim] = self.plotSettings.get(dim)
        wizDict['headers'] = self.data.get_headers()

        # Create the wizard
        frames = [wizards.RegressionSelection(),
                  wizards.ShotgunRegressionSelection(),
                  wizards.ManualRegressionSelection()]
        wizards.Wizard(self.root, frames, options=wizDict,
                       title="Linear Regression")

        if wizDict['Complete']:
            self.regressionSettings = wizDict
            # Build and display a manual regression if requested
            if wizDict['type'] == 'manual':
                self.buildRegression()
            # Otherwise display a dialog of the best models
            elif wizDict['type'] == 'shotgun':
                regs = analysis.shotgun_regression(
                    self.data, wizDict['shotgun dependent'],
                    wizDict['shotgun independent'])
                self.saveRegression(regressions=regs)

    # Create a dialog to run PCA on the data set and then display the results
    def pcaDialog(self, event=None):
        if self.rawData is None:
            self.loadData()
            if self.rawData is None:
                return

        # Initialize the wizard dict
        wizDict = self.pcaSettings.copy()
        wizDict['data'] = self.rawData

        # Create the wizard
        frames = [wizards.PCAPrompt(),
                  wizards.PCAInfoDisplay()]
        wizards.Wizard(self.root, frames, options=wizDict,
                       title="Principal Components Analysis")

        # Save user selections and add the pca to the pca list
        if wizDict['Complete']:
            self.pcaSettings = wizDict
            self.analysisList.append(
                {'type': 'PCA',
                 'name': wizDict['name'],
                 'analysis': wizDict['PCA']})

        # Create a dialog to run PCA on the data set and then display the results
    def clusterDialog(self, event=None):
        if self.rawData is None:
            self.loadData()
            if self.rawData is None:
                return

        # Initialize the wizard dict
        wizDict = self.clusterSettings.copy()
        wizDict['data'] = self.rawData

        # Create the wizard
        frames = [wizards.ClusterHeaderSelection(),
                  wizards.ClusterAlgorithmSelection(),
                  wizards.ClusterInfoDisplay()]
        wizards.Wizard(self.root, frames, options=wizDict,
                       title="Cluster Analysis")

        # Save user selections and add the pca to the pca list
        if wizDict['Complete']:
            self.pcaSettings = wizDict
            self.analysisList.append(
                {'type': 'Cluster',
                 'name': wizDict['name'],
                 'analysis': wizDict['Cluster']})

    # Popup a window to manage saved analyses
    def analysisDialog(self, event=None):
        dialog = dialogs.AnalysisManagementDialog(self.root, self, self.analysisList[:])
        if dialog.result is not None:
            self.analysisList = dialog.result


    #################################
    #      File I/O actions
    #################################

    # Load a data file and open plotting options
    def loadData(self, event=None):
        options = {'parent': self.root, 'title': "Choose a data set",
                   'filetypes': [('csv files', '.csv'),
                                 ('xml files', '.xml')]}
        filename = filedialog.askopenfilename(**options)
        if filename:
            self.clearData()
            self.plotSettings = {}
            self.regressionSettings = {}
            self.analysisList = []
            self.rawData = ...
            self.updateInfoBar()
            self.notebook.tab(self.frame, text=filename.split('/')[-1])

    # Save the opened data set to a csv file
    def saveData(self, event=None):
        if self.rawData is None:
                messagebox.showwarning("Error", "There is no data to save")
                return
        file = filedialog.asksaveasfilename(defaultextension='.csv')
        if file:
            self.rawData.save_csv(file)




