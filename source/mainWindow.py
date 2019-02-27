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
        self.tfcSpinBox.setValue(.2)

        self.tfcSlider = QSlider(Qt.Horizontal)
        self.tfcSlider.setMinimum(0)
        self.tfcSlider.setMaximum(1000)
        self.tfcSlider.setValue(200)

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
        self.spacingSpinBox.setValue(.2)

        self.spacingSlider = QSlider(Qt.Horizontal)
        self.spacingSlider.setMinimum(0)
        self.spacingSlider.setMaximum(1000)
        self.spacingSlider.setValue(200)

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
        self.pinIncrementSpinBox.setRange(0., 1.)
        self.pinIncrementSpinBox.setSingleStep(.001)
        self.pinIncrementSpinBox.setDecimals(3)
        self.pinIncrementSpinBox.setValue(.2)

        self.pinIncrementSlider = QSlider(Qt.Horizontal)
        self.pinIncrementSlider.setMinimum(0)
        self.pinIncrementSlider.setMaximum(1000)
        self.pinIncrementSlider.setValue(200)

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
        self.pinNumberSpinBox.setValue(10)
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
        for i in range(pinNumber):
            x.append(tfc + i*spacing - 0.05)
            y.append(-increment*self.pinSliders[i].value())
            x.append(tfc + i*spacing + 0.05)
            y.append(-increment*self.pinSliders[i].value())

        #last point
        lp = [x[-1],y[-1]]
        lp[0] = lp[0] + spacing

        self.parent().pt.setData(x,y)

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
        self.plot.setRange(xRange=(-1,3), yRange=(-2,1))
        self.pt = self.plot.plot(pen='w')

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
