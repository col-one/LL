from PySide.QtGui import *
from PySide.QtCore import *

"""
jamais appele parce que max doit avoir tout pyside dans le fichier main...
"""

class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        #override attr
        self.setWindowTitle('Legendass')

        #widgets
        self.w_ep = QWidget()
        self.w_et = QWidget()
        self.w_sh = QWidget()
        self.w_fi = QWidget()
        self.l_episode = QListWidget()
        self.l_etape = QListWidget()
        self.l_shot = QListWidget()
        self.l_file = QListWidget()
        self.split_g = QSplitter(Qt.Horizontal)
        self.btn_open = QPushButton("Open")
        self.lab_ep = QLabel("Episodes : ")
        self.lab_et = QLabel("Etapes : ")
        self.lab_sh = QLabel("Plans : ")
        self.lab_fi = QLabel("Fichiers : ")
        self.tab = QTabWidget()
        self.empty_item = QListWidgetItem()
        #layouts
        self.lay_ep = QVBoxLayout(self.w_ep)
        self.lay_et = QVBoxLayout(self.w_et)
        self.lay_sh = QVBoxLayout(self.w_sh)
        self.lay_fi = QVBoxLayout(self.w_fi)
        self.lay = QVBoxLayout(self)
        #settings
        self.setGeometry(400, 300, 460, 450)
        self.lay_ep.addWidget(self.lab_ep)
        self.lay_ep.addWidget(self.l_episode)
        self.lay_ep.setContentsMargins(5,5,5,5)
        self.lay_et.addWidget(self.lab_et)
        self.lay_et.addWidget(self.l_etape)
        self.lay_et.setContentsMargins(5,5,5,5)
        self.lay_sh.addWidget(self.lab_sh)
        self.lay_sh.addWidget(self.l_shot)
        self.lay_sh.setContentsMargins(5,5,5,5)
        self.lay_fi.addWidget(self.lab_fi)
        self.lay_fi.addWidget(self.l_file)
        self.lay_fi.setContentsMargins(5,5,5,5)
        self.split_g.addWidget(self.w_ep)
        self.split_g.addWidget(self.w_et)
        self.split_g.addWidget(self.w_sh)
        self.split_g.addWidget(self.w_fi)
        self.tab.addTab(self.split_g, "Open")
        self.tab.addTab(QWidget(), "Create")
        self.tab.addTab(QWidget(), "Save")
        self.lay.addWidget(self.tab)
        self.lay.addWidget(self.btn_open)
        self.split_g.setSizes([50,130,100,180])
        self.btn_open.setMinimumHeight(80)
