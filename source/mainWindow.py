import sys
#from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SpecWidget(QWidget):

    def __init__(self):
        super(SpecWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.initTfc()
        self.initSpacing()
        self.initPinIncrement()
        self.initBittingSpecs()

        self.show()

    @pyqtSlot()
    def changeSliderValue(self, spinner, slider):
        slider.setValue(int(spinner.value() * 1000))

    @pyqtSlot()
    def changeSpinnerValue(self, spinner, slider):
        spinner.setValue(slider.value() / 1000)

    def initTfc(self):
        # Distance to first cut
        # slider + spinner
        tfcWidget = QWidget()
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

        tfcLayout.addWidget(self.tfcSpinBox)
        tfcLayout.addWidget(self.tfcSlider)

        tfcWidget.setLayout(tfcLayout)
        # Label
        tfcLabel = QLabel("Distance to first cut (inches)")
        self.grid.addWidget(tfcLabel, 0,0)
        self.grid.addWidget(tfcWidget, 0,1)

    def initSpacing(self):
        # Distance to first cut
        # slider + spinner
        spacingWidget = QWidget()
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

        spacingLayout.addWidget(self.spacingSpinBox)
        spacingLayout.addWidget(self.spacingSlider)

        spacingWidget.setLayout(spacingLayout)
        # Label
        spacingLabel = QLabel("Distance between cuts (inches)")
        self.grid.addWidget(spacingLabel, 1,0)
        self.grid.addWidget(spacingWidget, 1,1)

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

        pinIncrementLayout.addWidget(self.pinIncrementSpinBox)
        pinIncrementLayout.addWidget(self.pinIncrementSlider)

        pinIncrementWidget.setLayout(pinIncrementLayout)
        # Label
        pinIncrementLabel = QLabel("Pin height increment (inches)")
        self.grid.addWidget(pinIncrementLabel, 2,0)
        self.grid.addWidget(pinIncrementWidget, 2,1)

    def initBittingSpecs(self):
        bittingWidget = QWidget()
        layout = QVBoxLayout()

        self.pinNumberSpinBox = QSpinBox()
        self.pinNumberSpinBox.setRange(1,10)
        self.pinNumberSpinBox.setSingleStep(1)
        self.pinNumberSpinBox.setValue(1)
        self.pinNumberSpinBox.valueChanged.connect(self.changePinNumber)

        self.slidersLayout = QHBoxLayout()
        self.pinSliders = [QSlider(Qt.Vertical)]
        for i in range(len(self.pinSliders)):
            self.pinSliders[i].setMinimum(0)
            self.pinSliders[i].setMaximum(9)
            self.pinSliders[i].setTickPosition(QSlider.TicksLeft)
            self.pinSliders[i].setTickInterval(1)
            #TODO: add label for pin position underneath the sliders
            self.pinSliders[i].valueChanged.connect(lambda: self.changePinHeight(i))
            self.slidersLayout.addWidget(self.pinSliders[i])

        layout.addWidget(self.pinNumberSpinBox)
        layout.addLayout(self.slidersLayout)

        bittingWidget.setLayout(layout)


        self.grid.addWidget(bittingWidget, 3,0,25,2)

    @pyqtSlot()
    def changePinHeight(self, pinNumber):
        print("This is slider number " + str(pinNumber))

    @pyqtSlot()
    def changePinNumber(self):
        val = self.pinNumberSpinBox.value()
        if len(self.pinSliders) < val:
            for i in range(len(self.pinSliders), val):
                print("Pouet")
                pin = QSlider(Qt.Vertical)
                pin.setMinimum(0)
                pin.setMaximum(9)
                pin.setTickPosition(QSlider.TicksLeft)
                pin.setTickInterval(1)
                #TODO: add label for pin position underneath the sliders
                pin.valueChanged.connect(lambda: self.changePinHeight(i))
                self.pinSliders.append(pin)
                self.slidersLayout.addWidget(pin)
        else:
            for i, pin in enumerate(self.pinSliders):
                if i >= val:
                    pin.hide()
                else:
                    pin.show()

class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        specs = SpecWidget()
        layout.addWidget(specs)

        specs2 = SpecWidget()
        layout.addWidget(specs2)

        self.show()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        mw = MainWidget()
        self.setCentralWidget(mw)
        self.setWindowTitle('Key Designer')
        #self.resize(800,600)

        self.show()
