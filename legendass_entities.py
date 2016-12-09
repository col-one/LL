import os
import re


class Episode(object):
    EPISODE_PATH = "Z:\\LL_prod"
    _episodes = {} #{episode_num : episode_path}
    _episode_patt = r"\b\d{3}\b"
    @staticmethod
    def get_episodes():
        Episode._episodes = {}
        for dir in os.listdir(Episode.EPISODE_PATH):
            dir_path = os.path.join(Episode.EPISODE_PATH, dir)
            if os.path.isdir(dir_path) and re.match(Episode._episode_patt, dir):
                Episode._episodes[dir] = dir_path
        return Episode

    @staticmethod
    def episode_path(episode):
        if not isinstance(episode, str):
            raise TypeError("Episode must be string")
        return Episode._episodes[episode]

    @staticmethod
    def episodes():
        return list(sorted(Episode._episodes.keys()))

class Etape(object):
    _etapes = {}
    _etapes_patt = r"^([0-9]{2})_([A-Z]*)$"
    @staticmethod
    def get_etapes(episode_path):
        Etape._etapes = {}
        for dir in os.listdir(episode_path):
            reg_etape = re.match(Etape._etapes_patt, dir)
            dir_path = os.path.join(episode_path, dir)
            if os.path.isdir(dir_path) and reg_etape:
                Etape._etapes[reg_etape.groups()[1]] = dir_path
        return Etape

    @staticmethod
    def etape_path(etape):
        if not isinstance(etape, str):
            raise TypeError("Etape must be string")
        return Etape._etapes[etape]

    @staticmethod
    def etapes():
        return list(sorted(Etape._etapes.keys()))

class Shot(object):
    _shots = {}
    _shots_patt = r"^([0-9]{3})_([0-9]{3})$"
    @staticmethod
    def get_shots(etape_path):
        Shot._shots = {}
        for dir in os.listdir(etape_path):
            reg_shot = re.match(Shot._shots_patt, dir)
            dir_path = os.path.join(etape_path, dir)
            if os.path.isdir(dir_path) and reg_shot:
                Shot._shots[reg_shot.groups()[1]] = dir_path
        return Shot

    @staticmethod
    def shot_path(shot):
        if not isinstance(shot, str):
            raise TypeError("Shot must be string")
        return Shot._shots[shot]

    @staticmethod
    def shots():
        return list(sorted(Shot._shots.keys()))

class MaxFile(object):
    _files = {}
    _files_patt = r"^([0-9]{3})_([0-9]{3})_([A-Z]{3})_(v[0-9]{3}).(max)$"
    @staticmethod
    def get_files(shot_path):
        MaxFile._files = {}
        for dir in os.listdir(shot_path):
            reg_shot = re.match(MaxFile._files_patt, dir)
            dir_path = os.path.join(shot_path, dir)
            if not os.path.isdir(dir_path) and reg_shot:
                MaxFile._files[dir] = dir_path
        return MaxFile

    @staticmethod
    def file_path(file):
        if not isinstance(file, str):
            raise TypeError("File must be string")
        return MaxFile._files[file]

    @staticmethod
    def files():
        return list(MaxFile._files.keys())

    @staticmethod
    def paths():
        return list(MaxFile._files.values())

class AssetInfo(object):
    def __init__(self, file_name):
        ll_path = Episode.EPISODE_PATH
        self.corres = {"LAY":"04_LAYOUT", "BLK":"08_BLK", "ANI":"07_ANIM", "FLA":"09_FLANIM",
                       "RDR":"10_RENDU", "FXS":"11_FX", "CMP":"20_COMPO"}
        patt = MaxFile._files_patt
        match_name = re.match(patt, file_name)
        if match_name is None:
            raise TypeError("Ce fichier n'est pas un fichier valide Legendaire")
        self.episode = match_name.groups()[0]
        self.shot = match_name.groups()[1]
        self.etape = match_name.groups()[2]
        self.str_version = match_name.groups()[3]
        self.version = int(self.str_version.replace("v",""))
        self.extension = match_name.groups()[4]


