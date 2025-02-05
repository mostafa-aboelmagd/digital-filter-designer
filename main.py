from PySide6.QtCore import Qt, QTimer, QEvent
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
        self.zero_mode = True   # default: adding a zero on right click unless pole mode is activated
        self.pole_mode = False
        self.zeros = []  # list of tuples for zeros
        self.poles = []  # list of tuples for poles
        self.conjugate_zeros = []
        self.conjugate_poles = []
        self.history = []  # history of (zeros, poles) states for undo/redo
        self.current_history_index = -1  # index for current state in history
        self.data_position = None  # last left-clicked position (used for removal)
        self.dragging_item = None  # used for dragging; stores dict with 'type', 'index', and 'offset'
        
        self.viewports = [self.plot_unitCircle, self.plot_magResponse, self.plot_phaseResponse,
                          self.plot_allPass, self.plot_realtimeInput, self.plot_realtimeFilter, self.plot_mouseInput]
        self.plotTitles = ['Zero/Pole Plot', 'Magnitude Response', 'Phase Response', 'All Pass Response',
                           'Realtime Input', 'Filtered Output', 'Mouse Input']
        self.init_UI()

    def init_UI(self):
        for view, title in zip(self.viewports, self.plotTitles):
            self.customize_plot(view, title)
        self.drawUnitCircle()
        self.connect_signals()
        # Install event filter on the unit circle's scene to enable dragging of markers.
        self.plot_unitCircle.scene().installEventFilter(self)

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
        self.pair_mode_toggle.clicked.connect(self.update_plot)

    def drawUnitCircle(self):
        theta = np.linspace(0, 100, 1000)
        self.plot_unitCircle.plot(np.cos(theta), np.sin(theta), pen='w')

    def toggleUsedMode(self):
        sender = self.sender()
        if sender.objectName() == "btn_addPoles":
            self.pole_mode = True
            self.zero_mode = False
        else:
            self.zero_mode = True
            self.pole_mode = False

    def addZeroOrPole(self, event):
        # Only act on right-click events to add a zero or a pole.
        if event.button() == Qt.RightButton:
            pos = event.scenePos()   # scene (pixel) coordinates
            data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)  # data coordinates
            if self.pole_mode:
                self.poles.append((data_pos.x(), data_pos.y()))
            else:
                self.zeros.append((data_pos.x(), data_pos.y()))
            self.update_plot()  # refresh the plots with new markers
            self.save_state()

    def storeClickedPosition(self, event):
        # This slot saves the data position on a left click if not dragging.
        if event.button() == Qt.LeftButton:
            # Only store if we are not currently dragging an item.
            if self.dragging_item is None:
                pos = event.scenePos()
                data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)
                self.data_position = (data_pos.x(), data_pos.y())

    def removePole(self):
        # Remove a pole if its coordinates are close to the last left-clicked position.
        if self.data_position is None:
            return
        for pole in self.poles:
            if round(pole[0], 1) == round(self.data_position[0], 1) and round(pole[1], 1) == round(self.data_position[1], 1):
                self.poles.remove(pole)
                self.update_plot()
                self.save_state()
                break

    def removeZero(self):
        # Remove a zero if its coordinates are close to the last left-clicked position.
        if self.data_position is None:
            return
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
        # Plot zeros and poles
        for zero in self.zeros:
            self.plot_unitCircle.plot([zero[0]], [zero[1]], pen=None, symbol='o', symbolBrush='r')
        for pole in self.poles:
            self.plot_unitCircle.plot([pole[0]], [pole[1]], pen=None, symbol='x', symbolBrush='b')

        # If the pair mode checkbox is checked, add and plot conjugate pairs.
        if self.pair_mode_toggle.isChecked():
            self.addConjugatePairs()
            for conjugate_pole in self.conjugate_poles:
                self.plot_unitCircle.plot([conjugate_pole[0]], [conjugate_pole[1]], pen=None, symbol='x', symbolBrush='b')
            for conjugate_zero in self.conjugate_zeros:
                self.plot_unitCircle.plot([conjugate_zero[0]], [conjugate_zero[1]], pen=None, symbol='o', symbolBrush='r')

        # Calculate and plot the frequency responses.
        self.plot_frequency_response()

    def addConjugatePairs(self):
        self.conjugate_poles.clear()
        self.conjugate_zeros.clear()
        for pole in self.poles:
            self.conjugate_poles.append((pole[0], -pole[1]))
        for zero in self.zeros:
            self.conjugate_zeros.append((zero[0], -zero[1]))

    def plot_frequency_response(self):
        if not self.zeros and not self.poles:
            self.plot_magResponse.clear()
            self.plot_phaseResponse.clear()
            return

        # Convert zeros and poles into complex numbers.
        zeros = [complex(z[0], z[1]) for z in self.zeros]
        poles = [complex(p[0], p[1]) for p in self.poles]
        # Append conjugates if pair mode is checked.
        if self.pair_mode_toggle.isChecked():
            zeros += [complex(cz[0], cz[1]) for cz in self.conjugate_zeros]
            poles += [complex(cp[0], cp[1]) for cp in self.conjugate_poles]

        b, a = zpk2tf(zeros, poles, 1)
        # Compute frequency response.
        w, h = freqz(b, a, worN=1024)
        magnitude = 20 * np.log10(np.abs(h))
        self.plot_magResponse.clear()
        self.plot_magResponse.plot(w, magnitude, pen='b')
        self.plot_magResponse.setLabel('left', 'Magnitude (dB)')
        self.plot_magResponse.setLabel('bottom', 'Frequency [rad/sample]')

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
        elif self.current_history_index == 0:
            self.poles.clear()
            self.zeros.clear()
            self.current_history_index -=1
            self.update_plot()

    def redo(self):
        if self.current_history_index < len(self.history) - 1:
            self.current_history_index += 1
            self.zeros, self.poles = self.history[self.current_history_index]
            self.update_plot()

    # Event Filter to enable dragging of zeros/poles 
    def eventFilter(self, source, event):
        if source is self.plot_unitCircle.scene():
            # Process mouse press: start drag if left click is close to a marker.
            if event.type() == QEvent.GraphicsSceneMousePress:
                if event.button() == Qt.LeftButton:
                    pos = event.scenePos()
                    data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)
                    threshold = 0.05  # threshold in data coordinates for selecting a marker
                    # Check zeros first.
                    for idx, zero in enumerate(self.zeros):
                        if abs(zero[0] - data_pos.x()) < threshold and abs(zero[1] - data_pos.y()) < threshold:
                            # Store offset so the marker doesn't "jump" to the cursor center.
                            offset = (zero[0] - data_pos.x(), zero[1] - data_pos.y())
                            self.dragging_item = {'type': 'zero', 'index': idx, 'offset': offset}
                            return True  # event handled
                    # Then check poles.
                    for idx, pole in enumerate(self.poles):
                        if abs(pole[0] - data_pos.x()) < threshold and abs(pole[1] - data_pos.y()) < threshold:
                            offset = (pole[0] - data_pos.x(), pole[1] - data_pos.y())
                            self.dragging_item = {'type': 'pole', 'index': idx, 'offset': offset}
                            return True
                        
            # Process mouse move: if dragging, update the marker position.
            elif event.type() == QEvent.GraphicsSceneMouseMove:
                if self.dragging_item is not None:  # if there is already a pressed zero or pole
                    pos = event.scenePos()
                    data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)
                    offset = self.dragging_item['offset']
                    new_point = (data_pos.x() + offset[0], data_pos.y() + offset[1])   # the new position of the held zero/pole that's being updated while moving
                    if self.dragging_item['type'] == 'zero':
                        self.zeros[self.dragging_item['index']] = new_point  # updating the position of the zero being held
                    else:
                        self.poles[self.dragging_item['index']] = new_point
                    self.update_plot()
                    return True
                
            # Process mouse release: finish dragging.
            elif event.type() == QEvent.GraphicsSceneMouseRelease:
                if self.dragging_item is not None:
                    self.dragging_item = None
                    self.save_state()
                    return True
        # For all other events, use the default processing.
        return super().eventFilter(source, event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
