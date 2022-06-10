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
        key = socket.recv(self.BUFFER_SIZE)

        with open(file_name, "wb") as file:
            file_temp = []
            # Recieve parts (each part 100MB)
            for i in range(0, file_size, 100000000):
                part = socket.recv(self.BUFFER_SIZE)
                file_temp.append(part)
            # Decrypt parts
            for i in range(0, len(file_temp)):
                file_temp[i] = self._encryptionService.decrypt("client", key, file_temp[i])
            # Concatenate parts
            file_temp = b''.join(file_temp)
            # Write file
            file.write(file_temp)


            


            # tqdm_bar = tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

            # for i in range(0, file_size, self.BUFFER_SIZE):
            #     print(i)
            #     data = socket.recv(self.BUFFER_SIZE)
            #     tqdm_bar.update(len(data))
            #     if not data:
            #         break
            #     # progressBarr(parts/file_size*100)
            #     print(data)
            #     data = self._encryptionService.decrypt("client", key, data)
            #     file_temp.append(data)

            # print("[CLIENT] Archivo recibido.")
            # tqdm_bar.close()
            # if file_size > 2.1*1024*1024*1024:
            #     print("[CLIENT] El archivo es muy grande para ser enviado!!! **BETA**")
            #     return
            #     #data = b''.join(file_temp)
            #     #file.write(self._encryptionService.largeFileDecrypt("client", key, data))
            # else:
            #     file.write(b''.join(file_temp))
        file_location = os.getcwd()
        shutil.move(file_location+"/"+file_name,file_location+"/download/")
        file.close()
        print(f"[Estado del Archivo] Archivo creado exitosamente.")



