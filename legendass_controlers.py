from PySide.QtGui import *
from PySide.QtCore import *

class MainWidget(QDialog):
    def __init__(self):
        super(MainWidget, self).__init__()
        #override attr
        self.setWindowTitle('Legendass')

        #widgets
        self.l_episode = QListWidget()
        self.l_etape = QListWidget()
        self.l_shot = QListWidget()
        self.l_file = QListWidget()
        self.split_g = QSplitter(Qt.Horizontal)

        #layouts
        self.lay = QHBoxLayout(self)

        #settings
        self.setGeometry(400, 300, 300, 450)
        self.split_g.addWidget(self.l_episode)
        self.split_g.addWidget(self.l_etape)
        self.split_g.addWidget(self.l_shot)
        self.split_g.addWidget(self.l_file)
        self.lay.addWidget(self.split_g)
        self.setModal(True)