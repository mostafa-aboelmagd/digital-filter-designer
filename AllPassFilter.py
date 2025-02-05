from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QShortcut, QListWidget, QListWidgetItem, QLineEdit, QPushButton
from scipy.signal import freqz, lfilter, zpk2tf
import numpy as np
import pyqtgraph as pg
import pandas as pd
import os
import math

class AllPassFilterDesigner(QMainWindow):
    def __init__(self):
        super(AllPassFilterDesigner, self).__init__()
        self.init_UI()
        
        # Predefined library of all-pass filters
        self.all_pass_library = [
            {"a": 0.5, "zeros": [0.5], "poles": [2]},
            {"a": -0.5, "zeros": [-0.5], "poles": [-2]},
            # Add more predefined filters here
        ]
        
        # Initialize the UI for the all-pass filter library
        self.init_all_pass_library_ui()
    
    def init_UI(self):
        self.setWindowTitle("All-Pass Filter Designer")
        self.setGeometry(100, 100, 800, 600)
        
        self.plot_allPass = pg.PlotWidget(self)
        self.plot_allPass.setGeometry(10, 10, 780, 300)
        
        self.table_coeff = QTableWidget(self)
        self.table_coeff.setGeometry(10, 320, 200, 200)
        self.table_coeff.setColumnCount(1)
        self.table_coeff.setHorizontalHeaderLabels(["Coefficients"])
        
        self.comboBox = QLineEdit(self)
        self.comboBox.setGeometry(220, 320, 100, 30)
        
        self.btn_addCoeff = QPushButton("Add Coefficient", self)
        self.btn_addCoeff.setGeometry(330, 320, 150, 30)
        self.btn_addCoeff.clicked.connect(self.add_coefficient)
        
        self.btn_removeCoeff = QPushButton("Remove Coefficient", self)
        self.btn_removeCoeff.setGeometry(330, 360, 150, 30)
        self.btn_removeCoeff.clicked.connect(self.remove_coefficient)
        
        self.list_enabled_all_pass = QListWidget(self)
        self.list_enabled_all_pass.setGeometry(500, 320, 200, 200)
        self.list_enabled_all_pass.itemChanged.connect(self.on_enabled_all_pass_changed)
    
    def init_all_pass_library_ui(self):
        # Create a list widget to display the all-pass filter library
        self.list_all_pass_library = QListWidget(self)
        self.list_all_pass_library.setGeometry(10, 530, 200, 60)
        
        # Populate the list widget with the predefined all-pass filters
        for filter in self.all_pass_library:
            item = QListWidgetItem(f"a = {filter['a']}")
            self.list_all_pass_library.addItem(item)
        
        # Connect the item selection signal to a slot
        self.list_all_pass_library.itemSelectionChanged.connect(self.on_all_pass_library_selection_changed)
    
    def on_all_pass_library_selection_changed(self):
        # Get the selected all-pass filter
        selected_items = self.list_all_pass_library.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            selected_filter = self.all_pass_library[self.list_all_pass_library.row(selected_item)]
            
            # Visualize the selected all-pass filter
            self.visualize_all_pass_filter(selected_filter)
    
    def visualize_all_pass_filter(self, filter):
        # Visualize the zero-pole combination and phase response of the selected all-pass filter
        zeros = filter["zeros"]
        poles = filter["poles"]
        # Add code to visualize the zeros and poles
        # Add code to calculate and visualize the phase response
    
    def add_coefficient(self):
        # Create a QTableWidgetItem
        coeff_item = QTableWidgetItem(self.comboBox.text())
        coeff_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        coeff_item.setCheckState(Qt.Checked)
        
        # Insert the item into the table widget
        self.table_coeff.insertRow(self.table_coeff.rowCount())
        self.table_coeff.setItem(self.table_coeff.rowCount()-1, 0, coeff_item)
    
    def remove_coefficient(self):
        self.table_coeff.removeRow(self.table_coeff.currentRow())
    
    def on_enabled_all_pass_changed(self, item):
        # Update the filter design based on the enabled/disabled all-pass filters
        self.update_all_pass_filters()
    
    def update_all_pass_filters(self):
        # Get the enabled all-pass filters
        enabled_filters = []
        for i in range(self.list_enabled_all_pass.count()):
            item = self.list_enabled_all_pass.item(i)
            if item.checkState() == Qt.Checked:
                enabled_filters.append(self.all_pass_library[i])
        
        # Update the filter design with the enabled all-pass filters
        # Add code to update the filter design

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = AllPassFilterDesigner()
    MainWindow.show()
    sys.exit(app.exec_())