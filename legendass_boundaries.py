#import MaxPlus
import legendass_entities

# class OpenFile(object):
#     def __init__(self, file_path):
#         self.file_path = file_path
#         fm = MaxPlus.FileManager
#         fm.Open(file_path)


class LegendassNode(object):
    def __init__(self, implementation):
        #attr
        self.implementation = implementation
        self.ep_select = None
        self.et_select = None
        self.sh_select = None

        #listes
        self.ep = self.implementation.l_episode
        self.et = self.implementation.l_etape
        self.sh = self.implementation.l_shot
        self.fi = self.implementation.l_file

        #get liste episodes
        self.ep_node = legendass_entities.Episode.get_episodes()
        self.ep_list = self.ep_node.episodes()

        #implement episode select change
        self.ep.itemSelectionChanged.connect(self.change_ep_select)

        #set implementation
        self.ep.addItems(self.ep_list)
        #self.implementation.l_etape.addItems(self.et_list)
        # self.implementation.l_episode.addItems(self.sh_list)

    def change_ep_select(self):
        try:
            self.ep_select = self.ep.selectedItems()[0]
        except IndexError:
            pass
        #populate etape list
        self.et.clear()
        self.sh.clear()
        self.et_node = legendass_entities.Etape.get_etapes(self.ep_node.episode_path(str(self.ep_select.text())))
        self.et_list = self.et_node.etapes()
        self.et.addItems(self.et_list)
        #implement etape select change
        self.et.itemSelectionChanged.connect(self.change_et_select)

    def change_et_select(self):
        try:
            self.et_select = self.et.selectedItems()[0]
        except IndexError:
            pass
        #clear shot before change
        self.sh.clear()
        #populate shot list
        self.sh_node = legendass_entities.Shot.get_shots(self.et_node.etape_path(str(self.et_select.text())))
        self.sh_list = self.sh_node.shots()
        self.sh.addItems(self.sh_list)
        #implement shot select change
        self.sh.itemSelectionChanged.connect(self.change_sh_select)

    def change_sh_select(self):
        try:
            self.sh_select = self.sh.selectedItems()[0]
        except IndexError:
            pass
        #clear file before change
        self.fi.clear()
        #populate file list
        self.fi_node = legendass_entities.MaxFile.get_files(self.sh_node.shot_path(str(self.sh_select.text())))
        self.fi_list = self.fi_node.files()
        self.fi.addItems(self.fi_list)