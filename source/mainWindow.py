import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Create an PyQT4 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QMainWindow()

# Set window size.
w.resize(800, 600)

# Set window title
w.setWindowTitle("Key Designer")

# Show window
w.show()

sys.exit(a.exec_())
