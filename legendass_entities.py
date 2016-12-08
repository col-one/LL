import os
import re


class Episode(object):
    EPISODE_PATH = "Z:\\LL_prod"
    _episodes = {} #{episode_num : episode_path}
    _episode_patt = r"\b\d{3}\b"
    @staticmethod
    def get_episodes():
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
        return list(Episode._episodes.keys())

class Etape(object):
    _etapes = {}
    _etapes_patt = r"^([0-9]{2})_([A-Z]*)$"
    @staticmethod
    def get_etapes(episode_path):
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
        return list(Etape._etapes.keys())

class Shot(object):
    _shots = {}
    _shots_patt = r"^([0-9]{3})_([0-9]{3})$"
    @staticmethod
    def get_shots(etape_path):
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
        return list(Shot._shots.keys())

class MaxFile(object):
    _files = {}
    _files_patt = r"^([0-9]{3})_([0-9]{3})_([A-Z]{3})_(v[0-9]{3}).(max)$"
    @staticmethod
    def get_files(shot_path):
        for dir in os.listdir(shot_path):
            reg_shot = re.match(MaxFile._files_patt, dir)
            dir_path = os.path.join(shot_path, dir)
            if not os.path.isdir(dir_path) and reg_shot:
                MaxFile._files[dir] = dir_path
        return MaxFile

    @staticmethod
    def file_path(file):
        if not isinstance(file, str):
            raise TypeError("Shot must be string")
        return MaxFile._files[file]

    @staticmethod
    def files():
        return list(MaxFile._files.keys())

ep = Episode.get_episodes()
print ep.episodes()
et = Etape.get_etapes(ep.episode_path("102"))
sh = Shot.get_shots(et.etape_path("LAYOUT"))
fi = MaxFile.get_files(sh.shot_path("006"))


