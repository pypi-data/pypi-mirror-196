# -*- coding: utf-8 -*-
import json
import re
import os
from time import sleep
from urllib.parse import urlparse, parse_qs

import pandas as pd
from PyQt5.QtCore import *

from idebug import *
from ipylib.ipath import *
from dataengineer.models import *

from youtube.Lib import *

__all__ = [
    'Playlists',
]


"""플레이리스트 모음"""
class Playlists(DataModel):

    @funcIdentity
    def __init__(self):
        super().__init__(self.__class__.__name__)
    @funcIdentity
    def create_n_update(self):
        self.drop()
        self.create()
        cursor = self.find()
        for d in list(cursor):
            self.add(d['name'], d['url'])
    @funcIdentity
    def add(self, listName, url):
        # 구글계정없이 액세스할 수 있는 'WatchURL'을 입력해야한다
        o = urlparse(url)
        logger.info(f'{self} | ParsedURL-->\n{[o, type(o)]}')
        qs = parse_qs(o.query)
        logger.info(f'{self} | QueryString-->\n{[qs, type(qs)]}')

        f = {'url':url}
        d = f.copy()
        d.update({'name':listName, 'pid': qs['list'][0]})
        self.update_one(f, {'$set':d}, True)
    @funcIdentity
    def view(self):
        cursor = self.find(None, {'_id':0})
        df = pd.DataFrame(list(cursor))
        return self._view(df)
    @property
    def Playlists(self):
        cursor = self.find(None, {'_id':0, 'playlist':0})
        df = pd.DataFrame(list(cursor))
        return self._view(df, title='플레이리스트 목록')
