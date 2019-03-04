from keyComputations import *

import sys
#from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyqtgraph as pg
import pyqtgraph.opengl as gl

import numpy as np

import json

#TODO: Add dropdown menu for selecting key standards
#TODO: (maybe) Add dropdown menu for selecting key blank

class SpecWidget(QWidget):

    def __init__(self):
        super(SpecWidget, self).__init__()
        self.initUI()

    def initUI(self):
        #Left side is sliders and stuff, right side is dropdown menu and button to generate stl
        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()
        self.horizontal.addLayout(self.vertical)
        self.setMaximumWidth(800)
        self.setLayout(self.horizontal)

        #Values used are for Schlage Classic, except key length
        self.specs = {
        "keyHeight" : .335,
        "keyLength":1.2,
        "macs" : 7,
        "rootCut" : .031,
        "tfc" : .231,
        "increment" : .015,
        "spacing" : .156,
        "pinNumber" : 6,
        "maxDepth":9
        }

        self.spinners = {}
        self.sliders = {}
        self.depths = [0]*10
        self.keyMeshItem = None
        self.data = None

        #Left side of spec widget

        self.initSPinSliderLabel("tfc", "Distance to first cut (inches):",0,1,self.specs["tfc"])
        self.initSPinSliderLabel("spacing","Distance between cuts (inches):",0,1,self.specs["spacing"])
        self.initSPinSliderLabel("increment","Pin height increment (inches):", 0, .2,self.specs["increment"])
        self.initSPinSliderLabel("rootCut", "Width of the cuts (inches):",0, 1,self.specs["rootCut"])
        self.initSPinSliderLabel("macs", "MACS:",0, 10,self.specs["macs"], 1)
        self.initSPinSliderLabel("keyHeight", "Height of the key (inches):",0, 1,self.specs["keyHeight"])
        #self.initSPinSliderLabel("keyLength", "Length of the key (inches):",0, 2,self.specs["keyLength"])
        self.initSPinSliderLabel("pinNumber", "Number of pins:", 1, 10,self.specs["pinNumber"], 1)

        self.initBittingSliders()

        #Spacing between left and right side
        self.horizontal.addSpacing(100)

        #Right side of spec widget
        rightSideLayout = QVBoxLayout()
        self.horizontal.addLayout(rightSideLayout)

        standardLabel = QLabel("Key Bitting Standard:")
        rightSideLayout.addWidget(standardLabel)

        with open("../resources/bittings.json", "r") as read_file:
            self.bittings = json.load(read_file)
        self.standardCombo = QComboBox(self)
        rightSideLayout.addWidget(self.standardCombo)
        for bitting in self.bittings:
            self.standardCombo.addItem(bitting)
        self.standardCombo.activated.connect(self.bitStandardSelect)

        rightSideLayout.addStretch()

        saveBtn = QPushButton("Save .STL")
        rightSideLayout.addWidget(saveBtn)
        saveBtn.clicked.connect(self.saveSTL)

        self.show()

    @pyqtSlot()
    def bitStandardSelect(self):
        std = self.standardCombo.currentText()
        for property in self.bittings[std]:
            self.specs[property] = self.bittings[std][property]
            self.spinners[property].setValue(self.specs[property])

    @pyqtSlot()
    def saveSTL(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '../resources/key.stl', '*.stl')
        if filename == "":
            pass
        else:
            generateSTL(self.data, filename)

    @pyqtSlot()
    def changeSliderValue(self, spinner, slider, spec, step):
        slider.setValue(int(spinner.value() / step))
        self.specs[spec] = spinner.value()
        if spec == "pinNumber":
            self.specs[spec] = int(spinner.value())
            self.changePinNumber()
        self.drawKey()

    @pyqtSlot()
    def changeSpinnerValue(self, spinner, slider, spec, step):
        spinner.setValue(slider.value() * step)
        self.specs[spec] = slider.value() * step
        if spec == "pinNumber":
            self.specs[spec] = int(slider.value() * step)
            self.changePinNumber()
        self.drawKey()

    def initSPinSliderLabel(self, spec, label, minVal, maxVal, val, step = 0.001):
        layout = QVBoxLayout()

        spinbox = QDoubleSpinBox()
        spinbox.setRange(minVal, maxVal)
        spinbox.setSingleStep(step)
        spinbox.setDecimals(int(np.log10(1/step)))
        spinbox.setValue(val)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minVal/step)
        slider.setMaximum(maxVal/step)
        slider.setValue(val/step)

        spinbox.valueChanged.connect(lambda: self.changeSliderValue(spinbox, slider, spec, step))
        slider.valueChanged.connect(lambda: self.changeSpinnerValue(spinbox, slider, spec, step))
        # Label
        label = QLabel(label)

        self.spinners[spec] = spinbox
        self.sliders[spec] = slider

        layout.addWidget(spinbox)
        layout.addWidget(slider)

        superLayout = QHBoxLayout()

        superLayout.addWidget(label)
        superLayout.addSpacing(50)
        superLayout.addLayout(layout)

        self.vertical.addLayout(superLayout)


    def initBittingSliders(self):
        self.slidersLayout = QHBoxLayout()
        self.pinSliders = []
        for i in range(10):
            pin = QSlider(Qt.Vertical)
            pin.setMinimum(0)
            pin.setMaximum(9)
            pin.setTickPosition(QSlider.TicksLeft)
            pin.setTickInterval(1)
            #TODO: add label for pin position underneath the sliders
            pin.valueChanged.connect(self.changePinHeight)
            self.pinSliders.append(pin)
            if i < self.specs["pinNumber"]:
                self.slidersLayout.addWidget(pin)
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(74)
        self.vertical.addLayout(self.slidersLayout)


    @pyqtSlot()
    def changePinHeight(self):
        for i in range(self.specs["pinNumber"]):
            self.depths[i] = self.pinSliders[i].value()
        self.drawKey()

    @pyqtSlot()
    def changePinNumber(self):
        while self.slidersLayout.count():
            item = self.slidersLayout.takeAt(0)
            self.slidersLayout.removeItem(item)
        for i in range(10):
            if i < self.specs["pinNumber"]:
                self.pinSliders[i].show()
                self.slidersLayout.addWidget(self.pinSliders[i])
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(74)
        self.drawKey()


    def drawKey(self):
        #2D Sketch
        x,y = computeSketch(self.specs, self.depths)

        self.parent().pt.setData(x,y)
        self.parent().pt2.setData([0,self.specs["tfc"] + self.specs["pinNumber"]*self.specs["spacing"] + 0.05],[0,0])

        #3D render
        self.data = computeMeshData(x, y, self.specs["pinNumber"], self.depths)

        keyMeshData = gl.MeshData(vertexes=self.data)
        if self.keyMeshItem:
            self.parent().view.removeItem(self.keyMeshItem)
        self.keyMeshItem = gl.GLMeshItem(meshdata = keyMeshData)
        self.parent().view.addItem(self.keyMeshItem)

        #generateSTL(data)

class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        tabs = QTabWidget()

        self.canvas = pg.GraphicsLayoutWidget()
        self.plot = self.canvas.addPlot()
        self.plot.setRange(xRange=(-3,2), yRange=(-1,1))
        self.pt = self.plot.plot(pen='w')
        self.pt2 = self.plot.plot()
        self.pt2.setPen(pg.mkPen('r', style=Qt.DotLine))

        self.view = gl.GLViewWidget()
        self.view.show()

        #Create gird
        zgrid = gl.GLGridItem()
        zgrid.scale(0.1, 0.1, 0.1)
        self.view.addItem(zgrid)

        tabs.addTab(self.canvas, "Sketch")
        tabs.addTab(self.view, "3D View")

        layout.addWidget(tabs,0,0,5,15)

        specs = SpecWidget()
        specs.setMaximumHeight(700)
        layout.addWidget(specs,15,0)
        specs.drawKey()

        self.show()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        mw = MainWidget()
        self.setCentralWidget(mw)
        self.setWindowTitle('Key Designer')
        self.resize(1300,1200)

        self.show()
