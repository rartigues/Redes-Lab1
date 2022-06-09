import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path


class EncryptionService:

    def createKeypair(self, prefix: str):
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

        with open(f"../keys/{prefix}/private.pem", "wb") as f:
            f.write(private_pem)

        with open(f"../keys/{prefix}/public.pem", "wb") as f:
            f.write(public_pem)

        return self.openKeypair(prefix)

    def openKeypair(self, prefix: str):
        # check if private.pem or public.pem exists
        private_pem = Path(f"../keys/{prefix}/private.pem")
        public_pem = Path(f"../keys/{prefix}/public.pem")
        if private_pem.is_file() and public_pem.is_file():
            with open("private.pem", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            with open("public.pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )
            return private_key, public_key
        else:
            return self.createKeypair(prefix)

    def encrypt(self, public_key, plaintext):
        encrypted = base64.b64encode(public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))
        return encrypted

    def decrypt(self, private_key, encrypted):
        decrypted = private_key.decrypt(
            base64.b64decode(encrypted),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted
    
