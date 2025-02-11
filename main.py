from ast import Not
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from scipy.signal import freqz, lfilter, zpk2tf, filtfilt, lfilter_zi
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow_ui import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import pandas as pd
import os
import scipy
import scipy.signal
import math
from numpy import *
from numpy.random import *
from scipy.signal import *
from save_load_c import *
from filters_lib import *
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
        self.current_history_index = 0  # index for current state in history
        self.data_position = None  # last left-clicked position (used for removal)
        self.dragging_item = None  # used for dragging; stores dict with 'type', 'index', and 'offset'
        self.all_pass_a = 1
        self.allpass_en = False
        self.checked_coeffs = [0.0]
        self.theta = 0.0
        self.colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#800080', '#FF00FF', '#FF1493', '#00FF7F', '#FFD700', '#FF6347', '#48D1CC', '#8A2BE2', '#20B2AA']
        self.total_phase = 0  # Add this line to initialize total_phase
        self.viewports = [self.plot_unitCircle, self.plot_magResponse, self.plot_phaseResponse,
                          self.plot_allPass, self.plot_realtimeInput, self.plot_realtimeFilter, self.plot_mouseInput]
        self.plotTitles = ['Zero/Pole Plot', 'Magnitude Response', 'Phase Response', 'All Pass Response',
                           'Realtime Input', 'Filtered Output', 'Mouse Input']
        self.init_UI()
        self.addEventListeners()

    def init_UI(self):
        for view, title in zip(self.viewports, self.plotTitles):
            self.customize_plot(view, title)
        self.history = [(self.zeros.copy(), self.poles.copy())] 
        self.drawUnitCircle()
        self.connect_signals()
        # Install event filter on the unit circle's scene to enable dragging of markers.
        self.plot_unitCircle.scene().installEventFilter(self)
        self.browsedSignal = None
        self.filteredSignal = None
        self.index = 0
        self.timer = None
        self.speed_slider.setDisabled(True)
        self.speed = 1
        self.userInput = False
        self.b = None
        self.a = None

    def customize_plot(self, plot, title):
        plot.getPlotItem().showGrid(True, True)
        plot.getPlotItem().setTitle(title)
        plot.setMenuEnabled(False)
    
    def addEventListeners(self):
        self.btn_openFile.clicked.connect(self.browseFile)
        self.speed_slider.valueChanged.connect(self.updateFilterSpeed)
        self.plot_mouseInput.setMouseTracking(True)
        self.plot_mouseInput.mouseMoveEvent = self.mouseMoveEvent
        self.btnClr.clicked.connect(self.clearSignal)

    def browseFile(self):
        if self.b is None and self.a is None:
            QMessageBox.critical(self, "Error", "Design Your Filter First Before Browsing A Signal!")
            return
        filePath, _ = QFileDialog.getOpenFileName(self, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)")
        
        if filePath:
            try:
                df = pd.read_csv(filePath, header=None)
                
                if df.shape[1] <= 10000:
                    QMessageBox.critical(self, "Error", "Signal File Must Have Atleast 10000 Points!")
                    return

                self.browsedSignal = df.iloc[0].values  # Get the first row as signal
                self.time = np.arange(len(self.browsedSignal)) * 0.1  # Generate time axis (t = [0, 0.1, 0.2, ...])
                self.filteredSignal = []
                self.speed_slider.setEnabled(True)  # Enable the start button
                self.zi = lfilter_zi(self.b, self.a) * self.browsedSignal[0]
                self.startPlotting()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read CSV: {str(e)}")
    
    def startPlotting(self):
        if self.browsedSignal is None:
            QMessageBox.warning(self, "Error", "No signal loaded!")
            return

        self.index = 0
        self.plot_realtimeInput.clear()
        self.plot_realtimeFilter.clear()

        # Create an empty plot curve
        self.curve = self.plot_realtimeInput.plot([], [], pen="r")
        self.filterCurve = self.plot_realtimeFilter.plot([], [], pen="g")

        # Set up the timer to update every 100 ms (since dt = 0.1 sec)
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateSignalsPlot)
        self.timer.start(100)  # 100 ms update rate

    def updateSignalsPlot(self):
        if self.index >= len(self.browsedSignal):
            self.timer.stop()  # Stop updating when all data is shown
            return
        
        # Process and filter all skipped points between the current index and the previous index
        startIndex = self.index
        endIndex = self.index + self.speed
        if endIndex  > len(self.browsedSignal):
            endIndex = len(self.browsedSignal)
        
        # Apply filter to each skipped point
        for i in range(startIndex, endIndex):
            currentPoint = np.array([self.browsedSignal[i]])
            filteredOutput, self.zi = lfilter(self.b, self.a, currentPoint, zi=self.zi)
            filteredOutput = np.real(filteredOutput)
            self.filteredSignal.append(filteredOutput[0])

        # Update the plot with the new data up to the current index
        self.curve.setData(self.time[:endIndex], self.browsedSignal[:endIndex])
        self.filterCurve.setData(self.time[:endIndex], self.filteredSignal[:endIndex])

        # Increment the index for the next iteration
        self.index = endIndex

    def updateFilterSpeed(self):
        self.speed = self.speed_slider.value()
        self.lbl_speed.setText(f"Speed: {self.speed} Points/Second ")
    
    def mouseMoveEvent(self, event):
        if self.browsedSignal is None and (self.b is not None or self.a is not None):
            self.userInput = True
            self.curve = self.plot_realtimeInput.plot([], [], pen="r")
            self.filterCurve = self.plot_realtimeFilter.plot([], [], pen="g")
            self.browsedSignal = []
            self.filteredSignal = []
            self.time = []
            self.zi = None
            self.startTime = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000

        if self.userInput:
            y = event.position().y()  # Get mouse Y position
            invertedY = self.plot_mouseInput.height() - y  # Invert Y-axis
            currentTime = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000 - self.startTime  # Calculate time elapsed since start

            # Append new data points
            self.time.append(currentTime)
            self.browsedSignal.append(invertedY)
            if self.zi is None:
                self.zi = lfilter_zi(self.b, self.a) * self.browsedSignal[0]

            currentPoint = np.array([invertedY])
            filteredOutput, self.zi = lfilter(self.b, self.a, currentPoint, zi=self.zi)
            filteredOutput = np.real(filteredOutput)
            self.filteredSignal.append(filteredOutput[0])

            # Update the plot
            self.curve.setData(self.time, self.browsedSignal)
            self.filterCurve.setData(self.time, self.filteredSignal)
    
    def clearSignal(self):
        self.plot_realtimeInput.clear()
        self.plot_realtimeFilter.clear()
        self.index = 0
        if self.browsedSignal is not None and not self.userInput:
            self.timer.stop()
        self.speed_slider.setDisabled(True)
        self.browsedSignal = None
        self.filteredSignal = None
        self.userInput = False

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
        self.pair_mode_toggle.clicked.connect(self.update_plot)
        self.btn_addCoeff.clicked.connect(self.add_coefficient)
        self.btn_removeCoeff.clicked.connect(self.remove_coefficient)
        self.table_coeff.itemChanged.connect(self.update_plot_allpass)
        self.all_pass_enable.stateChanged.connect(self.toggle_all_pass)
        self.theta_slider.valueChanged.connect(self.update_theta)
        self.btn_Export_Zero_Pole.clicked.connect(self.exportZeroPole)
        self.btn_Import_Zero_Pole.clicked.connect(self.importZeroPole)
        self.lib_combobox.currentIndexChanged.connect(self.apply_filter)
        self.type_combobox.currentIndexChanged.connect(self.apply_filter)
    
    def apply_filter(self):
        self.type_combobox.setDisabled(False)
        filter_ind = self.lib_combobox.currentIndex()
        sampling_frequency = max(self.sampling_frequency_spinbox.value(), 1)
        cutoff = max(self.cut_off_spinbox.value(), 0.001)
        cutoff = min(cutoff, (sampling_frequency / 2) - 0.001)
        order = max(self.order_spinbox.value(), 1)

        
        if self.type_combobox.currentText() == 'bandpass':
            freq3db = [0.001, cutoff]
        else:
            freq3db = cutoff
            
        if filter_ind < 5:
            b,a = FilterDesigner.design_iir(self.lib_combobox.currentText(), self.type_combobox.currentText(), order, freq3db, sampling_frequency)
        elif filter_ind == 5:
            b,a = FilterDesigner.design_fir(self.type_combobox.currentText(), 65, freq3db, sampling_frequency)
        elif filter_ind == 6:
            freq3db = cutoff
            b,a = FilterDesigner.design_gaussian(31, freq3db, sampling_frequency)
            # make the type combobox disabled and set it to lowpass
            self.type_combobox.setDisabled(True)
            self.type_combobox.setCurrentIndex(0)
        
        if b is not None and a is not None:
            zeros, poles, k = tf2zpk(b, a)
            self.zeros = [(z.real, z.imag) for z in zeros]
            self.poles = [(p.real, p.imag) for p in poles]
            self.update_plot()
            self.save_state()
     



    def exportZeroPole(self):
        zeros = self.zeros + (self.conjugate_zeros or [])
        poles = self.poles + (self.conjugate_poles or [])
        zeros = [complex(z[0], z[1]) for z in zeros]
        poles = [complex(p[0], p[1]) for p in poles]
        b, a = zpk2tf(zeros, poles, 1)
        save_filter_to_csv(zeros, poles, "filter_coef.csv")
        export_filter_to_c(b, a, "filter_direct.c", realization='direct')
        export_filter_to_c(b, a, "filter_cascade.c", realization='cascade')
    
    def importZeroPole(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Zero-Pole File", "", "CSV Files (*.csv)")
        if filename:
            zeros, poles = load_filter_from_csv(filename)
            zeros = [complex(row.strip("()")) for row in zeros]
            poles = [complex(row.strip("()")) for row in poles]
            self.zeros = [(z.real, z.imag) for z in zeros]
            self.poles = [(p.real, p.imag) for p in poles]
            self.update_plot()
            self.save_state()

        
    
    
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
            print("data position is none")
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
            self.b = None
            self.a = None
            self.clearSignal()
            return

        # Convert zeros and poles into complex numbers.
        zeros = [complex(z[0], z[1]) for z in self.zeros]
        poles = [complex(p[0], p[1]) for p in self.poles]
        # Append conjugates if pair mode is checked.
        if self.pair_mode_toggle.isChecked():
            zeros += [complex(cz[0], cz[1]) for cz in self.conjugate_zeros]
            poles += [complex(cp[0], cp[1]) for cp in self.conjugate_poles]

        self.b, self.a = zpk2tf(zeros, poles, 1)
        # Compute frequency response.
        w, h = freqz(self.b, self.a, worN=1024)
        magnitude = 20 * np.log10(np.abs(h)+1e-6)
        self.plot_magResponse.clear()
        self.plot_magResponse.plot(w, magnitude, pen='r')
        self.plot_magResponse.setLabel('left', 'Magnitude (dB)')
        self.plot_magResponse.setLabel('bottom', 'Frequency [rad/sample]')

        phase = np.unwrap(np.angle(h))
        self.plot_phaseResponse.clear()
        self.plot_phaseResponse.plot(w, phase, pen='r', name=' Original Phase Response')
        self.plot_phaseResponse.setLabel('left', 'Phase (radians)')
        self.plot_phaseResponse.setLabel('bottom', 'Frequency [rad/sample]')
        # print("W : " , w)
        # print("H : " , h)

        # Plot all-pass filter phase response if enabled
        if self.allpass_en:
            _, _, z_allpass, p_allpass = self.get_all_pass_filter()
            w, h = freqz(np.poly(z_allpass), np.poly(p_allpass))
            phase_allpass = self.fix_phase(h)
            self.plot_phaseResponse.plot(w, phase_allpass, pen='y', name='AllPass Phase Response')
            self.plot_phaseResponse.addLegend()
        
        if self.userInput:
            self.clearSignal()
        if self.browsedSignal is not None:
            self.startPlotting()

    def save_state(self):
    
        if self.current_history_index < len(self.history) - 1:
            self.history = self.history[:self.current_history_index + 1]
        # Save new state
        new_state = (self.zeros.copy(), self.poles.copy())
        # Only save if different from current state
        if new_state != self.history[self.current_history_index]:
            self.history.append(new_state)
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


    # Event Filter to enable dragging of zeros/poles 
    def eventFilter(self, source, event):
        if source is self.plot_unitCircle.scene():
            # Process mouse press: start drag if left click is close to a marker.
            if event.type() == QEvent.GraphicsSceneMousePress:
                if event.button() == Qt.LeftButton:
                    pos = event.scenePos()
                    data_pos = self.plot_unitCircle.getViewBox().mapSceneToView(pos)
                    self.data_position = (data_pos.x(), data_pos.y())
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
        self.save_state()
        return super().eventFilter(source, event)
        # self.save_state()
    

    
        
   
    def add_coefficient(self):
        # Create a QTableWidgetItem
        coeff_item = QTableWidgetItem(self.comboBox.currentText())
        coeff_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        coeff_item.setCheckState(Qt.CheckState.Checked)
        
        # Insert the item into the table widget
        self.table_coeff.insertRow(self.table_coeff.rowCount())
        self.table_coeff.setItem(self.table_coeff.rowCount()-1, 0, coeff_item)
        self.update_plot_allpass()
        self.update_response_plots()
        # Undo and Redo buttons
        self.save_state()

        
        
    # Removes the selected row from the table widget
    def remove_coefficient(self):
        self.table_coeff.removeRow(self.table_coeff.currentRow()) 
        # delete the corresponding coefficient from the list of coefficients as well the ploted all pass filter
        self.update_plot_allpass()
        self.update_response_plots()
        # Undo and Redo buttons
        self.save_state()


     
    def get_all_pass_filter(self):
        self.checked_coeffs = [0.0]  # List to hold the selected coefficient values
        
        for row in range(self.table_coeff.rowCount()):
            item = self.table_coeff.item(row, 0) 
            if item.checkState() == Qt.CheckState.Checked:
                self.checked_coeffs.append(float(item.text()))  
        
        if not self.allpass_en:
            self.checked_coeffs = [0.0]

        self.all_pass_zeros = self.zeros.copy()
        self.all_pass_poles = self.poles.copy()

        w, all_pass_phs = None, None
        self.plot_allPass.clear()

        for i in range(len(self.checked_coeffs)):
            a = self.checked_coeffs[i]

            if a == 1:
                a = 0.99999999
            a = complex(a, 0)
            
            # Check if denominator is not zero before performing division
            if np.abs(a) > 0:
                a_conj = 1 / np.conj(a)

                # Use theta as an input parameter to set location in the graph
                zero = a_conj * np.exp(1j * self.theta)
                pole = a * np.exp(1j * self.theta)

                # b_allpass, a_allpass = zpk2tf([zero], [pole], 1)
                # b_allpass, a_allpass = [-np.conj(zero), 1.0], [1.0, -pole]

                # w, h = freqz([-np.conj(zero), 1.0], [1.0, -pole])

                # self.plot_allPass.plot(w, np.unwrap(np.angle(h)), pen='g', name=f'All pass {a.real}')
                # self.plot_allPass.setLabel('left', 'All Pass Phase', units='radians')

                w, h = freqz(np.poly((zero.real, zero.imag)), np.poly((pole.real, pole.imag)))
                self.frequencies, self.phase_response = w, self.fix_phase(h)
                self.plot_allPass.plot(self.frequencies, self.phase_response, pen=self.colors[i % len(self.colors)] , name=f'All pass {pole.real}')
                if all_pass_phs is None:
                    all_pass_phs = np.angle(h)
                else:
                    all_pass_phs = np.add(all_pass_phs, np.angle(h))         
                
                # Add points to lists
                self.all_pass_poles.append((pole.real, pole.imag))
                self.all_pass_zeros.append((zero.real, zero.imag))
        
        self.plot_unitCircle.clear()
        self.drawUnitCircle()
        for zero in self.all_pass_zeros:
            self.plot_unitCircle.plot([zero[0]], [zero[1]], pen=None, symbol='o', symbolBrush='r')
        for pole in self.all_pass_poles:
            self.plot_unitCircle.plot([pole[0]], [pole[1]], pen=None, symbol='x', symbolBrush='b')

        # for zero, pole in zip(self.all_pass_zeros, self.all_pass_poles):
            
        #         w, h = freqz(np.poly(zero), np.poly(pole))
        #         self.frequencies, self.phase_response = w, self.fix_phase(h)
        #         self.plot_allPass.plot(self.frequencies, self.phase_response, pen=self.colors[i % len(self.colors)] , name=f'All pass {pole[0]}')

        if len(self.checked_coeffs) > 1:
            self.plot_allPass.plot(w, all_pass_phs, pen=self.colors[-1], name='All pass Total')
        self.plot_allPass.addLegend()

        # Combine zeros and poles
        z_allpass = np.array([complex(z[0], z[1]) for z in self.all_pass_zeros])
        p_allpass = np.array([complex(p[0], p[1]) for p in self.all_pass_poles])

        z = np.array([complex(z[0], z[1]) for z in self.zeros])
        p = np.array([complex(p[0], p[1]) for p in self.poles])

        return z, p, z_allpass, p_allpass

    def update_plot_allpass(self):
        self.update_response_plots()
        _, _, z, p = self.get_all_pass_filter()
        # Calculate frequency response
        w, h = freqz(np.poly(z), np.poly(p))
        self.phase_response = self.fix_phase(h)

    def fix_phase(self, h):
        phase_response_rad = np.unwrap(np.angle(h))
        return phase_response_rad

    def toggle_all_pass(self):
        self.allpass_en = not self.allpass_en
        self.update_plot_allpass()
        self.update_response_plots()

    def update_response_plots(self):
        # Combine zeros and poles
        z, p, z_allpass, p_allpass = self.get_all_pass_filter()

        # Calculate frequency response
        w, h = freqz(np.poly(z), np.poly(p))

        # Update class attributes
        self.frequencies, self.mag_response, self.phase_response = w, np.abs(h), self.fix_phase(h)

        # Plot magnitude response
        self.plot_response(self.plot_magResponse, self.frequencies, self.mag_response, pen='r', label='Magnitude', units='Linear', unit_bot="Radians", name="AllPass magnitude Response")

        # Plot phase response
        self.plot_response(self.plot_phaseResponse, self.frequencies, self.phase_response, pen='r', label='Phase', units='Degrees', unit_bot="Radians", name="Normal Phase Response")
        
        w, h = freqz(np.poly(z_allpass), np.poly(p_allpass))
        self.frequencies, self.mag_response, self.phase_response = w, np.abs(h), self.fix_phase(h)
        self.plot_phaseResponse.plot(x=self.frequencies, y=self.phase_response, pen='y', name="AllPass Phase Response")
        self.b, self.a = zpk2tf(z_allpass, p_allpass, 1)

        # Plot magnitude response
        self.plot_response(self.plot_magResponse, self.frequencies, self.mag_response, pen='r', label='Magnitude all pass', units='Linear', unit_bot="Radians", name="AllPass magnitude Response")
        #self.filteredSignal[:self.index] = np.real(lfilter(self.b, self.a, self.browsedSignal[:self.index]))

    def plot_response(self, plot, x, y, pen, label, units, unit_bot, name=""):
        plot.clear()
        plot.plot(x, y, pen=pen, name=name)
        plot.setLabel('left', label, units=units)
        plot.setLabel('bottom', label, units=unit_bot)
        self.plot_phaseResponse.addLegend()

    def update_theta(self, value):
        self.theta = np.deg2rad(value)
        if self.allpass_en and len(self.checked_coeffs) > 1:
            self.update_plot_allpass()
        self.update_plot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
