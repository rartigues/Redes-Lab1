#include "tcp.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

void tcp_server_create(struct tcp_server_t *server, int port) {
    // Crear socket de escucha (se guarda en server->listen_sock)

    // Bindear socket a puerto

    // Escuchar conexiones entrantes
}

int tcp_server_accept(struct tcp_server_t *server,
                      struct sockaddr_in *client_addr) {
    // Aceptar primera conexion entrante (guardar dirección del cliente en
    // client_addr)

    // Retorna descriptor de archivo del socket de comunicación con el cliente
}

void tcp_client_connect(struct tcp_client_t *client, const char *host,
                        int port) {
    // Crear socket de cliente (se guarda en client->sock)

    // Conectar con host y puerto indicados (se guarda en client->server_addr y
    // se usa en llamada a connect())
}

void tcp_send(int sock, const void *data, size_t size) {
}

void tcp_recv(int sock, void *data, size_t size) {
}

void tcp_close(int sock) {
    close(sock);
}
