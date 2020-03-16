from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar, QSplitter, QFrame, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit, QDialog, QDialogButtonBox, QColorDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from PyQt5 import uic

class MaterialInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/material.ui', self)
        self.exec_()
        # color = QColorDialog.getColor()
        # if color.isValid():
        #     print(color.name())
        