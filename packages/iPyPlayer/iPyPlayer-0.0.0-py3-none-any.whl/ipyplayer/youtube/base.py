# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime


from PyQt5.QtCore import *
import pandas as pd


from idebug import *

from dataengineer.base import *
from dataengineer.datacls import *


__all__ = [
    'BaseClass',
    'QBaseObject',
    'WorkerGenerator',
    'WorkerMDB',
]



class QBaseObject(QObject, BaseClass):
    # 용어정의
    # - 객체 생성: __init__() --> None
    # - 객체 종료/파괴: 파이썬이 알아서 해준다
    # - 작업시작: start/run() --> started.emit [작업(시작시퀀스)완료]
    # - 작업종료: close/stop/quit/exit() --> closed/stopped/finished
    # - 작업중지: pause() --> paused.emit
    # 서브작업완료의 경우 보다 상세한 시그널명을 사용하라

    # PyQt5의 정해진 규칙
    # thread.start() --> thread.started.emit()
    # thread.quit() --> thread.finished.emit()

    # worker.__init__() --> None
    # worker.start() --> worker.started.emit()
    # worker.started --> worker.run()
    # worker.run() --> None
    # worker.close() --> object.finished.emit()

    finished = pyqtSignal()
    closed = pyqtSignal() # finished 로 통일하라
    stopped = pyqtSignal() # finished 로 통일하라
    started = pyqtSignal() # 가끔 필요한 경우도 있다
    completed = pyqtSignal() # 보다 작은 작업 수준에서 작업완료시 사용하라
    initiated = pyqtSignal() # 초기화 작업 완료
    """이하 기본함수들은 '복붙'해서 사용해야 로깅이 정확하게 된다"""

    # @funcIdentity
    def __init__(self): super().__init__()
    @stateFunc
    def finish(self, *args): self.finished.emit()
    @stateFunc
    def State(self, *args): pass
    @funcIdentity
    @pyqtSlot()
    def sig_initiated(self): self.initiated.emit()

    @funcIdentity
    def run(self): pass

    @property
    def workerName(self): return self.__class__.__name__

    def starts_running(self):
        PartGubun(f'스레드 시작({self.workerName})', simbol='#')
    # @funcIdentity
    def started_running(self):
        PartGubun(f'스레드 시작시퀀스 완료({self.workerName})', simbol='#')
        self.started.emit()

class WorkerGenerator(QBaseObject):
    terminated = pyqtSignal(str)

    # @funcIdentity
    def __init__(self, qobject, func='run', *args, **kwargs):
        super().__init__()
        try:
            self.func = func
            self._args = args
            self._kwargs = kwargs

            self.obj = qobject(*self._args, **self._kwargs) if callable(qobject) else qobject
            self.name = self.obj.__class__.__name__

            self.thread = QThread()
            self.obj.moveToThread(self.thread)

            """시작시"""
            self.thread.started.connect(getattr(self.obj, self.func))
            self.thread.started.connect(self.started)

            """종료시 : 중요! 객체종료 -> 스레드종료 -> self종료 순으로 진행"""
            self.obj.finished.connect(self.thread.quit)
            self.thread.finished.connect(self.finish)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.obj.deleteLater)
        except Exception as e:
            args = [qobject, func, args, kwargs]
            logger.error([self, self.__init__, e, *args])
            self.finish(e)
    # @stateFunc
    def finish(self, *args):
        try:
            self.finished.emit()
            if hasattr(self, 'wid'): self.terminated.emit(self.wid)
        except Exception as e:
            logger.error([self, e])
    @stateFunc
    def State(self, *args): pass

    # @stateFunc
    def start(self): self.thread.start()
    # @stateFunc
    def stop(self): self.thread.quit()
    @property
    def is_runinng(self): return self.thread.isRunning()
    def set_workerId(self, id): self.wid = str(id)


class WorkerMDB(QBaseObject, BaseDataClass):
    # 스레드워커를 관리하는 메모리DB

    @funcIdentity
    def __init__(self, datanm=None):
        super().__init__()
        self._set_name(datanm)
    @stateFunc
    def State(self, *args): pass

    # @stateFunc
    def set(self, k, worker):
        try:
            k = str(k)
            if self.isin(k): pass
            else:
                worker.set_workerId(k)
                worker.terminated.connect(self.unset)
                setattr(self, k, worker)
        except Exception as e:
            logger.error([self, e, k, self.dataname])
    # @stateFunc
    @pyqtSlot(str)
    def unset(self, k):
        try:
            if self.isin(k): delattr(self, k)
            else: pass
            # self.State(self.dataname, self.len, self.keys)
        except Exception as e:
            logger.error([self, e, k, self.dataname])
    # @stateFunc
    def set_n_run(self, k, worker):
        try:
            k = str(k)
            if self.isin(k): pass
            else:
                self.set(k, worker)
                worker.start()
            # self.State(self.dataname, self.len, self.keys)
        except Exception as e:
            logger.error([self, e, k, self.dataname])
    # @stateFunc
    def kill_n_unset(self, k):
        try:
            k = str(k)
            if self.isin(k):
                w = self.get(k)
                w.stop()
            else: pass
            # self.State(self.dataname, self.len, self.keys)
        except Exception as e:
            logger.error([self, e, k, self.dataname])
