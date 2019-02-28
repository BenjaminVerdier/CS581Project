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

        self.initTfc()
        self.initSpacing()
        self.initPinIncrement()
        self.initBittingSpecs()

        #TODO: add sliders and spinners for that.
        #TODO: create function to add slider and spinner with string tag instead of copy pasting the same function everytime
        self.keyHeight = .335
        self.keyLength = 2
        self.macs = 7
        self.rootCut = .031

        self.show()

    @pyqtSlot()
    def changeSliderValue(self, spinner, slider):
        slider.setValue(int(spinner.value() * 1000))
        self.drawKey()

    @pyqtSlot()
    def changeSpinnerValue(self, spinner, slider):
        spinner.setValue(slider.value() / 1000)
        self.drawKey()

    def initTfc(self):
        # Distance to first cut
        # slider + spinner
        tfcLayout = QVBoxLayout()

        self.tfcSpinBox = QDoubleSpinBox()
        self.tfcSpinBox.setRange(0., 1.)
        self.tfcSpinBox.setSingleStep(.001)
        self.tfcSpinBox.setDecimals(3)
        self.tfcSpinBox.setValue(.231)

        self.tfcSlider = QSlider(Qt.Horizontal)
        self.tfcSlider.setMinimum(0)
        self.tfcSlider.setMaximum(1000)
        self.tfcSlider.setValue(231)

        self.tfcSpinBox.valueChanged.connect(lambda: self.changeSliderValue(self.tfcSpinBox, self.tfcSlider))
        self.tfcSlider.valueChanged.connect(lambda: self.changeSpinnerValue(self.tfcSpinBox, self.tfcSlider))
        # Label
        tfcLabel = QLabel("Distance to first cut (inches):")

        tfcLayout.addWidget(self.tfcSpinBox)
        tfcLayout.addWidget(self.tfcSlider)

        superLayout = QHBoxLayout()

        superLayout.addWidget(tfcLabel)
        superLayout.addSpacing(50)
        superLayout.addLayout(tfcLayout)

        self.vertical.addLayout(superLayout)

    def initSpacing(self):
        # Distance to first cut
        # slider + spinner
        spacingLayout = QVBoxLayout()

        self.spacingSpinBox = QDoubleSpinBox()
        self.spacingSpinBox.setRange(0., 1.)
        self.spacingSpinBox.setSingleStep(.001)
        self.spacingSpinBox.setDecimals(3)
        self.spacingSpinBox.setValue(.156)

        self.spacingSlider = QSlider(Qt.Horizontal)
        self.spacingSlider.setMinimum(0)
        self.spacingSlider.setMaximum(1000)
        self.spacingSlider.setValue(156)

        self.spacingSpinBox.valueChanged.connect(lambda: self.changeSliderValue(self.spacingSpinBox, self.spacingSlider))
        self.spacingSlider.valueChanged.connect(lambda: self.changeSpinnerValue(self.spacingSpinBox, self.spacingSlider))
        # Label
        spacingLabel = QLabel("Distance between cuts (inches):")

        spacingLayout.addWidget(self.spacingSpinBox)
        spacingLayout.addWidget(self.spacingSlider)

        superLayout = QHBoxLayout()

        superLayout.addWidget(spacingLabel)
        superLayout.addSpacing(28)
        superLayout.addLayout(spacingLayout)

        self.vertical.addLayout(superLayout)

    def initPinIncrement(self):
        # Distance to first cut
        # slider + spinner
        pinIncrementWidget = QWidget()
        pinIncrementLayout = QVBoxLayout()

        self.pinIncrementSpinBox = QDoubleSpinBox()
        self.pinIncrementSpinBox.setRange(0., .2)
        self.pinIncrementSpinBox.setSingleStep(.001)
        self.pinIncrementSpinBox.setDecimals(3)
        self.pinIncrementSpinBox.setValue(.015)

        self.pinIncrementSlider = QSlider(Qt.Horizontal)
        self.pinIncrementSlider.setMinimum(0)
        self.pinIncrementSlider.setMaximum(200)
        self.pinIncrementSlider.setValue(15)

        self.pinIncrementSpinBox.valueChanged.connect(lambda: self.changeSliderValue(self.pinIncrementSpinBox, self.pinIncrementSlider))
        self.pinIncrementSlider.valueChanged.connect(lambda: self.changeSpinnerValue(self.pinIncrementSpinBox, self.pinIncrementSlider))
        # Label
        pinIncrementLabel = QLabel("Pin height increment (inches):")

        pinIncrementLayout.addWidget(self.pinIncrementSpinBox)
        pinIncrementLayout.addWidget(self.pinIncrementSlider)

        superLayout = QHBoxLayout()

        superLayout.addWidget(pinIncrementLabel)
        superLayout.addSpacing(45)
        superLayout.addLayout(pinIncrementLayout)

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
        tfc = self.tfcSpinBox.value()
        increment = self.pinIncrementSpinBox.value()
        spacing = self.spacingSpinBox.value()
        pinNumber = self.pinNumberSpinBox.value()

        x = [0]
        y = [0]
        depths = []
        for i in range(pinNumber):
            x.append(tfc + i*spacing - self.rootCut/2)
            y.append(-increment*self.pinSliders[i].value())
            x.append(tfc + i*spacing + self.rootCut/2)
            y.append(-increment*self.pinSliders[i].value())
            depths.append(increment*self.pinSliders[i].value())

        #Bottom part
        lp = [x[-1],-min(max(depths)+self.macs, 9*increment)]
        lp[0] = lp[0] + spacing
        x.append(lp[0])
        y.append(lp[1])
        x.append(lp[0])
        y.append(-10*increment)
        x.append(0)
        y.append(-10*increment)

        x.append(0)
        y.append(-self.keyHeight + .1)
        x.append(tfc+2*spacing)
        y.append(-self.keyHeight + .1)
        x.append(tfc+2*spacing)
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
        self.parent().pt2.setData([0,tfc + pinNumber*spacing + 0.05],[0,0])

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
