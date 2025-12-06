import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 50000

def receive_messages(secure_socket):
    while True:
        try:
            message = secure_socket.recv(1024).decode('utf-8')
            print(f"\n{message}")
        except:
            print("Conexão perdida.")
            secure_socket.close()
            break


def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_client = context.wrap_socket(client, server_hostname=HOST)

    try:
        secure_client.connect((HOST, PORT))
        print("Conectado ao Chat Seguro! Digite suas mensagens:")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(secure_client,))
    receive_thread.start()

    username = input("Escolha seu apelido: ")
    while True:
        text = input()
        if text.lower() == 'sair':
            break
        msg_final = f"{username}: {text}"
        secure_client.send(msg_final.encode('utf-8'))

    secure_client.close()


if __name__ == "__main__":
    main()