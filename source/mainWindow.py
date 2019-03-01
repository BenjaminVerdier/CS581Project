import sys
#from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyqtgraph as pg
import pyqtgraph.opengl as gl

import numpy as np

from stl import mesh

#TODO: Add dropdown menu for selecting key standards
#TODO: (maybe) Add dropdown menu for selecting key blank

class SpecWidget(QWidget):

    def __init__(self):
        super(SpecWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.vertical = QVBoxLayout()
        self.setMaximumWidth(800)
        self.setLayout(self.vertical)


        #Values used are for Schlage Classic, except key length
        self.keyHeight = .335
        self.keyLength = 2
        self.macs = 7
        self.rootCut = .031
        self.tfc = .231
        self.increment = .015
        self.spacing = .156
        self.pinNumber = 6
        self.keyMeshItem = None

        self.initSPinSliderLabel("tfc", "Distance to first cut (inches):",0,1,self.tfc)
        self.initSPinSliderLabel("spacing","Distance between cuts (inches):",0,1,self.spacing)
        self.initSPinSliderLabel("increment","Pin height increment (inches):", 0, .2, self.increment)
        self.initSPinSliderLabel("rootCut", "Width of the cuts (inches):",0, 1, self.rootCut)
        self.initSPinSliderLabel("macs", "MACS:",0, 10, self.macs, 1)
        self.initSPinSliderLabel("keyHeight", "Height of the key (inches):",0, 1, self.keyHeight)
        #self.initSPinSliderLabel("keyLength", "Length of the key (inches):",0, 2, self.keyLength)
        self.initSPinSliderLabel("pinNumber", "Number of pins:", 1, 10, self.pinNumber, 1)
        self.initBittingSliders()

        self.show()

    @pyqtSlot()
    def changeSliderValue(self, spinner, slider, spec, step):
        slider.setValue(int(spinner.value() / step))
        if spec == "tfc":
            self.tfc = spinner.value()
        elif spec == "spacing":
            self.spacing = spinner.value()
        elif spec == "increment":
            self.increment = spinner.value()
        elif spec == "rootCut":
            self.rootCut = spinner.value()
        elif spec == "macs":
            self.macs = int(spinner.value())
        elif spec == "keyHeight":
            self.keyHeight = spinner.value()
        elif spec == "keyLength":
            self.keyLength = spinner.value()
        elif spec == "pinNumber":
            self.pinNumber = int(spinner.value())
            self.changePinNumber()
        self.drawKey()

    @pyqtSlot()
    def changeSpinnerValue(self, spinner, slider, spec, step):
        spinner.setValue(slider.value() * step)
        if spec == "tfc":
            self.tfc = slider.value() * step
        elif spec == "spacing":
            self.spacing = slider.value() * step
        elif spec == "increment":
            self.increment = slider.value() * step
        elif spec == "rootCut":
            self.rootCut = slider.value() * step
        elif spec == "macs":
            self.macs = int(slider.value() * step)
        elif spec == "keyHeight":
            self.keyHeight = slider.value() * step
        elif spec == "keyLength":
            self.keyLength = slider.value() * step
        elif spec == "pinNumber":
            self.pinNumber = int(slider.value() * step)
            self.changePinNumber()
        self.drawKey()

    def initSPinSliderLabel(self, spec, label, min, max, val, step = 0.001):
        layout = QVBoxLayout()

        spinbox = QDoubleSpinBox()
        spinbox.setRange(min, max)
        spinbox.setSingleStep(step)
        spinbox.setDecimals(3)
        spinbox.setValue(val)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min/step)
        slider.setMaximum(max/step)
        slider.setValue(val/step)

        spinbox.valueChanged.connect(lambda: self.changeSliderValue(spinbox, slider, spec, step))
        slider.valueChanged.connect(lambda: self.changeSpinnerValue(spinbox, slider, spec, step))
        # Label
        label = QLabel(label)

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
            pin.valueChanged.connect(lambda: self.changePinHeight(i))
            self.pinSliders.append(pin)
            if i < self.pinNumber:
                self.slidersLayout.addWidget(pin)
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(74)
        self.vertical.addLayout(self.slidersLayout)


    @pyqtSlot()
    def changePinHeight(self, pinNumber):
        self.drawKey()

    @pyqtSlot()
    def changePinNumber(self):
        while self.slidersLayout.count():
            item = self.slidersLayout.takeAt(0)
            self.slidersLayout.removeItem(item)
        for i in range(10):
            if i < self.pinNumber:
                self.pinSliders[i].show()
                self.slidersLayout.addWidget(self.pinSliders[i])
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(74)
        self.drawKey()


    def drawKey(self):
        #2D Sketch
        x = [0]
        y = [0]
        depths = []
        for i in range(self.pinNumber):
            x.append(self.tfc + i*self.spacing - self.rootCut/2)
            y.append(-self.increment*self.pinSliders[i].value())
            x.append(self.tfc + i*self.spacing + self.rootCut/2)
            y.append(-self.increment*self.pinSliders[i].value())
            depths.append(self.increment*self.pinSliders[i].value())

        #Bottom part
        x.append(x[-1] + self.spacing)
        y.append(-10*self.increment)
        #Need this to for mesh design
        for i in range(self.pinNumber):
            x.append(self.tfc + (self.pinNumber-1-i)*self.spacing + self.rootCut/2)
            y.append(-10*self.increment)
            x.append(self.tfc + (self.pinNumber-1-i)*self.spacing - self.rootCut/2)
            y.append(-10*self.increment)

        x.append(0)
        y.append(-10*self.increment)

        x.append(0)
        y.append(-self.keyHeight + .1)
        x.append(self.tfc+2*self.spacing)
        y.append(-self.keyHeight + .1)
        x.append(self.tfc+2*self.spacing)
        y.append(-self.keyHeight)
        x.append(0)
        y.append(-self.keyHeight)

        #Handle
        x.append(0)
        y.append(y[-1]-.1)
        x.append(-.3)
        y.append(y[-1])
        x.append(-1.5)
        y.append(y[-1])
        x.append(-1.5)
        y.append(0.7)
        x.append(-.3)
        y.append(0.7)
        x.append(-.3)
        y.append(0.1)
        x.append(0)
        y.append(0.1)
        x.append(0)
        y.append(0)


        self.parent().pt.setData(x,y)
        self.parent().pt2.setData([0,self.tfc + self.pinNumber*self.spacing + 0.05],[0,0])

        #3D render
        extrudedHeight = 0.1
        #This is super messy, really. Might want to change this.
        pointsBase = list(zip(x,y,[0]*len(x)))
        pointsExtruded = list(zip(x,y,[extrudedHeight]*len(x)))

        #sides
        data = np.zeros((2*(len(x)-1),3,3))
        for i in range(len(x)-1):
            data[2*i,0] = pointsBase[i]
            data[2*i,2] = pointsBase[i+1]
            data[2*i,1] = pointsExtruded[i]
            data[2*i + 1,0] = pointsBase[i+1]
            data[2*i + 1,2] = pointsExtruded[i+1]
            data[2*i + 1,1] = pointsExtruded[i]

        #handle
        data = np.insert(data,len(data),[pointsBase[-2],pointsBase[-8],pointsBase[-7]], axis=0)
        data = np.insert(data,len(data),[pointsBase[-2],pointsBase[-7],pointsBase[-3]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-2],pointsExtruded[-7],pointsExtruded[-8]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-2],pointsExtruded[-3],pointsExtruded[-7]], axis=0)
        data = np.insert(data,len(data),[pointsBase[-7],pointsBase[-6],pointsBase[-4]], axis=0)
        data = np.insert(data,len(data),[pointsBase[-6],pointsBase[-5],pointsBase[-4]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-7],pointsExtruded[-4],pointsExtruded[-6]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-6],pointsExtruded[-4],pointsExtruded[-5]], axis=0)
        data = np.insert(data,len(data),[pointsBase[-9],pointsBase[-12],pointsBase[-10]], axis=0)
        data = np.insert(data,len(data),[pointsBase[-10],pointsBase[-12],pointsBase[-11]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-9],pointsExtruded[-10],pointsExtruded[-12]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[-10],pointsExtruded[-11],pointsExtruded[-12]], axis=0)

        #bitting
        prevDepth = 0
        for i in range(self.pinNumber):
            if prevDepth == depths[i]:
                data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+2],pointsBase[2+4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsBase[2*i+2],pointsBase[4*self.pinNumber-2*i],pointsBase[2+4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2*i],pointsExtruded[2+4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2+4*self.pinNumber-2*i],pointsExtruded[4*self.pinNumber-2*i]], axis=0)
            else:
                data = np.insert(data,len(data),[pointsBase[2*i+1],pointsBase[2*i+2],pointsBase[4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsBase[2*i+1],pointsBase[4*self.pinNumber-2*i],pointsBase[1+4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2*i+1],pointsExtruded[4*self.pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i+1],pointsExtruded[1+4*self.pinNumber-2*i],pointsExtruded[4*self.pinNumber-2*i]], axis=0)
                if prevDepth < depths[i]:
                    midPointBase = [pointsBase[2*i][0],pointsBase[2*i+1][1],0]
                    midPointExtruded = [pointsBase[2*i][0],pointsBase[2*i+1][1],extrudedHeight]
                    data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+1],midPointBase], axis=0)
                    data = np.insert(data,len(data),[pointsBase[2+4*self.pinNumber-2*i],midPointBase,pointsBase[2*i+1]], axis=0)
                    data = np.insert(data,len(data),[pointsBase[1+4*self.pinNumber-2*i],pointsBase[2+4*self.pinNumber-2*i],pointsBase[2*i+1]], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2*i],midPointExtruded,pointsExtruded[2*i+1]], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2+4*self.pinNumber-2*i],pointsExtruded[2*i+1],midPointExtruded], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2+4*self.pinNumber-2*i],pointsExtruded[1+4*self.pinNumber-2*i],pointsExtruded[2*i+1]], axis=0)

                else:
                    midPointBase = [pointsBase[2*i+1][0],pointsBase[2*i][1],0]
                    midPointExtruded = [pointsBase[2*i+1][0],pointsBase[2*i][1],extrudedHeight]
                    data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+1],midPointBase], axis=0)
                    data = np.insert(data,len(data),[pointsBase[2+4*self.pinNumber-2*i],pointsBase[2*i],midPointBase], axis=0)
                    data = np.insert(data,len(data),[pointsBase[2+4*self.pinNumber-2*i],midPointBase,pointsBase[1+4*self.pinNumber-2*i]], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2*i],midPointExtruded,pointsExtruded[2*i+1]], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2+4*self.pinNumber-2*i],midPointExtruded,pointsExtruded[2*i]], axis=0)
                    data = np.insert(data,len(data),[pointsExtruded[2+4*self.pinNumber-2*i],pointsExtruded[1+4*self.pinNumber-2*i],midPointExtruded], axis=0)
            prevDepth = depths[i]
        data = np.insert(data,len(data),[pointsBase[2*self.pinNumber],pointsBase[2*self.pinNumber+1],pointsBase[2*self.pinNumber+2]], axis=0)
        data = np.insert(data,len(data),[pointsExtruded[2*self.pinNumber],pointsExtruded[2*self.pinNumber+2],pointsExtruded[2*self.pinNumber+1]], axis=0)

        key = mesh.Mesh(np.zeros(data.shape[0], dtype=mesh.Mesh.dtype))
        key.vectors = data
        key.save('key.stl')
        keyMeshData = gl.MeshData(vertexes=data)
        if self.keyMeshItem:
            self.parent().view.removeItem(self.keyMeshItem)
        self.keyMeshItem = gl.GLMeshItem(meshdata = keyMeshData)
        self.parent().view.addItem(self.keyMeshItem)

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

        ## create three grids, add each to the view
        zgrid = gl.GLGridItem()
        #self.view.addItem(zgrid)

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
