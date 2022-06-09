import base64
from services.encryptionService import EncryptionService
from services.clearService import ClearService
from configuration.Settings import Settings
import os
import tkinter
from tkinter import filedialog

class SendService:
    _encryptionService = EncryptionService()
    _clearService = ClearService()
    _settings = Settings()

    def send(self, socket):
        # Seleccionar archivo para enviar
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print(f"Se selecciono el archivo {file_name} de {file_size} bytes.")
        self._clearService.clear()

        # if file_size > 2.1GB split file
        if file_size > 2.1*1024*1024*1024:
            print("[SERVER] El archivo es muy grande para ser enviado.")
            return


        # Enviando el nombre del archivo
        socket.send(file_name.encode(self._settings.FORMAT))
        print("[SERVER] Nombre del archivo enviado.")

        # Enviando el tamaño del archivo
        socket.send(str(file_size).encode(self._settings.FORMAT))
        print("[SERVER] Tamaño del archivo enviado.")

        # Enviando el archivo
        self._encryptionService.openKeypair("server")
        with open(file_path, "rb") as file:
            data = file.read()
            data, key = self._encryptionService.encrypt("server", data)
            socket.send(key)
            socket.send(data)
            print("[SERVER] Archivo enviado.")
        file.close()



