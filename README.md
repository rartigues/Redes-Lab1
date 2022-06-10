# Laboratorio 1 Redes de Computadores
Entrega de laboratorio 1 hecha en Python por Roberto Artigues y Emilio Meza
> **Nota:** poca RAM disponible en archivos grandes puede bugear la transferencia


## Setup

### Requerimientos
##### Python3
```
sudo apt install python3 python3-tk
```
##### pip 
```
pip install -r requirements.txt
```

### Archivo .env
Primero se tiene que modificar archivo `.env.example` y guardar como `.env`

###### Ejemplo:
```
IP = localhost
PORT = 5252
```
> **Nota:** IP y PORT seran utilizadas por el servidor

---
## Instrucciones de uso
Solo se debe ejecutar `main.py` agregando -s o -r para indicar si hara send(servidor) o recieve(cliente)


###### Servidor:
```console
python main.py -s
```
###### Cliente:
```console
python main.py -r
```



