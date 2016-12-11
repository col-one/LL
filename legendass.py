from PySide.QtGui import *
from PySide.QtCore import *
import sys
import os
import MaxPlus
import legendass_entities
import qdarkstyle
import copy
reload(legendass_entities)
"""
La specialistee de 3dsmax cest de tout foutre dans un seul fichier ! Je suis oblige
sinon je doit utiliser app.exec ce qui fou en lair le viewport....
"""

class MaxFile(object):
    def __init__(self):
        self.file_name = MaxPlus.FileManager.GetFileName()

    @staticmethod
    def open_max(file):
        MaxPlus.FileManager.Open(file)

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
        self.et_preset = ["ANIM","BLK","COMPO","FLANIM","FX","LAYOUT","RENDU"]
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
        self.et_select = QListWidgetItem()
        self.sh_select = None
        self.fi_select = None
        self.items_ls = 0
        # get liste episodes
        self.l_etape.addItems(self.et_preset)

        self.l_etape.itemSelectionChanged.connect(self.change_et_select)

    def change_et_select(self):
        try:
            self.et_select = self.l_etape.selectedItems()[0]
        except IndexError:
            pass


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
        self.lab_create.setStyleSheet("QLabel { color : orange; }")
        self.btn_save = QPushButton("Save and Version !!!")
        self.w_save = QWidget()
        self.lay_save = QVBoxLayout(self.w_save)
        #override
        self.lab_create.setFixedHeight(30)
        self.btn_open.setMinimumHeight(80)
        self.btn_create.setMinimumHeight(80)
        self.btn_save.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        #set param
        self.lay_open.addWidget(self.split_g)
        self.lay_open.addWidget(self.btn_open)
        self.lay_create.addWidget(self.split_c)
        self.lay_create.addWidget(self.lab_create)
        self.lay_create.addWidget(self.btn_create)
        self.lay_save.addWidget(self.btn_save)


        self.tab.addTab(self.w_open, "Open")
        self.tab.addTab(self.w_create, "Create")
        self.tab.addTab(self.w_save, "Save")
        self.tab.addTab(QWidget(), "Settings")

        self.split_g.setSizes([50,130,100,180])
        self.split_c.setSizes([50,130,100,180])

        self.lay.addWidget(self.tab)

        #connect
        #implement episode select change
        self.btn_open.clicked.connect(self.split_g.open_file)
        self.btn_create.clicked.connect(self.create)
        self.btn_save.clicked.connect(self.save)
        self.tab.currentChanged.connect(self.setSelectionColumn)
        self.split_c.l_etape.itemSelectionChanged.connect(self.setSelectionColumn)

    def setSelectionColumn(self):
        try:
            self.asset = legendass_entities.AssetInfo(MaxFile().file_name)
            self.lab_create.setText("Tu vas creer un nouveau fichier {new} a partir de l'etape {etape}"
                                    " pour le shot {shot} de l'episode {ep}"
            .format(etape=self.asset.proto.etape, shot=self.asset.proto.shot,
                    ep=self.asset.proto.episode, new=self.split_c.et_select.text()))
        except TypeError:
            self.lab_create.setText("Fichier invalide")

    def create(self):
        new_etape = self.split_c.et_select.text()
        self.asset = legendass_entities.AssetInfo(MaxFile().file_name)
        self.current_asset = copy.deepcopy(self.asset)
        self.asset.change_etape(str(new_etape))
        self.asset.change_version(1)
        current_file = legendass_entities.FileManage(self.current_asset.deduice_path())
        if not current_file.copy_file(self.asset.deduice_path()):
            rep = QMessageBox.question(self, "Legendass", "Le fichier {f} que tu tentes de creer existe deja, "
                                                        "veux tu creer une nouvelle version?".format(f=self.asset.proto.file),
                                       QMessageBox.Yes|QMessageBox.No)
            if rep == QMessageBox.Yes:
                return
            else:
                return
        rep = QMessageBox.question(self, "Legendass", "Voulez vous ouvrir le fichier cree?",
                                   QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            MaxFile.open_max(self.asset.file_path)
        self.btn_create.clearFocus()

    def save(self):
        asset_json = legendass_entities.Asset(MaxFile().file_name)
        asset_json.add_version("003", "un com trop lol")

        self.btn_save.clearFocus()

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
    mainwindow.setGeometry(0, 300, 550, 450)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mainwindow.show()

if __name__ == '__main__':
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)
    main()
