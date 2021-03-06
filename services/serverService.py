import os
import socket
from configuration.Settings import Settings
from services.sendService import SendService
from services.clearService import ClearService

class ServerService:
    _sendService = SendService()
    _clearService = ClearService()

    ip = Settings.IP
    port = Settings.PORT
    addr = Settings.ADDR

    def startServer(self):
        self._clearService.clear()
        print(f"Se inicia el servidor en {self.ip}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(self.addr)
            server.listen()
            client, addr = server.accept()

            print(f"[Nueva conexion] {addr[0]} se ha conectado.")
            self._sendService.send(client)

            client.close()
            server.close()
            print("[SERVER] *Conexion cerrada.*")
        

