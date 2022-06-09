import socket
import os
import base64
from tkinter.filedialog import askopenfilename
import sys
import shutil

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
    print(f"[Nueva conexion] {ADDR[0]} se ha conectado.")

    # Recibiendo el nombre del archivo del cliente
    # Recibiendo el tamaño del archivo

    name = Emo.recv(8192).decode(FORMAT)                                    # 1 RECV
    Emo.send("[SERVER] Nombre del archivo recibido.\n".encode(FORMAT))      # 2 SEND
    size = Emo.recv(8192).decode(FORMAT)                                    # 3 RECV
    Emo.send("[SERVER] Tamaño del archivo recibido.\n".encode(FORMAT))      # 4 SEND

    print(f"[RECV] Nombre del archivo = {name}")
    print(f"[RECV] Tamaño del archivo = {size} bytes")

    #total de repeticiones a ralizar
    repeticiones = int((int(size) / 8192)+1)
    porcentaje=0
    # Recibindo la informacion del archivo del cliente
    parts = []
    
    with open(name, "wb") as file:
        while True:
            data = Emo.recv(8192)       # 6 RECV
            progressBarr(len(parts)/repeticiones*100)                                    
            if not data:
                break
            parts.append(data)
            

        file.write(b"".join(parts))

    Emo.sendall("[SERVER] Archivo recibido.\n".encode(FORMAT))

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
        msg=client.recv(8192).decode(FORMAT)
        print(msg)
        # Se envia el tamano del archivo al server
        client.send(str(size).encode(FORMAT))
        
        # Respuesta sobre el tamaño del archivo
        msg=client.recv(8192).decode(FORMAT)
        print(msg)

        # Se envia la informacion del archivo al server
        client.send(data)
        
        # Respuesta sobre la informacion del archivo
        msg=client.recv(8192).decode(FORMAT)
        print(msg)

        # Cerrando el archivo
        file.close()

def main():
    os.system('clear')
    print("[Iniciando] El server esta iniciando...")
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
