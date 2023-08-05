# -*- coding: utf-8 -*-
import json
import re
import os
from pathlib import PureWindowsPath, PurePosixPath
from time import sleep

from PyQt5.QtCore import *

from idebug import *
from ipylib.ipath import *

from youtube.Lib import *
from youtube.models import *


__all__ = [
    'FileHandler',
    'MusicStorage',
]

class MusicStorage:

    def __init__(self, dirpath=None):
        p = 'C:/Users/innovata/Music' if dirpath is None else dirpath
        self.path = clean_path(p)
    def find(self, name):
        with os.scandir(self.path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    m = re.search(name, entry.name, flags=re.I)
                    self.detected = None if m is None else entry.name
                    if m is not None: break
        if self.detected is None:
            logger.info(f'{self} | File Not Found')
        else:
            print('m-->', m, entry.name)
            logger.info(f'{self} | File Found--> {self.detected_fullpath}')
    @property
    def detected_fullpath(self): return os.path.join(self.path, self.detected)
    @funcIdentity
    def rename_detected(self, newName):
        if self.detected is not None:
            root, ext = os.path.splitext(self.detected)
            newFilename = f'{newName}{ext}'
            dst = os.path.join(self.path, newFilename)
            try:
                os.rename(self.detected_fullpath, dst)
                logger.info(f'{self} | Renamed-->\n{self.detected_fullpath} ==>>\n{dst}')
            except Exception as e:
                logger.error([self, e])
    @funcIdentity
    def clean_all_names(self): pass

class FileHandler(BaseQWorker):

    @funcIdentity
    def __init__(self):
        super().__init__()

    @property
    def dl_path(self): return self._dl_path
    @property
    def filename(self): return self._filename
    @property
    def fpath(self): return clean_path(f'{self.dl_path}/{self.filename}')

    @funcIdentity
    def set_dlpath(self, path=None):
        try:
            if path is None:
                if os.name == 'nt': path = 'C:/Users/innovata/Music'
                elif os.name == 'posix': path = '/Users/sambong/Music'
            self._dl_path = clean_path(path)
            # 해당 경로가 존재하지 않으면 강제로 생성한다
            if not os.path.exists(path): os.makedirs(path)
            return self
        except Exception as e:
            logger.error([self, e])
            raise
    @funcIdentity
    def set_filename(self, s): self._filename = clean_filename(s)
    @funcIdentity
    def autorename(self): pass
    @funcIdentity
    def autorename_all(self): pass
