import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import random
import secrets
from pathlib import Path
import time
from services.clearService import ClearService


class EncryptionService:
    _clearService = ClearService()

    def createKeypair(self, prefix: str):
        if (prefix== "client"): prefix2 = "server"
        else: prefix2 = "client"

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        filename = Path(f"./keys/{prefix}/private.pem")
        filename.touch()
        with open(filename, "wb") as f:
            f.write(private_pem)
        print(f"#Private key creada para {prefix}")

        filename = Path(f"./keys/{prefix2}/public.pem")
        filename.touch()
        with open(filename, "wb") as f:
            f.write(public_pem)
        print(f"#Public key creada para {prefix2}")
        

        print("\n\n#!Atencion!#")
        print(f"-Asegurarse que {prefix2} tenga la llave publica-")
        print(f"En caso contrario {prefix} no podra enviar archivos a {prefix2}")
        print("Ctrl + C para salir... (Esperando 10 segundos para proseguir)")
        time.sleep(9)
        self._clearService.clear()

        return self.openKeypair(prefix)

    def openKeypair(self, prefix: str):
        if (prefix== "client"): prefix2 = "server"
        else: prefix2 = "client"

        private_pem = Path(f"./keys/{prefix}/private.pem")
        public_pem = Path(f"./keys/{prefix}/public.pem")
        if private_pem.is_file() and public_pem.is_file():
            with open(private_pem, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            with open(public_pem, "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )
            # print(f"#Obtenidas llaves para {prefix}!")
            # self._clearService.clear()
            return private_key, public_key
        else:
            return self.createKeypair(prefix)


    def encrypt(self, prefix, data):
        public_key = self.openKeypair(prefix)[1]
        key = self.createAESKey()
        encrypted_data = base64.b64encode(self.encryptAES(key, data))
        encrypted_data = self.encryptAES(key, data)
        encrypted_key = base64.b64encode(public_key.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))
        return encrypted_data, encrypted_key

    def decrypt(self, prefix, key, encrypted):
        private_key = self.openKeypair(prefix)[0]
        key = base64.b64decode(key)
        key = private_key.decrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        data = self.decryptAES(key, encrypted)
        return data

    def createAESKey(self):
        key = AESGCM.generate_key(256)
        return key

    def encryptAES(self, key, data):
        nonce = secrets.token_bytes(12)
        data = nonce + AESGCM(key).encrypt(nonce, data, None)
        return data

    def decryptAES(self, key, data):
        data = AESGCM(key).decrypt(data[:12], data[12:], None)
        return data

    def largeFileEncrypt(self, prefix, data):
        # split data into chunks
        chunks = [data[i:i+1073741824] for i in range(0, len(data), 1073741824)]
        # encrypt each chunk
        encrypted_chunks = []
        encrypted_keys = []
        for chunk in chunks:
            print(f"#Encriptando chunk {chunks.index(chunk)} de {len(chunks)}")
            encrypted_chunk, encrypted_key = self.encrypt(prefix, chunk)
            encrypted_chunks.append(base64.b64decode(encrypted_chunk).decode())
            encrypted_keys.append(base64.b64decode(encrypted_key).decode())
        # join encrypted chunks
        encrypted_data = ','.join(encrypted_chunks)
        encrypted_keys = ','.join(encrypted_keys)


        return base64.b64encode(encrypted_data), base64.b64encode(encrypted_keys)

        # encrypted_data = ""
        # for chunk in encrypted_chunks:
        #     print(f"#Uniendo chunk {encrypted_chunks.index(chunk)+1} de {len(encrypted_chunks)}")
        #     encrypted_data += base64.b64encode(chunk).decode("utf-8")
        #     encrypted_data += ","
        # encrypted_key = ""
        # for key in encrypted_keys:
        #     encrypted_key += base64.b64encode(key).decode("utf-8")
        #     encrypted_key += ","
        

        return base64.b64encode(encrypted_data), base64.b64encode(encrypted_key)

    def largeFileDecrypt(self, prefix, key, encrypted):
        # split data into chunks
        encrypted_chunks = encrypted.split(b',')
        encrypted_keys = key.split(b',')
        # decrypt each chunk
        decrypted_chunks = []
        for chunk, key in zip(encrypted_chunks, encrypted_keys):
            print(f"#Desencriptando chunk {encrypted_chunks.index(chunk)+1} de {len(encrypted_chunks)}")
            print(f"#DATA: {chunk}")
            decrypted_chunks.append(self.decrypt(prefix, key, chunk))
        # join decrypted chunks
        decrypted_data = b''
        for chunk in decrypted_chunks:
            decrypted_data += chunk
        return decrypted_data

        
