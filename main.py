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
    # Recibiendo el nombre del archivo del cliente
    # Recibiendo el tamaño del archivo

    name = (Emo.recv(SIZE)).decode(FORMAT)
    #decode in base 64 the size of the file
    Emo.send("[SERVER] Archivo recibido".encode(FORMAT))
    size = (Emo.recv(SIZE)).decode(FORMAT)
    Emo.send("[SERVER] Nombre recibido".encode(FORMAT))
    print(f"[RECV] Nombre del archivo = {name}")
    print(f"[RECV] Tamaño del archivo = {size} bytes")
    # Recibindo la informacion del archivo del cliente
    tqdm_bar=tqdm(total=int(size), unit="B", unit_scale=True, unit_divisor=SIZE)
    parts = []
    with open(name, "wb") as file:
        #create a for that will receive the data by parts of SIZE
        for i in range(0, int(size), SIZE):
            part = Emo.recv(int(size))
            parts.append(part)
            tqdm_bar.update(len(part))
        file.write(b"".join(parts))
    tqdm_bar.close()
    file_location= os.getcwd()
    shutil.move(file_location+"/"+name,file_location+"/saves/")

    # Cerrando el Archivo
    file.close()
    print(f"[Estado del Archivo] Archivo creado exitosamente.")

def sendFile(client):
    fileDir=askopenfilename(initialdir="~")
    filedirarray = fileDir.split("/")
    filename = filedirarray[len(filedirarray)-1]
    with open(fileDir,"rb") as file:            
        data = file.read()
        size = file.seek(0, os.SEEK_END)
        #print the filename and size of the file
        print(f"[SEND] Nombre del archivo = {filename}")
        print(f"[SEND] Tamaño del archivo = {size} bytes")

        # Se envia el nombre del archivo al server
        client.send(filename.encode(FORMAT))            #1 SEND

        # Respuesta sobre el nombre del archivo
        msg=client.recv(SIZE).decode(FORMAT)            #2 RECV
        print(msg)
        # Se envia el tamano del archivo al server
        client.send(str(size).encode(FORMAT))           #3 SEND
        
        # Respuesta sobre el tamaño del archivo
        msg=client.recv(SIZE).decode(FORMAT)            #4 RECV
        print(msg)

        # Se envia la informacion del archivo al server
        #divide data in parts of SIZE
        parts = [data[i:i+SIZE] for i in range(0, len(data), SIZE)]
        for part in tqdm(parts):
            client.send(part, SIZE)
        print(f"[Estado del Archivo] Archivo enviado exitosamente.")
        # Cerrando el archivo
        file.close()

def SendFunction():
    #create a socket that waits for a connection

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDR)
            #make it listen until a connection is made
            s.listen()
            #accept the connection
            client, addr = s.accept()
            print(f"[Nueva conexion] {addr[0]} se ha conectado.")
            sendFile(client)
            #close the connection
            client.close()


    
    
def RecvFunction():
    #create a socket that joins a connection
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
