# Python
from abc import ABCMeta
from abc import abstractmethod
# Project
# Externals


class Notifier(metaclass=ABCMeta):
    
    @abstractmethod
    def send_signal(msg:str) -> None : pass