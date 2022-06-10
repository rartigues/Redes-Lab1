from services.serverService import ServerService
from services.clientService import ClientService
import sys


def main():
    if(len(sys.argv)>2):
        print("[ERROR] El numero de argumentos es incorrecto.")
        sys.exit()
    elif(len(sys.argv)<2):
        print("[ERROR] No se ha ingresado ningun argumento.")
        sys.exit()
    elif(len(sys.argv)==2):
        if(sys.argv[1]=="-s"):
            ServerService().startServer()
        elif(sys.argv[1]=="-r"):
            ClientService().startClient()
        else:
            print("[ERROR] Argumento incorrecto.")
            sys.exit()
    return 0





if __name__ == "__main__":
    main()