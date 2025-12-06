import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 50000

clients = []

def broadcast(message, _client_socket):
    for client in clients:
        if client != _client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break


def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    secure_server = context.wrap_socket(server, server_side=True)

    print(f"Servidor Seguro rodando em {HOST}:{PORT}...")

    while True:
        client_sock, addr = secure_server.accept()
        clients.append(client_sock)

        print(f"Nova conexão segura estabelecida com: {addr}")

        thread = threading.Thread(target=handle_client, args=(client_sock,))
        thread.start()

if __name__ == "__main__":
    main()