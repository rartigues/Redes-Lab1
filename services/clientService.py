import os
import socket
from configuration.Settings import Settings
from services.recieveService import RecieveService

class ClientService:
    _recieveService = RecieveService()

    ip = Settings.IP
    port = Settings.PORT
    addr = Settings.ADDR

    def startClient(self):
        print(f"Se intenta conectar al servidor en {self.ip}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            connected = False
            while not connected:
                try:
                    client.connect(self.addr)
                    connected = True
                except:
                    continue
            print(f"Se logro la conexion con el servidor en {self.ip}:{self.port}")
            
            self._recieveService.recieve(client)

