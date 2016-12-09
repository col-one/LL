from PySide.QtGui import *
from PySide.QtCore import *
import sys
import os
import MaxPlus
import legendass_entities
import qdarkstyle
import copy

"""
La specialiste de 3dsmax cest de tou foutre dans un seul fichier ! Je suis oblige
sinon je doit utiliser app.exec ce qui fou en lair le viewport....
"""

class MaxFile(object):
    def __init__(self):
        self.file_name = MaxPlus.FileManager.GetFileName()

class OpenFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.isfile(file_path):
            fm = MaxPlus.FileManager
            fm.Open(file_path)
        else:
            print "Invalide file"

class _GCProtector(object):
    controls = []

class ColumnSplit(QSplitter):
    def __init__(self, *args):
        super(ColumnSplit, self).__init__(*args)
        #widgets
        self.w_ep = QWidget()
        self.w_et = QWidget()
        self.w_sh = QWidget()
        self.w_fi = QWidget()
        self.l_episode = QListWidget()
        self.l_etape = QListWidget()
        self.l_shot = QListWidget()
        self.l_file = QListWidget()
        self.lab_ep = QLabel("Episodes : ")
        self.lab_et = QLabel("Etapes : ")
        self.lab_sh = QLabel("Plans : ")
        self.lab_fi = QLabel("Fichiers : ")
        self.empty_item = QListWidgetItem()
        #layouts
        self.lay_ep = QVBoxLayout(self.w_ep)
        self.lay_et = QVBoxLayout(self.w_et)
        self.lay_sh = QVBoxLayout(self.w_sh)
        self.lay_fi = QVBoxLayout(self.w_fi)
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
        self.addWidget(self.w_ep)
        self.addWidget(self.w_et)
        self.addWidget(self.w_sh)
        self.addWidget(self.w_fi)
        #attr
        self.implementation = self
        self.ep_select = None
        self.et_select = None
        self.sh_select = None
        self.fi_select = None
        self.items_ls = 0
        #get liste episodes
        self.ep_node = legendass_entities.Episode.get_episodes()
        self.ep_list = self.ep_node.episodes()

        self.l_episode.addItems(self.ep_list)

        # set implementation
        self.l_episode.itemSelectionChanged.connect(self.change_ep_select)
        self.l_file.itemDoubleClicked.connect(self.open_file)

    def change_ep_select(self):
        try:
            self.ep_select = self.l_episode.selectedItems()[0]
        except IndexError:
            pass
        # populate etape list
        self.l_etape.clear()
        self.l_shot.clear()
        self.l_file.clear()
        self.et_node = legendass_entities.Etape.get_etapes(self.ep_node.episode_path(str(self.ep_select.text())))
        self.et_list = self.et_node.etapes()
        self.l_etape.addItems(self.et_list)
        self.items_ls += 1
        # implement etape select change
        self.l_etape.itemSelectionChanged.connect(self.change_et_select)

    def change_et_select(self):
        try:
            self.et_select = self.l_etape.selectedItems()[0]
        except IndexError:
            pass
        # clear shot before change
        self.l_shot.clear()
        self.l_file.clear()
        # populate shot list
        self.sh_node = legendass_entities.Shot.get_shots(self.et_node.etape_path(str(self.et_select.text())))
        self.sh_list = self.sh_node.shots()
        self.l_shot.addItems(self.sh_list)
        self.items_ls += 1
        # implement shot select change
        self.l_shot.itemSelectionChanged.connect(self.change_sh_select)

    def change_sh_select(self):
        try:
            self.sh_select = self.l_shot.selectedItems()[0]
        except IndexError:
            pass
        # clear file before change
        self.l_file.clear()
        # populate file list
        self.fi_node = legendass_entities.MaxFile.get_files(self.sh_node.shot_path(str(self.sh_select.text())))
        self.fi_list = self.fi_node.files()
        self.l_file.addItems(self.fi_list)
        self.items_ls += 1

    def open_file(self):
        try:
            self.fi_select = self.l_file.selectedItems()[0]
        except IndexError:
            pass
        if (len(self.l_episode.selectedItems()) == 0
            or len(self.l_etape.selectedItems()) == 0
            or len(self.l_shot.selectedItems()) == 0
            or len(self.l_file.selectedItems()) == 0):
            print "Vous devez selection un element par liste"
            return False
        file_path = self.fi_node.file_path(str(self.fi_select.text()))
        OpenFile(file_path)
        self.l_file.setFocus()

class ColumnCreate(QSplitter):
    def __init__(self, *args):
        super(ColumnCreate, self).__init__()
        #attr
        self.et_preset = ["ANIM","ANIMATIQUE","BG","BLK","COMPO","DETECT","FLANIM","FX","LAYOUT","PROD","RENDU","STORYBOARD"]
        # widgets
        self.w_et = QWidget()
        self.l_etape = QListWidget()
        self.l_file = QListWidget()
        self.lab_et = QLabel("Nouvelle Etapes : ")
        self.empty_item = QListWidgetItem()
        # layouts
        self.lay_et = QVBoxLayout(self.w_et)
        # settings
        self.setGeometry(400, 300, 460, 450)
        self.lay_et.addWidget(self.lab_et)
        self.lay_et.addWidget(self.l_etape)
        self.lay_et.setContentsMargins(5, 5, 5, 5)
        self.addWidget(self.w_et)

        # attr
        self.implementation = self
        self.ep_select = None
        self.et_select = None
        self.sh_select = None
        self.fi_select = None
        self.items_ls = 0
        # get liste episodes
        self.l_etape.addItems(self.et_preset)


class TabWidget(QTabWidget):
    def __init__(self, column_open, column_create):
        super(TabWidget, self).__init__()
        self.column_create = column_create
        self.column_open = column_open


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        #attr
        self.asset = None
        #override attr
        self.setWindowTitle('Legendass')
        #widget
        self.split_g = ColumnSplit(Qt.Horizontal)
        self.split_c = ColumnCreate(Qt.Horizontal)
        self.tab = TabWidget(self.split_g, self.split_c)
        self.w_open = QWidget()
        self.lay_open = QVBoxLayout(self.w_open)
        self.w_create = QWidget()
        self.lay_create = QVBoxLayout(self.w_create)
        self.lay = QVBoxLayout(self)
        self.btn_open = QPushButton("Open")
        self.btn_create = QPushButton("Creer")
        self.lab_create = QLabel("")

        #override
        self.lab_create.setFixedHeight(30)
        self.btn_open.setMinimumHeight(80)
        self.btn_create.setMinimumHeight(80)

        #set param
        self.lay_open.addWidget(self.split_g)
        self.lay_open.addWidget(self.btn_open)
        self.lay_create.addWidget(self.split_c)
        self.lay_create.addWidget(self.lab_create)
        self.lay_create.addWidget(self.btn_create)


        self.tab.addTab(self.w_open, "Open")
        self.tab.addTab(self.w_create, "Create")
        self.tab.addTab(QWidget(), "Save")

        self.split_g.setSizes([50,130,100,180])
        self.split_c.setSizes([50,130,100,180])

        self.lay.addWidget(self.tab)

        #connect
        #implement episode select change
        self.btn_open.clicked.connect(self.split_g.open_file)

        self.tab.currentChanged.connect(self.SetSelectionColumn)

    def SetSelectionColumn(self):
        try:
            self.asset = legendass_entities.AssetInfo(MaxFile().file_name)
            self.lab_create.setText("Tu vas creer un nouveau fichier a partir de l'etape {etape}"
            .format(etape=self.asset.etape))
        except TypeError:
            print "invalide file"

def main():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    ui = MainWidget()
    mainwindow = QMainWindow()
    mainwindow.setWindowTitle('Legendass')
    mainwindow.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)
    mainwindow.setAttribute(Qt.WA_DeleteOnClose)
    mainwindow.setAttribute(Qt.WA_QuitOnClose)
    mainwindow.setAttribute(Qt.WA_X11NetWmWindowTypeDialog)
    _GCProtector.controls.append(mainwindow)
    MaxPlus.AttachQWidgetToMax(ui)
    mainwindow.setCentralWidget(ui)
    mainwindow.setGeometry(400, 300, 460, 450)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mainwindow.show()

if __name__ == '__main__':
    # st = open("C:\\Users\\DO\\PycharmProjects\\LL\\ressources\\darkorange.stylesheet")
    # style = st.read()
    # app.setStyleSheet(style)
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)
    main()
