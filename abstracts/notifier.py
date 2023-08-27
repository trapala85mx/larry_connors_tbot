# Python
from abc import ABCMeta
from abc import abstractmethod
# Project
# Externals


class Notifier(metaclass=ABCMeta):
    """Abstract class that represents a Notifier that is in charge of show the mesage
    """    
    @abstractmethod
    def send_signal(msg:str) -> None : pass