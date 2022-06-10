from services.encryptionService import EncryptionService
from services.clearService import ClearService
from configuration.Settings import Settings
import os
import shutil
from tqdm import tqdm

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
            tqdm_bar = tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
            key = socket.recv(self.BUFFER_SIZE)
            for i in range(0, file_size, self.BUFFER_SIZE):
                data = socket.recv(self.BUFFER_SIZE)
                tqdm_bar.update(len(data))
                if not data:
                    break
                parts += 1
                # progressBarr(parts/file_size*100)
                file_temp.append(data)

            print("[CLIENT] Archivo recibido.")
            tqdm_bar.close()
            if file_size > 2.1*1024*1024*1024:
                print("[CLIENT] El archivo es muy grande para ser enviado!!! **BETA**")
                return
                #data = b''.join(file_temp)
                #file.write(self._encryptionService.largeFileDecrypt("client", key, data))
            else:
                file.write(self._encryptionService.decrypt("client", key,b"".join(file_temp)))
        file_location = os.getcwd()
        shutil.move(file_location+"/"+file_name,file_location+"/download/")
        file.close()
        print(f"[Estado del Archivo] Archivo creado exitosamente.")


    


