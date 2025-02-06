from PySide6.QtCore import Qt, QTimer
from PySide6 import QtWidgets, QtCore
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
        self.viewports = [self.plot_unitCircle, self.plot_magResponse, self.plot_phaseResponse,
                          self.plot_allPass, self.plot_realtimeInput, self.plot_realtimeFilter, self.plot_mouseInput]
        self.plotTitles = ['Zero/Pole Plot', 'Magnitude Response', 'Phase Response', 'All Pass Response','Realtime Input', 'Filtered Output', 'Mouse Input']
        self.init_UI()
        self.addEventListeners()

    def customize_plot(self, plot, title):
        plot.getPlotItem().showGrid(True, True)
        plot.getPlotItem().setTitle(title)
        plot.setMenuEnabled(False)

    def init_UI(self):
        # Customize the appearance of the plots using the new function
        for view, title in zip(self.viewports, self.plotTitles):
            self.customize_plot(view, title)
        self.browsedSignal = None
        self.index = 0
        self.timer = None
        self.speed_slider.setDisabled(True)
        self.speed = 1
        self.userInput = False
    
    def addEventListeners(self):
        self.btn_openFile.clicked.connect(self.browseFile)
        self.speed_slider.valueChanged.connect(self.updateFilterSpeed)
        self.plot_mouseInput.setMouseTracking(True)
        self.plot_mouseInput.mouseMoveEvent = self.mouseMoveEvent
        self.btnClr.clicked.connect(self.clearSignal)

    def browseFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)")
        
        if filePath:
            try:
                df = pd.read_csv(filePath, header=None)
                
                if df.shape[1] <= 10000:
                    QMessageBox.critical(self, "Error", "Signal file must have atleast 10000 points!")
                    return

                self.browsedSignal = df.iloc[0].values  # Get the first row as signal
                self.time = np.arange(len(self.browsedSignal)) * 0.1  # Generate time axis (t = [0, 0.1, 0.2, ...])
                self.speed_slider.setEnabled(True)  # Enable the start button
                self.startPlotting()
                #yLimit = max(np.abs(self.browsedSignal))
                #signalFreq = self.calculate_frequency(self.browsedSignal, yLimit - 0.3)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read CSV: {str(e)}")
    
    def startPlotting(self):
        if self.browsedSignal is None:
            QMessageBox.warning(self, "Error", "No signal loaded!")
            return

        self.index = 0
        self.plot_realtimeInput.clear()

        # Create an empty plot curve
        self.curve = self.plot_realtimeInput.plot([], [], pen="r")

        # Set up the timer to update every 100 ms (since dt = 0.1 sec)
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(100)  # 100 ms update rate

    def updatePlot(self):
        if self.index >= len(self.browsedSignal):
            self.timer.stop()  # Stop updating when all data is shown
            return
        
        # Display more points as speed increases
        self.index += self.speed  
        if self.index >= len(self.browsedSignal):
            self.index = len(self.browsedSignal)  # Prevent overshooting

        # Update the plot with new data
        self.curve.setData(self.time[:self.index], self.browsedSignal[:self.index])


    def calculate_frequency(self, signal, threshold):
        peaks = []
        for i in range(len(signal)):
            if i > 0 and i < len(signal) - 1:
                if signal[i] > signal[i - 1] and signal[i] > signal[i + 1] and signal[i] > threshold:
                    peaks.append(i)

        currSignalTime = np.linspace(0, 1, 1000)
        cycleTimes = []
        for i in range(len(peaks) - 1, 0, -1):
            cycleTimes.append(currSignalTime[peaks[i]] - currSignalTime[peaks[i - 1]])
        
        periodicTime = np.average(cycleTimes)

        return round(1 / periodicTime)

    def updateFilterSpeed(self):
        self.speed = self.speed_slider.value()
        self.lbl_speed.setText(f"Speed: {self.speed} Points/Second ")
    
    def mouseMoveEvent(self, event):
        if self.browsedSignal is None:
            self.userInput = True
            self.curve = self.plot_realtimeInput.plot([], [], pen="r")
            self.browsedSignal = []
            self.time = []
            self.startTime = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000

        if self.userInput:
            y = event.pos().y()  # Get mouse Y position
            invertedY = self.plot_mouseInput.height() - y  # Invert Y-axis
            currentTime = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000 - self.startTime  # Calculate time elapsed since start

            # Append new data points
            self.time.append(currentTime)
            self.browsedSignal.append(invertedY)

            # Update the plot
            self.curve.setData(self.time, self.browsedSignal)
    
    def clearSignal(self):
        self.plot_realtimeInput.clear()
        self.plot_realtimeFilter.clear()
        self.index = 0
        self.timer.stop()
        self.speed_slider.setDisabled(True)
        self.browsedSignal = None
        self.userInput = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
