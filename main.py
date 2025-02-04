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
        self.zero_mode = True   # default mode detecting whether to add a zero or pole on right click in the unit circle plot
        self.pole_mode = False
        self.zeros = []  # contains tuples of coordinates of the zeroes we have.
        self.poles = []
        self.history = []  # a list that contains tuples, each tuple contains a list of zeroes and a list of poles at a certain time. It's updated with each plot update.
        self.current_history_index = -1  # it points at the tuple which contains the current zeroes and poles lists 
        self.data_position = None  # a tuple that contains the coordinates of the last left clicked area in the unit circle plot
        self.dragging_item = None
        
        self.viewports = [self.plot_unitCircle, self.plot_magResponse, self.plot_phaseResponse,
                          self.plot_allPass, self.plot_realtimeInput, self.plot_realtimeFilter, self.plot_mouseInput]
        self.plotTitles = ['Zero/Pole Plot', 'Magnitude Response', 'Phase Response', 'All Pass Response','Realtime Input', 'Filtered Output', 'Mouse Input']
        self.init_UI()

    def init_UI(self):
        for view, title in zip(self.viewports, self.plotTitles):
            self.customize_plot(view, title)
        self.drawUnitCircle()
        self.connect_signals()
  
        
    def customize_plot(self, plot, title):
        plot.getPlotItem().showGrid(True, True)
        plot.getPlotItem().setTitle(title)
        plot.setMenuEnabled(False)
        
        
    def connect_signals(self):
   
        self.btn_addPoles.clicked.connect(self.toggleUsedMode)
        self.btn_addZeros.clicked.connect(self.toggleUsedMode)
        self.btn_removePoles.clicked.connect(self.removePole)
        self.btn_RemoveZeros.clicked.connect(self.removeZero)
        self.btn_Swapping.clicked.connect(self.replaceZeroPole)
        self.btn_Undo.clicked.connect(self.undo)
        self.btn_Redo.clicked.connect(self.redo)
        self.btn_removeAll.clicked.connect(self.removeAll)
        self.btn_Remove_all_zeros.clicked.connect(self.removeAllZeros)
        self.btn_Remove_all_poles.clicked.connect(self.removeAllPoles)
        self.plot_unitCircle.scene().sigMouseClicked.connect(self.addZeroOrPole)
        self.plot_unitCircle.scene().sigMouseClicked.connect(self.storeClickedPosition)
        
        
    
    
    def drawUnitCircle(self):
        theta = np.linspace(0, 100, 1000)
        self.plot_unitCircle.plot(np.cos(theta), np.sin(theta), pen = 'w')

    def toggleUsedMode(self):
        sender = self.sender()
        if sender.objectName() == "btn_addPoles":
            self.pole_mode = True
            self.zero_mode = False
        else:
            self.zero_mode = True
            self.pole_mode = False
            
    def addZeroOrPole(self, event):
        # print("entered the add zero or pole method")
        if event.button() == Qt.RightButton:
            # print(f"right click sig recieved ")
            pos = event.scenePos()   # Get the mouse click position in pixel coordinates
            data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)      # Convert the pixel coordinates to data coordinates
            if self.pole_mode == True:
                self.poles.append((data_pos.x(), data_pos.y()))   # add the position of the new pole to the poles array
            else:
                self.zeros.append((data_pos.x(), data_pos.y()))
                
            self.update_plot()   #to place the new pole or zero in the plot
            self.save_state()
                
    def storeClickedPosition(self, event):
        if event.button() == Qt.LeftButton:
            position = event.scenePos()  # position in pixels
            data_position = self.plot_unitCircle.getViewBox().mapSceneToView(position)  # qpoint holding the coordinates of the left clicked position
            self.data_position = (data_position.x(), data_position.y())  # changing the qpoint into a tuple to be easier to deal with
            # print(self.data_position)

    def removePole(self):
        for pole in self.poles:
            if round(pole[0], 1) == round(self.data_position[0], 1) and round(pole[1], 1) == round(self.data_position[1], 1):  # comparing last left clicked x and y coordinates to the coordinates of each pole.
                self.poles.remove(pole)
                self.update_plot()
                self.save_state()
                break
            
    def removeZero(self):
        for zero in self.zeros:
            if round(zero[0], 1) == round(self.data_position[0], 1) and round(zero[1], 1) == round(self.data_position[1], 1): 
                self.zeros.remove(zero)
                self.update_plot()
                self.save_state()
                break
            
    def removeAllPoles(self):
        self.poles.clear()
        self.update_plot()
        self.save_state()
        
    def removeAllZeros(self):
        self.zeros.clear()
        self.update_plot()
        self.save_state()
    
    def removeAll(self):
        self.poles.clear()
        self.zeros.clear()
        self.update_plot()
        self.save_state()

    def replaceZeroPole(self):
        self.zeros, self.poles = self.poles, self.zeros
        self.update_plot()
        self.save_state()

    def update_plot(self):
        self.plot_unitCircle.clear()
        self.drawUnitCircle()
        for zero in self.zeros:
            self.plot_unitCircle.plot([zero[0]], [zero[1]], pen=None, symbol='o', symbolBrush='r')
        for pole in self.poles:
            self.plot_unitCircle.plot([pole[0]], [pole[1]], pen=None, symbol='x', symbolBrush='b')

        # Calculate and plot the magnitude and phase response
        self.plot_frequency_response()

    def plot_frequency_response(self):
        if not self.zeros and not self.poles:
            self.plot_magResponse.clear()
            self.plot_phaseResponse.clear()
            return

        # Convert poles and zeros to transfer function
        zeros = [complex(z[0], z[1]) for z in self.zeros]  # putting the zeroes coordinates in the form of complex numbers
        poles = [complex(p[0], p[1]) for p in self.poles]  # same for poles
       
        b, a = zpk2tf(zeros, poles, 1)  # b: array containing the numrator cooffs of the transfer fn in z domain (b0, b1, b2, ...)
                                        # a: array containing the denomenator cooffs (a0, a1, a2, ...)
        # Calculate frequency response
        w, h = freqz(b, a, worN=1024)     # h: frequency response (transfer fn in w),   w: frequencies at which h is computed
                                          # NOTE: w is put in its real value on the x axis (for example: if we put a
                                          # zero on the unit circle plot at pi/2, we will find that it will be reflected
                                          # at w = 1.5 rad/sample in the mag plot where pi/2 = 3.14/2 = 1.5 nearly)

        # Plot magnitude response
        magnitude = 20 * np.log10(abs(h))
        self.plot_magResponse.clear()
        self.plot_magResponse.plot(w, magnitude, pen='b')
        self.plot_magResponse.setLabel('left', 'Magnitude (dB)')
        self.plot_magResponse.setLabel('bottom', 'Frequency [rad/sample]')

        # Plot phase response
        phase = np.unwrap(np.angle(h))
        self.plot_phaseResponse.clear()
        self.plot_phaseResponse.plot(w, phase, pen='r')
        self.plot_phaseResponse.setLabel('left', 'Phase (radians)')
        self.plot_phaseResponse.setLabel('bottom', 'Frequency [rad/sample]')

    def save_state(self):
        if self.current_history_index < len(self.history) - 1:
            self.history = self.history[:self.current_history_index + 1]
        self.history.append((self.zeros.copy(), self.poles.copy()))
        self.current_history_index += 1

    def undo(self):
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self.zeros, self.poles = self.history[self.current_history_index]
            self.update_plot()

    def redo(self):
        if self.current_history_index < len(self.history) - 1:
            self.current_history_index += 1
            self.zeros, self.poles = self.history[self.current_history_index]
            self.update_plot()

    
            
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())