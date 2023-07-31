class ArgumentsMissingError(Exception):
    
    def __init__(self, arg:str) -> None:
        self._arg = arg
    
    def __str__(self) -> str:
        return f"ArgumentsMissingError : {self._arg} was/were not sent"