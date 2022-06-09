from services.encryptionService import EncryptionService
from services.clearService import ClearService
from configuration.Settings import Settings
import os
import shutil

class RecieveService:
    _encryptionService = EncryptionService()
    _clearService = ClearService()
    _settings = Settings()
    BUFFER_SIZE = 1024

    def recieve(self, socket):

        file_name = socket.recv(self.BUFFER_SIZE).decode(self._settings.FORMAT)
        file_size = int(socket.recv(self.BUFFER_SIZE).decode(self._settings.FORMAT))

        print(f"Se recibira el archivo {file_name} de {file_size} bytes.")
        self._clearService.clear()

        # Recieve file
        self._encryptionService.openKeypair("client")
        with open(file_name, "wb") as file:
            parts= 0
            file_temp = []
            key = socket.recv(self.BUFFER_SIZE)
            while True:
                data = socket.recv(self.BUFFER_SIZE)
                if not data:
                    break
                parts += 1
                # progressBarr(parts/file_size*100)
                file_temp.append(data)
            print("[CLIENT] Archivo recibido.")
            file.write(self._encryptionService.decrypt("client", key,b"".join(file_temp)))

        file_location = os.getcwd()
        shutil.move(file_location+"/"+file_name,file_location+"/download/")
        file.close()
        print(f"[Estado del Archivo] Archivo creado exitosamente.")


    


