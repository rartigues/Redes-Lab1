from fileinput import filename
import socket
import os       #os nos permite usar seek() en file para poder saber la cantidad de bytes
import ntpath
from time import process_time_ns   #para que imprima el nombre del archivo independiente del archivo que se elija

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def getFile():
    # Abriendo y leyendo la informacion del archivo
    #ciclo el cual revisa que el input de la localizacion y el archivo exista
    while True:
        filelocation = input("Introduzca la localizacion del archivo: ")
        filename = input("Introduzca el nombre del archivo: ")
        path=filelocation+filename
        if(os.path.isfile(path)):
            file = open(filelocation+filename, "rb")
            return file,filename
        os.system('clear')
        print("Localizacion o nombre del archivo incorrecto.\nIntente nuevamente...")
    

def main():
    os.system('clear')
    # Iniciando el socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectando al servidor
    client.connect(ADDR)

    #file,filename=getFile()

    file=open("ejemplo/funcionaxd.png","rb")
    filename=("funcionaxd.png")

    data = file.read()
    size = file.seek(0, os.SEEK_END)
    print("1")

    # Se envia el nombre del archivo al server
    client.send(filename.encode(FORMAT))
    print("1")
    client.send(str(SIZE).encode(FORMAT))
    print("1")
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    print("1")
    # Se envia la informacion del archivo al server
    client.send((data))#.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    # Cerrando el archivo 
    file.close()

    # Cerrando la conexion con el servidor 
    client.close()


if __name__ == "__main__":
    main()