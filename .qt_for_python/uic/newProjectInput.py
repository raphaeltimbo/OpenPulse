# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\OpenPulse\data\user_input\ui\Project\newProjectInput.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(567, 330)
        Dialog.setMinimumSize(QtCore.QSize(567, 330))
        Dialog.setMaximumSize(QtCore.QSize(567, 330))
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 567, 330))
        self.frame.setMinimumSize(QtCore.QSize(567, 330))
        self.frame.setMaximumSize(QtCore.QSize(567, 330))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(48, 88, 150, 25))
        self.label_8.setMinimumSize(QtCore.QSize(150, 25))
        self.label_8.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.button_create_project = QtWidgets.QDialogButtonBox(self.frame)
        self.button_create_project.setGeometry(QtCore.QRect(374, 286, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button_create_project.setFont(font)
        self.button_create_project.setOrientation(QtCore.Qt.Horizontal)
        self.button_create_project.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_create_project.setCenterButtons(True)
        self.button_create_project.setObjectName("button_create_project")
        self.toolButton_search_project_folder = QtWidgets.QToolButton(self.frame)
        self.toolButton_search_project_folder.setGeometry(QtCore.QRect(458, 88, 75, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_search_project_folder.sizePolicy().hasHeightForWidth())
        self.toolButton_search_project_folder.setSizePolicy(sizePolicy)
        self.toolButton_search_project_folder.setMinimumSize(QtCore.QSize(75, 25))
        self.toolButton_search_project_folder.setMaximumSize(QtCore.QSize(75, 25))
        self.toolButton_search_project_folder.setSizeIncrement(QtCore.QSize(0, 1))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.toolButton_search_project_folder.setFont(font)
        self.toolButton_search_project_folder.setObjectName("toolButton_search_project_folder")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 567, 38))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(48, 52, 150, 25))
        self.label_2.setMinimumSize(QtCore.QSize(150, 25))
        self.label_2.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit_project_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_project_name.setGeometry(QtCore.QRect(202, 52, 250, 25))
        self.lineEdit_project_name.setMinimumSize(QtCore.QSize(250, 25))
        self.lineEdit_project_name.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_project_name.setFont(font)
        self.lineEdit_project_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_project_name.setFrame(True)
        self.lineEdit_project_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_project_name.setObjectName("lineEdit_project_name")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(16, 126, 533, 149))
        self.tabWidget.setMinimumSize(QtCore.QSize(470, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit_element_size = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_element_size.setEnabled(True)
        self.lineEdit_element_size.setGeometry(QtCore.QRect(216, 44, 131, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_element_size.setFont(font)
        self.lineEdit_element_size.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_element_size.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_element_size.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_element_size.setMaxLength(20)
        self.lineEdit_element_size.setFrame(True)
        self.lineEdit_element_size.setCursorPosition(4)
        self.lineEdit_element_size.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_element_size.setObjectName("lineEdit_element_size")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(348, 44, 75, 25))
        self.label_7.setObjectName("label_7")
        self.lineEdit_import_geometry = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_import_geometry.setEnabled(False)
        self.lineEdit_import_geometry.setGeometry(QtCore.QRect(125, 10, 300, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_import_geometry.sizePolicy().hasHeightForWidth())
        self.lineEdit_import_geometry.setSizePolicy(sizePolicy)
        self.lineEdit_import_geometry.setMinimumSize(QtCore.QSize(260, 25))
        self.lineEdit_import_geometry.setMaximumSize(QtCore.QSize(300, 25))
        self.lineEdit_import_geometry.setSizeIncrement(QtCore.QSize(0, 1))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.lineEdit_import_geometry.setFont(font)
        self.lineEdit_import_geometry.setStyleSheet("color: rgb(0, 0, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.lineEdit_import_geometry.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_import_geometry.setObjectName("lineEdit_import_geometry")
        self.toolButton_import_geometry = QtWidgets.QToolButton(self.tab)
        self.toolButton_import_geometry.setGeometry(QtCore.QRect(434, 10, 80, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_import_geometry.sizePolicy().hasHeightForWidth())
        self.toolButton_import_geometry.setSizePolicy(sizePolicy)
        self.toolButton_import_geometry.setMinimumSize(QtCore.QSize(80, 25))
        self.toolButton_import_geometry.setMaximumSize(QtCore.QSize(80, 25))
        self.toolButton_import_geometry.setSizeIncrement(QtCore.QSize(0, 1))
        self.toolButton_import_geometry.setObjectName("toolButton_import_geometry")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(58, 44, 150, 25))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(12, 10, 111, 25))
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(348, 80, 75, 25))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(58, 80, 150, 25))
        self.label_10.setObjectName("label_10")
        self.lineEdit_geometry_tolerance = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_geometry_tolerance.setEnabled(True)
        self.lineEdit_geometry_tolerance.setGeometry(QtCore.QRect(216, 80, 131, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_geometry_tolerance.setFont(font)
        self.lineEdit_geometry_tolerance.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_geometry_tolerance.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_geometry_tolerance.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_geometry_tolerance.setMaxLength(20)
        self.lineEdit_geometry_tolerance.setFrame(True)
        self.lineEdit_geometry_tolerance.setCursorPosition(4)
        self.lineEdit_geometry_tolerance.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_geometry_tolerance.setObjectName("lineEdit_geometry_tolerance")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lineEdit_import_connectivity = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_import_connectivity.setEnabled(False)
        self.lineEdit_import_connectivity.setGeometry(QtCore.QRect(180, 66, 260, 25))
        self.lineEdit_import_connectivity.setMinimumSize(QtCore.QSize(260, 25))
        self.lineEdit_import_connectivity.setMaximumSize(QtCore.QSize(260, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.lineEdit_import_connectivity.setFont(font)
        self.lineEdit_import_connectivity.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_import_connectivity.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_import_connectivity.setObjectName("lineEdit_import_connectivity")
        self.lineEdit_import_nodal_coordinates = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_import_nodal_coordinates.setEnabled(False)
        self.lineEdit_import_nodal_coordinates.setGeometry(QtCore.QRect(180, 22, 260, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.lineEdit_import_nodal_coordinates.sizePolicy().hasHeightForWidth())
        self.lineEdit_import_nodal_coordinates.setSizePolicy(sizePolicy)
        self.lineEdit_import_nodal_coordinates.setMinimumSize(QtCore.QSize(260, 25))
        self.lineEdit_import_nodal_coordinates.setMaximumSize(QtCore.QSize(260, 25))
        self.lineEdit_import_nodal_coordinates.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.lineEdit_import_nodal_coordinates.setFont(font)
        self.lineEdit_import_nodal_coordinates.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_import_nodal_coordinates.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_import_nodal_coordinates.setObjectName("lineEdit_import_nodal_coordinates")
        self.toolButton_import_conn = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_import_conn.setGeometry(QtCore.QRect(446, 66, 75, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_import_conn.sizePolicy().hasHeightForWidth())
        self.toolButton_import_conn.setSizePolicy(sizePolicy)
        self.toolButton_import_conn.setMinimumSize(QtCore.QSize(75, 25))
        self.toolButton_import_conn.setMaximumSize(QtCore.QSize(75, 25))
        self.toolButton_import_conn.setSizeIncrement(QtCore.QSize(0, 1))
        self.toolButton_import_conn.setObjectName("toolButton_import_conn")
        self.toolButton_import_cord = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_import_cord.setGeometry(QtCore.QRect(446, 22, 75, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_import_cord.sizePolicy().hasHeightForWidth())
        self.toolButton_import_cord.setSizePolicy(sizePolicy)
        self.toolButton_import_cord.setMinimumSize(QtCore.QSize(75, 25))
        self.toolButton_import_cord.setMaximumSize(QtCore.QSize(75, 25))
        self.toolButton_import_cord.setSizeIncrement(QtCore.QSize(0, 1))
        self.toolButton_import_cord.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_import_cord.setAutoFillBackground(False)
        self.toolButton_import_cord.setObjectName("toolButton_import_cord")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(2, 66, 177, 25))
        self.label_6.setMinimumSize(QtCore.QSize(0, 25))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(6, 22, 173, 25))
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_2, "")
        self.lineEdit_project_folder = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_project_folder.setEnabled(False)
        self.lineEdit_project_folder.setGeometry(QtCore.QRect(202, 88, 250, 25))
        self.lineEdit_project_folder.setMinimumSize(QtCore.QSize(250, 25))
        self.lineEdit_project_folder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.lineEdit_project_folder.setFont(font)
        self.lineEdit_project_folder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 255);")
        self.lineEdit_project_folder.setFrame(True)
        self.lineEdit_project_folder.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_project_folder.setObjectName("lineEdit_project_folder")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create new Project"))
        self.label_8.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Project directory:</p></body></html>"))
        self.toolButton_search_project_folder.setText(_translate("Dialog", "Search"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">New project</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Project name:</p></body></html>"))
        self.lineEdit_element_size.setText(_translate("Dialog", "0.01"))
        self.lineEdit_element_size.setPlaceholderText(_translate("Dialog", "< Insert a value >"))
        self.label_7.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Unit: [m]</p></body></html>"))
        self.toolButton_import_geometry.setText(_translate("Dialog", "Import"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Element size:</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Geometry file:</p></body></html>"))
        self.label_9.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Unit: [m]</p></body></html>"))
        self.label_10.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Geometry tolerance:</p></body></html>"))
        self.lineEdit_geometry_tolerance.setText(_translate("Dialog", "1e-8"))
        self.lineEdit_geometry_tolerance.setPlaceholderText(_translate("Dialog", "< Insert a value >"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Import geometry"))
        self.toolButton_import_conn.setText(_translate("Dialog", "Import"))
        self.toolButton_import_cord.setText(_translate("Dialog", "Import"))
        self.label_6.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Connectivity matrix file:</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Nodal coordinates file:</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Import mesh"))
