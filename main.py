# i want tos show the Ui in the MainWindow_ui.py
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from scipy.signal import freqz, lfilter, zpk2tf, filtfilt
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow_ui import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
from scipy.signal import freqz
import pandas as pd
import os
import scipy
import scipy.signal
import math
from numpy import *
from numpy.random import *
from scipy.signal import *
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setupUi(self)
        self.viewports = [self.plot_unitCircle, self.plot_magResponse, self.plot_phaseResponse,
                          self.plot_allPass, self.plot_realtimeInput, self.plot_realtimeFilter, self.plot_mouseInput]
        self.plotTitles = ['Zero/Pole Plot', 'Magnitude Response', 'Phase Response', 'All Pass Response','Realtime Input', 'Filtered Output', 'Mouse Input']
        self.init_UI()

    def customize_plot(self, plot, title):
        plot.getPlotItem().showGrid(True, True)
        plot.getPlotItem().setTitle(title)
        plot.setMenuEnabled(False)

    def init_UI(self):
        # Customize the appearance of the plots using the new function
        for view, title in zip(self.viewports, self.plotTitles):
            self.customize_plot(view, title)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
