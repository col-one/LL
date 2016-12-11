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

class EtapeFile():
    def __init__(self, et):
        self.corres = {"LAY":"04_LAYOUT", "BLK":"08_BLK", "ANI":"07_ANIM", "FLA":"09_FLANIM",
                       "RDR":"10_RENDU", "FXS":"11_FX", "CMP":"20_COMPO"}
        self.long = None
        self.short = None
        self.normal = None

        if et in list(self.corres.keys()):
            self.short = et
            self.long = self.corres[et]
            self.normal = self.corres[et].split("_")[-1]
        elif et in list(self.corres.values()):
            for key, value in self.corres.iteritems():
                if value == et:
                    self.short = key
            self.long = et
            self.normal = et.split("_")[-1]
        elif et in [value.split("_")[-1] for value in self.corres.values()]:
            self.normal = et
            for key, value in  self.corres.iteritems():
                if et in value:
                    self.long = value
                    self.short = key
        else:
            raise NameError(et + " n'est pas un mot valide")

    def __str__(self):
        return "Short : {short} \nNormal : {nor} \nLong : {long}".format(short=self.short,
                                                                           nor=self.normal,
                                                                           long=self.long)

class ProtoAsset():
    file = None
    episode = None
    shot = None
    shot_long = None
    etape = None
    etape_short = None
    etape_long = None
    str_version = None
    version = None
    extension = None

class AssetInfo(object):
    def __init__(self, file_name):
        self.file_path = None
        self.ll_path = Episode.EPISODE_PATH

        patt = MaxFile._files_patt
        match_name = re.match(patt, file_name)
        self.proto = ProtoAsset()
        if match_name is None:
            raise TypeError("{file} Ce fichier n'est pas un fichier valide Legendaire".format(file=file_name))
        self.etape = EtapeFile(match_name.groups()[2])
        self.proto.file = file_name
        self.proto.episode = match_name.groups()[0]
        self.proto.shot = match_name.groups()[1]
        self.proto.shot_long = self.proto.episode + "_" + self.proto.shot
        self.proto.etape = self.etape.normal
        self.proto.etape_short =self.etape.short
        self.proto.etape_long = self.etape.long
        self.proto.str_version = match_name.groups()[3]
        self.proto.version = int(self.proto.str_version.replace("v",""))
        self.proto.extension = match_name.groups()[4]

    def deduice_path(self):
        self.file_path = self.ll_path + "\\{ep}\\{etape}\\{shot}\\{file}".format(
            ep=self.proto.episode, etape=self.proto.etape_long, shot=self.proto.shot_long,
            file=self.proto.file)
        return self.file_path

    def change_etape(self, etape):
        if not isinstance(etape, str):
            raise TypeError("Etape doit etre de type string")
        etape = EtapeFile(etape)
        new_name = "{ep}_{shot}_{etape}_{ver}.{ext}".format(ep=self.proto.episode,
                    etape=etape.short, shot=self.proto.shot, ver=self.proto.str_version,
                                                        ext=self.proto.extension)
        n = AssetInfo(new_name)
        self.proto = n.proto

    def change_version(self, ver):
        ver = str(ver)
        if not ver.isdigit():
            raise TypeError("version doit etre de type string digit")
        new_name = "{ep}_{shot}_{etape}_v{ver:0=3d}.{ext}".format(ep=self.proto.episode,
                    etape=self.proto.etape_short, shot=self.proto.shot, ver=int(ver),
                                                        ext=self.proto.extension)
        n = AssetInfo(new_name)
        self.proto = n.proto

class FileManage(object):
    def __init__(self, file_path):
        self.file = file_path
        self.exist = None
        if not os.path.isfile(self.file):
            self.is_valide = False
        else:
            self.exist = True

    def copy_file(self, dst):
        if os.path.isfile(dst):
            print("Warning ! {f} existe deja, pas de copy".format(f=dst))
            return False
        import shutil
        try:
            os.makedirs(os.path.dirname(dst))
        except WindowsError:
            print "integralite du path deja cree, pass."
        shutil.copy2(self.file, dst)
        return dst