# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1294, 942)

        MainWindow.setStyleSheet("""
    #centralwidget {
        background: #000000;
    }
    
    QWidget {
        background: #000000;
        color: #E7EBF0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    QGroupBox {
        background: #000000;
        border: 2px solid #3399FF;
        border-radius: 8px;
        margin-top: 1em;
        font-size: 14px;
        font-weight: bold;
    }
    
    QGroupBox::title {
        color: #3399FF;
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
    }
    
    QPushButton {
        background: #000000;
        border: 2px solid #3399FF;
        border-radius: 4px;
        padding: 5px 15px;
        color: #3399FF;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background: #1E4976;
        border-color: #66B2FF;
    }
    
    QPushButton:pressed {
        background: #132F4C;
    }
    
    QComboBox {
        background: #000000;
        border: 2px solid #3399FF;
        border-radius: 4px;
        padding: 5px;
        color: #3399FF;
    }
    
    QComboBox:hover {
        border-color: #66B2FF;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QComboBox::down-arrow {
        image: url(down_arrow.png);
        width: 12px;
        height: 12px;
    }
    
    QSlider::groove:horizontal {
        border: 1px solid #3399FF;
        height: 8px;
        background: #000000;
        margin: 2px 0;
        border-radius: 4px;
    }
    
    QSlider::handle:horizontal {
        background: #3399FF;
        border: 1px solid #3399FF;
        width: 18px;
        margin: -6px 0;
        border-radius: 9px;
    }
    
    QSlider::handle:horizontal:hover {
        background: #66B2FF;
        border-color: #66B2FF;
    }
    
    QCheckBox {
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    
    QCheckBox::indicator:unchecked {
        border: 2px solid #3399FF;
        border-radius: 4px;
        background: #000000;
    }
    
    QCheckBox::indicator:checked {
        border: 2px solid #3399FF;
        border-radius: 4px;
        background: #3399FF;
    }
    
    PlotWidget {
        border: 2px solid #3399FF;
        border-radius: 8px;
        background: #000000;
    }
    
    QTableWidget {
        gridline-color: #3399FF;
        border: 2px solid #3399FF;
        border-radius: 4px;
        selection-background-color: #1E4976;
    }
""")
        
    #     MainWindow.setStyleSheet("""
    #     #centralwidget {
    #         background: #0A1929;
    #     }
        
    #     QWidget {
    #         background: #132F4C;
    #         color: #E7EBF0;
    #         font-family: 'Segoe UI', sans-serif;
    #     }
        
    #     QGroupBox {
    #         background: #0A1929;
    #         border: 2px solid #3399FF;
    #         border-radius: 8px;
    #         margin-top: 1em;
    #         font-size: 14px;
    #         font-weight: bold;
    #     }
        
    #     QGroupBox::title {
    #         color: #66B2FF;
    #         subcontrol-origin: margin;
    #         subcontrol-position: top center;
    #         padding: 0 5px;
    #     }
        
    #     QPushButton {
    #         background: #1E4976;
    #         border: 2px solid #3399FF;
    #         border-radius: 4px;
    #         padding: 5px 15px;
    #         color: #E7EBF0;
    #         font-weight: bold;
    #     }
        
    #     QPushButton:hover {
    #         background: #265D97;
    #         border-color: #66B2FF;
    #     }
        
    #     QPushButton:pressed {
    #         background: #132F4C;
    #     }
        
    #     QComboBox {
    #         background: #1E4976;
    #         border: 2px solid #3399FF;
    #         border-radius: 4px;
    #         padding: 5px;
    #         color: #E7EBF0;
    #     }
        
    #     QComboBox:hover {
    #         border-color: #66B2FF;
    #     }
        
    #     QComboBox::drop-down {
    #         border: none;
    #     }
        
    #     QComboBox::down-arrow {
    #         image: url(down_arrow.png);
    #         width: 12px;
    #         height: 12px;
    #     }
        
    #     QSlider::groove:horizontal {
    #         border: 1px solid #3399FF;
    #         height: 8px;
    #         background: #1E4976;
    #         margin: 2px 0;
    #         border-radius: 4px;
    #     }
        
    #     QSlider::handle:horizontal {
    #         background: #3399FF;
    #         border: 1px solid #3399FF;
    #         width: 18px;
    #         margin: -6px 0;
    #         border-radius: 9px;
    #     }
        
    #     QSlider::handle:horizontal:hover {
    #         background: #66B2FF;
    #         border-color: #66B2FF;
    #     }
        
    #     QCheckBox {
    #         spacing: 8px;
    #     }
        
    #     QCheckBox::indicator {
    #         width: 18px;
    #         height: 18px;
    #     }
        
    #     QCheckBox::indicator:unchecked {
    #         border: 2px solid #3399FF;
    #         border-radius: 4px;
    #         background: #1E4976;
    #     }
        
    #     QCheckBox::indicator:checked {
    #         border: 2px solid #3399FF;
    #         border-radius: 4px;
    #         background: #3399FF;
    #     }
        
    #     PlotWidget {
    #         border: 2px solid #3399FF;
    #         border-radius: 8px;
    #         background: #132F4C;
    #     }
        
    #     QTableWidget {
    #         gridline-color: #3399FF;
    #         border: 2px solid #3399FF;
    #         border-radius: 4px;
    #         selection-background-color: #1E4976;
    #     }
    # """)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.grpbx_DigitalFilter = QGroupBox(self.centralwidget)
        self.grpbx_DigitalFilter.setObjectName(u"grpbx_DigitalFilter")
        self.gridLayout = QGridLayout(self.grpbx_DigitalFilter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plot_magResponse = PlotWidget(self.grpbx_DigitalFilter)
        self.plot_magResponse.setObjectName(u"plot_magResponse")
        self.plot_magResponse.setMinimumSize(QSize(200, 0))

        self.verticalLayout_2.addWidget(self.plot_magResponse)

        self.plot_phaseResponse = PlotWidget(self.grpbx_DigitalFilter)
        self.plot_phaseResponse.setObjectName(u"plot_phaseResponse")
        self.plot_phaseResponse.setMinimumSize(QSize(200, 0))

        self.verticalLayout_2.addWidget(self.plot_phaseResponse)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.wgt_unitCircle = QWidget(self.grpbx_DigitalFilter)
        self.wgt_unitCircle.setObjectName(u"wgt_unitCircle")
        self.gridLayout_5 = QGridLayout(self.wgt_unitCircle)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.plot_unitCircle = PlotWidget(self.wgt_unitCircle)
        self.plot_unitCircle.setObjectName(u"plot_unitCircle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_unitCircle.sizePolicy().hasHeightForWidth())
        self.plot_unitCircle.setSizePolicy(sizePolicy)
        self.plot_unitCircle.setMinimumSize(QSize(400, 400))
        self.plot_unitCircle.setMaximumSize(QSize(400, 400))
        self.plot_unitCircle.setSizeIncrement(QSize(1, 1))
        self.plot_unitCircle.setBaseSize(QSize(0, 0))
        self.plot_unitCircle.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.plot_unitCircle, 1, 4, 1, 1)

        self.btn_Undo = QPushButton(self.wgt_unitCircle)
        self.btn_Undo.setObjectName(u"btn_Undo")
        self.btn_Undo.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_5.addWidget(self.btn_Undo, 2, 0, 1, 1)

        self.btn_Redo = QPushButton(self.wgt_unitCircle)
        self.btn_Redo.setObjectName(u"btn_Redo")
        self.btn_Redo.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_5.addWidget(self.btn_Redo, 3, 0, 1, 1)

        self.wgt_buttons = QWidget(self.wgt_unitCircle)
        self.wgt_buttons.setObjectName(u"wgt_buttons")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wgt_buttons.sizePolicy().hasHeightForWidth())
        self.wgt_buttons.setSizePolicy(sizePolicy1)
        self.wgt_buttons.setMaximumSize(QSize(120, 16777215))
        self.wgt_buttons.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.wgt_buttons)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.btn_addPoles = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles = QButtonGroup(MainWindow)
        self.btngrp_zerosPoles.setObjectName(u"btngrp_zerosPoles")
        self.btngrp_zerosPoles.addButton(self.btn_addPoles)
        self.btn_addPoles.setObjectName(u"btn_addPoles")
        self.btn_addPoles.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_addPoles)

        self.btn_addZeros = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles.addButton(self.btn_addZeros)
        self.btn_addZeros.setObjectName(u"btn_addZeros")
        self.btn_addZeros.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_addZeros)

        self.btn_Swapping = QPushButton(self.wgt_buttons)
        self.btn_Swapping.setObjectName(u"btn_Swapping")
        self.btn_Swapping.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_Swapping)

        self.btn_removePoles = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles.addButton(self.btn_removePoles)
        self.btn_removePoles.setObjectName(u"btn_removePoles")
        self.btn_removePoles.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_removePoles)

        self.btn_RemoveZeros = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles.addButton(self.btn_RemoveZeros)
        self.btn_RemoveZeros.setObjectName(u"btn_RemoveZeros")
        self.btn_RemoveZeros.setMaximumSize(QSize(100, 16777215))
        self.btn_RemoveZeros.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.btn_RemoveZeros)

        self.btn_removeAll = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles.addButton(self.btn_removeAll)
        self.btn_removeAll.setObjectName(u"btn_removeAll")
        self.btn_removeAll.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_removeAll)

        self.btn_Remove = QPushButton(self.wgt_buttons)
        self.btngrp_zerosPoles.addButton(self.btn_Remove)
        self.btn_Remove.setObjectName(u"btn_Remove")
        self.btn_Remove.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.btn_Remove)

        self.pair_mode_toggle = QCheckBox(self.wgt_buttons)
        self.pair_mode_toggle.setObjectName(u"pair_mode_toggle")

        self.verticalLayout_3.addWidget(self.pair_mode_toggle)

        self.mouse_en = QCheckBox(self.wgt_buttons)
        self.mouse_en.setObjectName(u"mouse_en")

        self.verticalLayout_3.addWidget(self.mouse_en)


        self.gridLayout_5.addWidget(self.wgt_buttons, 1, 0, 1, 1)

        self.btn_Import_Zero_Pole = QPushButton(self.wgt_unitCircle)
        self.btn_Import_Zero_Pole.setObjectName(u"btn_Import_Zero_Pole")
        self.btn_Import_Zero_Pole.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.btn_Import_Zero_Pole, 0, 1, 1, 1)

        self.btn_Export_Zero_Pole = QPushButton(self.wgt_unitCircle)
        self.btn_Export_Zero_Pole.setObjectName(u"btn_Export_Zero_Pole")
        self.btn_Export_Zero_Pole.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.btn_Export_Zero_Pole, 0, 2, 1, 2)


        self.gridLayout.addWidget(self.wgt_unitCircle, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.grpbx_DigitalFilter, 0, 0, 1, 1)

        self.grpbx_AllPassFilter = QGroupBox(self.centralwidget)
        self.grpbx_AllPassFilter.setObjectName(u"grpbx_AllPassFilter")
        sizePolicy1.setHeightForWidth(self.grpbx_AllPassFilter.sizePolicy().hasHeightForWidth())
        self.grpbx_AllPassFilter.setSizePolicy(sizePolicy1)
        self.grpbx_AllPassFilter.setMaximumSize(QSize(300, 16777215))
        self.gridLayout_3 = QGridLayout(self.grpbx_AllPassFilter)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(self.grpbx_AllPassFilter)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 5, 0, 0)
        self.table_coeff = QTableWidget(self.groupBox)
        if (self.table_coeff.columnCount() < 1):
            self.table_coeff.setColumnCount(1)
        self.table_coeff.setObjectName(u"table_coeff")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.table_coeff.sizePolicy().hasHeightForWidth())
        self.table_coeff.setSizePolicy(sizePolicy2)
        self.table_coeff.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table_coeff.setAlternatingRowColors(False)
        self.table_coeff.setShowGrid(True)
        self.table_coeff.setCornerButtonEnabled(False)
        self.table_coeff.setColumnCount(1)
        self.table_coeff.horizontalHeader().setVisible(False)
        self.table_coeff.verticalHeader().setVisible(False)

        self.gridLayout_7.addWidget(self.table_coeff, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)

        self.plot_allPass = PlotWidget(self.grpbx_AllPassFilter)
        self.plot_allPass.setObjectName(u"plot_allPass")
        self.plot_allPass.setMinimumSize(QSize(0, 70))
        self.plot_allPass.setMaximumSize(QSize(300, 16777215))

        self.gridLayout_3.addWidget(self.plot_allPass, 2, 0, 1, 1)

        self.wgt_coefficient = QWidget(self.grpbx_AllPassFilter)
        self.wgt_coefficient.setObjectName(u"wgt_coefficient")
        self.wgt_coefficient.setMinimumSize(QSize(0, 70))
        self.wgt_coefficient.setMaximumSize(QSize(300, 70))
        self.gridLayout_6 = QGridLayout(self.wgt_coefficient)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.all_pass_enable = QCheckBox(self.wgt_coefficient)
        self.all_pass_enable.setObjectName(u"all_pass_enable")

        self.gridLayout_6.addWidget(self.all_pass_enable, 1, 0, 1, 2)

        self.btn_addCoeff = QPushButton(self.wgt_coefficient)
        self.btn_addCoeff.setObjectName(u"btn_addCoeff")

        self.gridLayout_6.addWidget(self.btn_addCoeff, 1, 2, 1, 1)

        self.label = QLabel(self.wgt_coefficient)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)

        self.btn_removeCoeff = QPushButton(self.wgt_coefficient)
        self.btn_removeCoeff.setObjectName(u"btn_removeCoeff")

        self.gridLayout_6.addWidget(self.btn_removeCoeff, 1, 3, 1, 1)

        self.comboBox = QComboBox(self.wgt_coefficient)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy3)
        self.comboBox.setStyleSheet(u"background:white;\n"
"color:black;\n"
"")
        self.comboBox.setEditable(True)

        self.gridLayout_6.addWidget(self.comboBox, 0, 1, 1, 3)


        self.gridLayout_3.addWidget(self.wgt_coefficient, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.grpbx_AllPassFilter, 0, 1, 1, 1)

        self.grpbx_RealtimeFiltering = QGroupBox(self.centralwidget)
        self.grpbx_RealtimeFiltering.setObjectName(u"grpbx_RealtimeFiltering")
        self.grpbx_RealtimeFiltering.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_2 = QGridLayout(self.grpbx_RealtimeFiltering)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btnClr = QPushButton(self.grpbx_RealtimeFiltering)
        self.btnClr.setObjectName(u"btnClr")

        self.gridLayout_2.addWidget(self.btnClr, 1, 4, 1, 1)

        self.plot_realtimeFilter = PlotWidget(self.grpbx_RealtimeFiltering)
        self.plot_realtimeFilter.setObjectName(u"plot_realtimeFilter")

        self.gridLayout_2.addWidget(self.plot_realtimeFilter, 0, 2, 1, 2)

        self.plot_mouseInput = PlotWidget(self.grpbx_RealtimeFiltering)
        self.plot_mouseInput.setObjectName(u"plot_mouseInput")
        sizePolicy.setHeightForWidth(self.plot_mouseInput.sizePolicy().hasHeightForWidth())
        self.plot_mouseInput.setSizePolicy(sizePolicy)
        self.plot_mouseInput.setMinimumSize(QSize(200, 200))

        self.gridLayout_2.addWidget(self.plot_mouseInput, 0, 4, 1, 1)

        self.btn_openFile = QPushButton(self.grpbx_RealtimeFiltering)
        self.btn_openFile.setObjectName(u"btn_openFile")
        self.btn_openFile.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.btn_openFile, 1, 0, 1, 1)

        self.plot_realtimeInput = PlotWidget(self.grpbx_RealtimeFiltering)
        self.plot_realtimeInput.setObjectName(u"plot_realtimeInput")

        self.gridLayout_2.addWidget(self.plot_realtimeInput, 0, 0, 1, 2)

        self.speed_slider = QSlider(self.grpbx_RealtimeFiltering)
        self.speed_slider.setObjectName(u"speed_slider")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.speed_slider.sizePolicy().hasHeightForWidth())
        self.speed_slider.setSizePolicy(sizePolicy4)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.speed_slider, 1, 3, 1, 1)

        self.lbl_speed = QLabel(self.grpbx_RealtimeFiltering)
        self.lbl_speed.setObjectName(u"lbl_speed")
        self.lbl_speed.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lbl_speed, 1, 2, 1, 1)

        self.btn_play = QPushButton(self.grpbx_RealtimeFiltering)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setCheckable(False)

        self.gridLayout_2.addWidget(self.btn_play, 1, 1, 1, 1)


        self.gridLayout_4.addWidget(self.grpbx_RealtimeFiltering, 1, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.label.setBuddy(self.wgt_coefficient)
        self.lbl_speed.setBuddy(self.speed_slider)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        # Add these properties to specific widgets
        self.plot_unitCircle.setBackground('#132F4C')
        self.plot_magResponse.setBackground('#132F4C')
        self.plot_phaseResponse.setBackground('#132F4C')
        self.plot_allPass.setBackground('#132F4C')
        self.plot_realtimeFilter.setBackground('#132F4C')
        self.plot_mouseInput.setBackground('#132F4C')
        self.plot_realtimeInput.setBackground('#132F4C')
        
        # Add tooltips
        self.btn_addPoles.setToolTip("Add a pole to the filter design")
        self.btn_addZeros.setToolTip("Add a zero to the filter design")
        self.btn_Swapping.setToolTip("Swap between poles and zeros")
        self.speed_slider.setToolTip("Adjust the playback speed")
        self.pair_mode_toggle.setToolTip("Enable/disable conjugate pair mode")
        self.all_pass_enable.setToolTip("Enable all-pass filter configuration")
        self.btn_Undo.setToolTip("Undo last action (Ctrl+Z)")
        self.btn_Redo.setToolTip("Redo last action (Ctrl+Y)")
        
        # Make plots more attractive
        for plot in [self.plot_magResponse, self.plot_phaseResponse, self.plot_unitCircle,
                     self.plot_allPass, self.plot_realtimeFilter, self.plot_mouseInput,
                     self.plot_realtimeInput]:
            plot.showGrid(True, True, alpha=0.3)
            plot.setMenuEnabled(False)
            plot.getAxis('bottom').setPen(color='#3399FF')
            plot.getAxis('left').setPen(color='#3399FF')
            plot.getAxis('bottom').setTextPen(color='#E7EBF0')
            plot.getAxis('left').setTextPen(color='#E7EBF0')

        # Configure table
        self.table_coeff.setStyleSheet("""
            QTableWidget {
                background: #132F4C;
                color: #E7EBF0;
                gridline-color: #3399FF;
                border: 2px solid #3399FF;
            }
            QTableWidget::item:selected {
                background: #1E4976;
            }
        """)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import Zeros/Poles", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export Zeros/Poles", None))
        self.grpbx_DigitalFilter.setTitle(QCoreApplication.translate("MainWindow", u"Digital Filter Design", None))
        self.btn_Undo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.btn_Redo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.btn_addPoles.setText(QCoreApplication.translate("MainWindow", u"Add Pole", None))
        self.btn_addZeros.setText(QCoreApplication.translate("MainWindow", u"Add Zero", None))
        self.btn_Swapping.setText(QCoreApplication.translate("MainWindow", u"Swapping", None))
        self.btn_removePoles.setText(QCoreApplication.translate("MainWindow", u"Remove Poles", None))
        self.btn_RemoveZeros.setText(QCoreApplication.translate("MainWindow", u"Remove Zeros", None))
        self.btn_removeAll.setText(QCoreApplication.translate("MainWindow", u"Remove All", None))
        self.btn_Remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pair_mode_toggle.setText(QCoreApplication.translate("MainWindow", u"Pair Mode", None))
        self.mouse_en.setText(QCoreApplication.translate("MainWindow", u"Mouse Enable", None))
        self.btn_Import_Zero_Pole.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.btn_Import_Zero_Pole.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        self.btn_Export_Zero_Pole.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.btn_Export_Zero_Pole.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        self.grpbx_AllPassFilter.setTitle(QCoreApplication.translate("MainWindow", u"All Pass Filter Design", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"All Pass Filters", None))
        self.all_pass_enable.setText(QCoreApplication.translate("MainWindow", u"All Pass", None))
        self.btn_addCoeff.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Coefficient", None))
        self.btn_removeCoeff.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"-1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"-0.9", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"-0.495", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"0", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"0.495", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"0.9", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"1", None))

        self.grpbx_RealtimeFiltering.setTitle(QCoreApplication.translate("MainWindow", u"Realtime Filtering", None))
        self.btnClr.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.btn_openFile.setText(QCoreApplication.translate("MainWindow", u"Choose File", None))
        self.btn_openFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        self.lbl_speed.setText(QCoreApplication.translate("MainWindow", u"Speed: 1 Point/Second", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.btn_play.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))

if __name__ == "__main__":
        import sys
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec())