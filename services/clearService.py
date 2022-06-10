from os import system, name
from time import sleep

class ClearService:
    def clear(self):
        
        sleep(0.1)
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
