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
    serverPublicKey = None
    serverPrivateKey = None
    clientPublicKey = None
    clientPrivateKey = None

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
        time.sleep(10)
        print("\n\n\n\n\n\n\n\n")

        return self.openKeypair(prefix)

    def openKeypair(self, prefix: str):
        if (prefix== "client"): 
            prefix2 = "server"
            if (self.clientPrivateKey != None and self.serverPublicKey != None):
                return self.clientPrivateKey, self.serverPublicKey
        else: 
            prefix2 = "client"
            if (self.serverPrivateKey != None and self.clientPublicKey != None):
                return self.serverPrivateKey, self.clientPublicKey
        
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
            return private_key, public_key
        else:
            return self.createKeypair(prefix)

    def encrypt(self, prefix, data, key = None, onlyKey = False):
        """
        Encripta llave con RSA y envia datos a encriptar con AES
        :param onlyKey: True para retornar solo encrypted_key, sirve para cuando se quiere crear key para mas de un archivo
        """
        public_key = self.openKeypair(prefix)[1]
        if (key == None ): key = self.createAESKey()
        encrypted_key = public_key.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        if (onlyKey == True): return encrypted_key
        else: 
            encrypted_data = self.encryptAES(data, key)
            return encrypted_data, encrypted_key

    def decrypt(self, prefix, encrypted_data, encrypted_key):
        private_key = self.openKeypair(prefix)[0]
        key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        data = self.decryptAES(encrypted_data, key)
        return data






    def createAESKey(self):
        key = AESGCM.generate_key(256)
        return key

    def encryptAES(self, data, key):
        nonce = secrets.token_bytes(12)
        data = nonce + AESGCM(key).encrypt(nonce, data, b'')
        return data

    def decryptAES(self, data, key):
        data = AESGCM(key).decrypt(data[:12], data[12:], b'')
        return data