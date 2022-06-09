import socket
import os
import base64
from tkinter.filedialog import askopenfilename
import sys
import shutil
import argparse
import tqdm


IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
#SIZE = 8192
FORMAT = "utf-8"

def progressBarr(percent):
    if percent == 100:
        text=(f"[##################################################]{'%.2f' %percent}%")
    elif(percent>=90):
        text=(f"[############################################______]{'%.2f' %percent}%")
    elif(percent>=80):
        text=(f"[########################################__________]{'%.2f' %percent}%")
    elif(percent>=70):
        text=(f"[###################################_______________]{'%.2f' %percent}%")
    elif(percent>=60):
        text=(f"[##############################____________________]{'%.2f' %percent}%")
    elif(percent>=50):
        text=(f"[#########################_________________________]{'%.2f' %percent}%")
    elif(percent>=40):
        text=(f"[####################______________________________]{'%.2f' %percent}%")
    elif(percent>=30):
        text=(f"[###############___________________________________]{'%.2f' %percent}%")
    elif(percent>=20):
        text=(f"[##########________________________________________]{'%.2f' %percent}%")
    elif(percent>=10):
        text=(f"[#####_____________________________________________]{'%.2f' %percent}%")
    elif(percent>=0):
        text=(f"[__________________________________________________]{'%.2f' %percent}%")
    sys.stdout.write("\r")
    sys.stdout.write(text)
    if(percent==100):
        sys.stdout.write("\n")
    sys.stdout.flush()  
def recvFile(Emo):
    os.system('clear')
    # Recibiendo el nombre del archivo del cliente
    # Recibiendo el tamaño del archivo

    name = str(Emo.recv(8192).decode(FORMAT))
    size = str(Emo.recv(8192).decode(FORMAT))

    print(f"[RECV] Nombre del archivo = {name}")
    print(f"[RECV] Tamaño del archivo = {size} bytes")

    repeticiones = int((float(size) / 8192)+1)

    # Recibindo la informacion del archivo del cliente
    parts = []
    percentage=tqdm.tqdm(total=repeticiones)
    with open(name, "wb") as file:
        while True:
            chunk = Emo.recv(int(size))
            if not chunk:
                break
            parts.append(chunk)
            percentage.update(1)            
            #progressBarr(len(parts)/repeticiones*100)
        file.write(b"".join(parts))
    percentage.close()
    file_location= os.getcwd()
    shutil.move(file_location+"/"+name,file_location+"/saves/")

    # Cerrando el Archivo
    file.close()
    print(f"[Estado del Archivo] Archivo creado exitosamente.")

def sendFile(client):
    print(f"[Nueva conexion] {ADDR[0]} se ha conectado.")
    fileDir=askopenfilename(initialdir="~")
    filedirarray = fileDir.split("/")
    filename = filedirarray[len(filedirarray)-1]
    with open(fileDir,"rb") as file:            
        data = file.read()
        size = file.seek(0, os.SEEK_END)    

        # Se envia el nombre del archivo al server
        client.send(filename.encode(FORMAT))

        # Respuesta sobre el nombre del archivo
        # Se envia el tamano del archivo al server
        client.send(str(size).encode(FORMAT))
        
        # Respuesta sobre el tamaño del archivo

        # Se envia la informacion del archivo al server
        client.send(data)
        
        # Respuesta sobre la informacion del archivo

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








    # Inicializando el TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bindeamos la ip y puerto al servidor
    server.bind(ADDR)
    
    # Server esta esperando para que el cliente se conecte
    server.listen()
    
    print("[Esperando conexion...] El server esta esperando conexion.")

    while True:
        # El server ha aceptado la conexion del cliente
        Emo,addr = server.accept()
        type(Emo)

        #si se quiere hacer algo tiene que ser desde aca
        Emo.send("[SERVER] Que deseas hacer?\n[SERVER] 1-Enviar Archivo\n[SERVER] 2-Recibir Archivo".encode(FORMAT))

        answer=Emo.recv(8192).decode(FORMAT)
        if(answer=="1"):
            recvFile(Emo)
        elif(answer=="2"):
            sendFile(Emo)
        else:
            print("[SERVER] opcion no valida\n")


        # Cerrando la conexion con el cliente 
        Emo.close()
        print(f"[Desconectado] {addr} se ha desconectado.")

if __name__ == "__main__":
    main()
