import sys
#from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyqtgraph as pg

class SpecWidget(QWidget):

    def __init__(self):
        super(SpecWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.vertical = QVBoxLayout()
        self.setMaximumWidth(800)
        self.setLayout(self.vertical)

        #TODO: add sliders and spinners for that.
        self.keyHeight = .335
        self.keyLength = 2
        self.macs = 7
        self.rootCut = .031
        self.tfc = .231
        self.increment = .015
        self.spacing = .156

        self.initSPinSliderLabel("tfc", "Distance to first cut (inches):",0,1,self.tfc)
        self.initSPinSliderLabel("spacing","Distance between cuts (inches):",0,1,self.spacing)
        self.initSPinSliderLabel("increment","Pin height increment (inches):", 0, .2, self.increment)
        self.initBittingSpecs()

        self.show()

    @pyqtSlot()
    def changeSliderValue(self, spinner, slider, spec):
        slider.setValue(int(spinner.value() * 1000))
        if spec == "tfc":
            self.tfc = spinner.value()
        elif spec == "spacing":
            self.spacing = spinner.value()
        elif spec == "increment":
            self.increment = spinner.value()
        self.drawKey()

    @pyqtSlot()
    def changeSpinnerValue(self, spinner, slider, spec):
        spinner.setValue(slider.value() / 1000)
        if spec == "tfc":
            self.tfc = slider.value() / 1000
        elif spec == "spacing":
            self.spacing = slider.value() / 1000
        elif spec == "increment":
            self.increment = slider.value() / 1000
        self.drawKey()

    def initSPinSliderLabel(self, spec, label, min, max, val):
        layout = QVBoxLayout()

        spinbox = QDoubleSpinBox()
        spinbox.setRange(min, max)
        spinbox.setSingleStep(.001)
        spinbox.setDecimals(3)
        spinbox.setValue(val)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min*1000)
        slider.setMaximum(max*1000)
        slider.setValue(val*1000)

        spinbox.valueChanged.connect(lambda: self.changeSliderValue(spinbox, slider, spec))
        slider.valueChanged.connect(lambda: self.changeSpinnerValue(spinbox, slider, spec))
        # Label
        label = QLabel(label)

        layout.addWidget(spinbox)
        layout.addWidget(slider)

        superLayout = QHBoxLayout()

        superLayout.addWidget(label)
        superLayout.addSpacing(50)
        superLayout.addLayout(layout)

        self.vertical.addLayout(superLayout)


    def initBittingSpecs(self):
        bittingWidget = QWidget()
        layout = QVBoxLayout()

        hlayout = QHBoxLayout()

        pinNumLabel = QLabel("Number of pins:")

        self.pinNumberSpinBox = QSpinBox()
        self.pinNumberSpinBox.setRange(1,10)
        self.pinNumberSpinBox.setSingleStep(1)
        self.pinNumberSpinBox.setValue(6)
        self.pinNumberSpinBox.valueChanged.connect(self.changePinNumber)

        hlayout.addWidget(pinNumLabel)
        hlayout.addWidget(self.pinNumberSpinBox)
        hlayout.addStretch()

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
            if i < self.pinNumberSpinBox.value():
                self.slidersLayout.addWidget(pin)
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(58)

        layout.addLayout(hlayout)
        layout.addLayout(self.slidersLayout)

        bittingWidget.setLayout(layout)

        self.vertical.addWidget(bittingWidget)

    def drawKey(self):
        pinNumber = self.pinNumberSpinBox.value()

        x = [0]
        y = [0]
        depths = []
        for i in range(pinNumber):
            x.append(self.tfc + i*self.spacing - self.rootCut/2)
            y.append(-self.increment*self.pinSliders[i].value())
            x.append(self.tfc + i*self.spacing + self.rootCut/2)
            y.append(-self.increment*self.pinSliders[i].value())
            depths.append(self.increment*self.pinSliders[i].value())

        #Bottom part
        lp = [x[-1],-min(max(depths)+self.macs, 9*self.increment)]
        lp[0] = lp[0] + self.spacing
        x.append(lp[0])
        y.append(lp[1])
        x.append(lp[0])
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
        x.append(-1.5)
        y.append(y[-1])
        x.append(-1.5)
        y.append(0.3)
        x.append(-.5)
        y.append(0.3)
        x.append(-.5)
        y.append(0.1)
        x.append(0)
        y.append(0.1)
        x.append(0)
        y.append(0)


        self.parent().pt.setData(x,y)
        self.parent().pt2.setData([0,self.tfc + pinNumber*self.spacing + 0.05],[0,0])

    @pyqtSlot()
    def changePinHeight(self, pinNumber):
        self.drawKey()

    @pyqtSlot()
    def changePinNumber(self):
        while self.slidersLayout.count():
            item = self.slidersLayout.takeAt(0)
            self.slidersLayout.removeItem(item)
        val = self.pinNumberSpinBox.value()
        for i in range(10):
            if i < val:
                self.pinSliders[i].show()
                self.slidersLayout.addWidget(self.pinSliders[i])
            else:
                self.pinSliders[i].hide()
                self.slidersLayout.addSpacing(58)
        self.drawKey()

class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.canvas = pg.GraphicsLayoutWidget()
        layout.addWidget(self.canvas,0,0,5,15)
        self.plot = self.canvas.addPlot()
        self.plot.setRange(xRange=(-3,3), yRange=(-2,1))
        self.pt = self.plot.plot(pen='w')
        self.pt2 = self.plot.plot(pen='r', style=Qt.DotLine)

        specs = SpecWidget()
        specs.setMaximumHeight(500)
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
        self.resize(800,1200)

        self.show()
