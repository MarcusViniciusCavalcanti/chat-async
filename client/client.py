import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9006))

is_listened = True


def start_chat(sock):
    while is_listened:
        expected_data_size = int(sock.recv(4).decode())

        received_data = ''
        while len(received_data) < expected_data_size:
            received_data += sock.recv(4).decode()

        print(received_data)
        print("\nmessage:")


listener = threading.Thread(target=start_chat, args=(sock,))
listener.setDaemon(True)
listener.start()

self_message = ''

while self_message != 'see ya':
    message = raw_input("message: \n").strip()
    self_message = message
    length = len(message)

    sock.sendall(str(length).zfill(4).encode())
    sock.sendall(message.encode())

is_listened = False
print("\ndisconnected from server!")
sock.close()
