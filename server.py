import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def create_a_barr(porcentage):
def recvall(sock,size):
    BUFF_SIZE = int(size) 
    data = b''
    while True:
        part = sock.recv(int(size))
        data += part
        print(f"{(BUFF_SIZE/int(size))*100}%")
        if (len(part) < BUFF_SIZE):
            # either 0 or end of data
            break
    return data

def main():
    #os.system('clear')
    print(ADDR[0])
    print("[Iniciando] El server esta iniciando...")
    #inicializando el TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bindeamos la ip y puerto al servidor
    server.bind(ADDR)

    # Server esta esperando para que el cliente se conecte
    server.listen()

    print("[Esperando conexion...] El server esta esperando conexion.")

    while True:
        # El server ha aceptado la conexion del cliente
        conn, addr = server.accept()
        type(conn)
        print(f"[Nueva conexion] {addr} se ha conectado.")

        print("1")

        # Recibiendo el nombre del archivo del cliente
        
        filename = conn.recv(SIZE).decode(FORMAT)
        filesize = conn.recv(SIZE).decode(FORMAT)
        print("1")

        print(f"[RECV] Recibiendo el nombre del archivo.")
        print(f"Nombre del archivo = {filename}")
        print(f"Tamagno del archivo = {filesize} bytes")

        file = open(filename, "wb")
        print("1")

        
        conn.send("Nombre del archivo recibido.\n".encode(FORMAT))
        print("1")

        # Recibindo la informacion del archivo del cliente
        #data = recvall(conn,filesize)
        data = conn.recv(SIZE)#.decode(FORMAT)
        print("1")

        print(f"[RECV] Recibiendo la informacion del archivo.")
        #print(f"Informacion del archivo = {data}")

        

        file.write(data)

        conn.send("La informacion del archivo ha sido recibida".encode(FORMAT))

        # Cerrando el Archivo

        file.close()

        # Cerrando la conexion con el cliente 
        conn.close()

        print(f"[Desconectado] {addr} se ha desconectado.")

if __name__ == "__main__":
    main()