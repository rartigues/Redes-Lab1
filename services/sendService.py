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
    BUFFER_SIZE = 1024

    def send(self, socket):
        # Seleccionar archivo para enviar
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print(f"Se selecciono el archivo {file_name} de {file_size} bytes.")
        self._clearService.clear()

        # if file_size > 2.1GB split file
        bigFile = False
        if file_size > 2.1*1024*1024*1024:
            print("[SERVER] El archivo es muy grande para ser enviado!!!!")
            return
            # bigFile = True


        # Enviando el nombre del archivo
        socket.send(file_name.encode(self._settings.FORMAT))
        print("[SERVER] Nombre del archivo enviado.")

        # Enviando el tamaño del archivo
        socket.send(str(file_size).encode(self._settings.FORMAT))
        print("[SERVER] Tamaño del archivo enviado.")

        # Enviando el archivo
        self._encryptionService.openKeypair("server")
        key = self._encryptionService.createAESKey()
        encrypted_key = self._encryptionService.encrypt("server", None, key, True)[1]
        socket.send(encrypted_key)
        with open(file_path, "rb") as file:
            data = file.read()
            parts= [data[i:i+100000000 ] for i in range(0, len(data), 100000000 )]
            #encrypt parts
            for i in range(0, len(parts)):
                parts[i] = self._encryptionService.encrypt("server", parts[i], key)[0]
            #send parts
            for i in range(0, len(parts)):
                socket.send(parts[i])



            # bar_encrypt = tqdm(total=len(parts), unit="B", unit_scale=True, unit_divisor=1024)    
            # #encrypt elements of parts
            # print("[SERVER] Encriptando archivo...")
            # for part in tqdm(parts):
            #     parts[part] = self._encryptionService.encrypt("server", parts[part], key)[0]
            # print(parts[0])
            
            # print("[SERVER] Transferiendo archivo...")
            # for part in tqdm(parts):
            #     socket.send(part)
            print("[SERVER] Archivo enviado.")
        file.close()



