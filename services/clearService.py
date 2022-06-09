from os import system, name
from time import sleep

class ClearService:
    def clear(self):
        
        sleep(1.7)
        if name == 'nt':
            # _ = system('cls')
            next
        else:
            # _ = system('clear')
            next
