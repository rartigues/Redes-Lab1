import base64
from services.encryptionService import EncryptionService
from services.clearService import ClearService
from configuration.Settings import Settings
import os
import tkinter
from tkinter import filedialog
from tqdm import tqdm


class SendService:
    _encryptionService = EncryptionService()
    _clearService = ClearService()
    _settings = Settings()

    def send(self, socket):
        print("[STATUS] Esperando seleccion de archivo...")
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        if(file_path == ""):
            socket.send("///cancelado!///".encode(self._settings.FORMAT))
            print("[STATUS] *Cancelado*")
            return
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print(f"Se selecciono el archivo {file_name} de {file_size} bytes.")


        socket.send(file_name.encode(self._settings.FORMAT))
        print("\n[SERVER] Nombre del archivo enviado.")
        socket.send(str(file_size).encode(self._settings.FORMAT))
        print("[SERVER] Tamaño del archivo enviado.")

        # Enviando el archivo
        key = self._encryptionService.createAESKey()
        encrypted_key = self._encryptionService.encrypt("server", None, key, True) # Solo retorna el key encriptado
        socket.send(encrypted_key)
        print("[SERVER] Key encriptada enviada.")
        with open(file_path, "rb") as file:
            print("\n[STATUS] Abriendo archivo...")
            data = file.read()
            print("[STATUS] Archivo abierto.")

            if file_size > 100000000:
                parts = []
                for i in range(0, file_size, 100000000):
                    parts.append(data[i:i+100000000])
            else:
                parts = [data]
            
            socket.send(b'listoparaenviar')
            
            print("\n[SERVER] Enviando archivo...")
            for i in tqdm(range(0, len(parts))):
                part = parts[i]
                encrypted_part = self._encryptionService.encrypt("server", part, key)[0]
                encrypted_part_size = str(len(encrypted_part)).encode(self._settings.FORMAT)
                # socket.send(str(len(encrypted_part_size)).encode(self._settings.FORMAT)) # Con archivos muy grande puede fallar sin esto
                socket.send(encrypted_part_size)
                socket.send(encrypted_part)
            print("[SERVER] Archivo enviado.")
        file.close()



