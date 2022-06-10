import os
import socket
from configuration.Settings import Settings
from services.recieveService import RecieveService
from services.clearService import ClearService

class ClientService:
    _recieveService = RecieveService()
    _clearService = ClearService()

    ip = Settings.IP
    port = Settings.PORT
    addr = Settings.ADDR

    def startClient(self):
        self._clearService.clear()
        print(f"Se intenta conectar al servidor en {self.ip}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            connected = False
            while not connected:
                try:
                    client.connect(self.addr)
                    connected = True
                except:
                    continue
            print("[Nueva conexion] Conectado a servidor.")
            
            self._recieveService.recieve(client)

