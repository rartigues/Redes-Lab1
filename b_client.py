import socket
import os
import base64
from tkinter.filedialog import askopenfilename
import sys
import shutil

IP=socket.gethostbyname(socket.gethostname())
PORT=4455
ADDR=(IP,PORT)
#SIZE=8192
FORMAT="utf-8"

def progressBarr(percent):
    if percent == 100:
        text=(f"[##################################################]{percent}%")
    elif(percent>=90):
        text=(f"[############################################______]{percent}%")
    elif(percent>=80):
        text=(f"[########################################__________]{percent}%")
    elif(percent>=70):
        text=(f"[###################################_______________]{percent}%")
    elif(percent>=60):
        text=(f"[##############################____________________]{percent}%")
    elif(percent>=50):
        text=(f"[#########################_________________________]{percent}%")
    elif(percent>=40):
        text=(f"[####################______________________________]{percent}%")
    elif(percent>=30):
        text=(f"[###############___________________________________]{percent}%")
    elif(percent>=20):
        text=(f"[##########________________________________________]{percent}%")
    elif(percent>=10):
        text=(f"[#####_____________________________________________]{percent}%")
    elif(percent>=0):
        text=(f"[__________________________________________________]{percent}%")
    sys.stdout.write("\r")
    sys.stdout.write(text)
    if(percent==100):
        sys.stdout.write("\n")
    sys.stdout.flush()  

def sendFile(client):
    fileDir=askopenfilename(initialdir="~")
    filedirarray = fileDir.split("/")
    filename = filedirarray[len(filedirarray)-1]
    with open(fileDir,"rb") as file:            
        data = file.read()
        size = file.seek(0, os.SEEK_END)

        # Se envia el nombre del archivo al server
        client.send(filename.encode(FORMAT))            #1 SEND

        # Respuesta sobre el nombre del archivo
        msg=client.recv(8192).decode(FORMAT)            #2 RECV
        print(msg)
        # Se envia el tamano del archivo al server
        client.send(str(size).encode(FORMAT))           #3 SEND
        
        # Respuesta sobre el tamaño del archivo
        msg=client.recv(8192).decode(FORMAT)            #4 RECV
        print(msg)

        # Se envia la informacion del archivo al server
        client.sendall(data)                               #6 SEND

        # Cerrando el archivo
        file.close()

def recvFile(Emo):
    os.system('clear')
    # Recibiendo el nombre del archivo del cliente
    # Recibiendo el tamaño del archivo

    name = Emo.recv(8192).decode(FORMAT)
    size = Emo.recv(8192).decode(FORMAT)

    print(f"[RECV] Nombre del archivo = {name}")
    print(f"[RECV] Tamaño del archivo = {size} bytes")

    repeticiones = int((int(size) / 8192)+1)


    # Recibindo la informacion del archivo del cliente
    parts = []
    with open(name, "wb") as file:
        while True:
            chunk = Emo.recv(int(size))
            if not chunk:
                break
            parts.append(chunk)
            progressBarr(len(parts)/repeticiones*100)
        file.write(b"".join(parts))
        
    file_location= os.getcwd()
    shutil.move(file_location+"/"+name,file_location+"/saves/")

    # Cerrando el Archivo
    file.close()
    print(f"[Estado del Archivo] Archivo creado exitosamente.")

def main():
    os.system('clear')
    # Iniciando el socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectando al servidor
    client.connect(ADDR)

    msg=client.recv(8192).decode(FORMAT)
    print(msg)
    
    answer=input()
    client.send(answer.encode(FORMAT))
    if(answer=="1"):
        sendFile(client)
    elif(answer=="2"):
        recvFile(client)
    else:
        return("Error la opcion no existe")    
    # Cerrando la conexion con el servidor
    client.close()

if __name__ == "__main__":
    main()