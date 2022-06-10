import socket
import os
import base64
import tkinter
from tkinter.filedialog import askopenfilename
import sys
import shutil
import argparse
from tqdm import tqdm

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def recvFile(Emo):
    os.system('clear')
    name = (Emo.recv(SIZE)).decode(FORMAT)
    Emo.send("[SERVER] Archivo recibido".encode(FORMAT))
    size = (Emo.recv(SIZE)).decode(FORMAT)
    Emo.send("[SERVER] Nombre recibido".encode(FORMAT))
    print(f"[RECV] Nombre del archivo = {name}")
    print(f"[RECV] Tamaño del archivo = {size} bytes")
    with open(name, "wb") as file:
        tqdm_bar=tqdm(total=int(size), unit="B", unit_scale=True, unit_divisor=SIZE)
        parts = []
        for i in range(0, int(size), SIZE):
            part = Emo.recv(int(size))
            parts.append(part)
            tqdm_bar.update(len(part))
        file.write(b"".join(parts))
    tqdm_bar.close()
    file_location= os.getcwd()
    shutil.move(file_location+"/"+name,file_location+"/saves/")
    file.close()
    print(f"[Estado del Archivo] Archivo creado exitosamente.")
def sendFile(client):
    fileDir=askopenfilename(initialdir="~")
    filedirarray = fileDir.split("/")
    filename = filedirarray[len(filedirarray)-1]
    with open(fileDir,"rb") as file:            
        data = file.read()
        size = file.seek(0, os.SEEK_END)
        print(f"[SEND] Nombre del archivo = {filename}")
        print(f"[SEND] Tamaño del archivo = {size} bytes")
        client.send(filename.encode(FORMAT))
        msg=client.recv(SIZE).decode(FORMAT)
        print(msg)
        client.send(str(size).encode(FORMAT))
        msg=client.recv(SIZE).decode(FORMAT)
        print(msg)
        parts = [data[i:i+SIZE] for i in range(0, len(data), SIZE)]
        for part in tqdm(parts):
            client.send(part, SIZE)
        print(f"[Estado del Archivo] Archivo enviado exitosamente.")
        file.close()
def SendFunction():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDR)
            s.listen()
            client, addr = s.accept()
            print(f"[Nueva conexion] {addr[0]} se ha conectado.")
            sendFile(client)
            client.close()
def RecvFunction():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected=False
        while not connected:
            try:
                s.connect(ADDR)
                connected=True
            except:
                connected=False
        print("se logro la conexion digo yo cliente")
        recvFile(s)
        s.close()
def main():
    if(len(sys.argv)>2):
        print("[ERROR] El numero de argumentos es incorrecto.")
        sys.exit()
    elif(len(sys.argv)<2):
        print("[ERROR] No se ha ingresado ningun argumento.")
        sys.exit()
    elif(len(sys.argv)==2):
        if(sys.argv[1]=="-s"):
            SendFunction()
        elif(sys.argv[1]=="-r"):
            RecvFunction()
        else:
            print("[ERROR] Argumento incorrecto.")
            sys.exit()
    return 0
if __name__ == "__main__":
    main()
