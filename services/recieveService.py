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
    BUFFER_SIZE = 10 * 1024 * 1024

    def recieve(self, socket):
        print("[STATUS] Esperando seleccion de archivo...")
        file_name = socket.recv(self.BUFFER_SIZE).decode(self._settings.FORMAT)
        file_size = int(socket.recv(self.BUFFER_SIZE).decode(self._settings.FORMAT))
        print(f"\n[CLIENT] Se recibira el archivo {file_name} de {file_size} bytes.")
        encrypted_key = socket.recv(self.BUFFER_SIZE)


        while True:
            staller = socket.recv(self.BUFFER_SIZE)
            if staller == b'listoparaenviar':
                break


        parts_needed = int(file_size / 100000000)
        if file_size % 100000000 != 0:
            parts_needed += 1
        print(f"[CLIENT] Recibiendo {parts_needed} partes encriptadas del archivo...")
        parts = []
        for i in tqdm(range(0, parts_needed)):
            # encrypted_part_size_size = socket.recv(self.BUFFER_SIZE)
            # print(encrypted_part_size_size)
            # encrypted_part_size_size = int(encrypted_part_size_size.decode(self._settings.FORMAT))
            encrypted_part_size = int(socket.recv(self.BUFFER_SIZE).decode(self._settings.FORMAT))
            while True:
                encrypted_part = socket.recv(encrypted_part_size)
                if encrypted_part_size == len(encrypted_part):
                    break
            parts.append(encrypted_part)
        print("[CLIENT] Partes recibidas.")


        print("\n[CLIENT] Desencriptando partes...")
        decrypted_parts = []
        for i in tqdm(range(0, len(parts))):
            decrypted_parts.append(self._encryptionService.decrypt("client", parts[i], encrypted_key))
        print("[CLIENT] Partes desencriptadas.")

        print("\n[CLIENT] Guardando partes en un archivo...")
        with open(file_name, "wb") as file:
            for i in tqdm(range(0, len(decrypted_parts))):
                file.write(decrypted_parts[i])
        file_location = os.getcwd()
        shutil.move(file_location+"/"+file_name,file_location+"/download/")
        file.close()
        print("[CLIENT] Archivo guardado.")

        print(f"\n[STATUS] Archivo creado exitosamente.")