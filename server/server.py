import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 9006))
sock.listen(0)


def listen_client(current_client):
    current_client_last_message = ''

    while current_client_last_message != 'see ya':
        expected_data_size = ''
        while expected_data_size == '':
            expected_data_size += current_client.connection.recv(4).decode()
        expected_data_size = int(expected_data_size)

        received_data = ''
        while len(received_data) < expected_data_size:
            received_data += current_client.connection.recv(4).decode()

            formatted_message = ''
            if received_data == 'see ya':
                formatted_message = "Client {0}: {1}".format(current_client.address, 'disconnected from chat')
            else:
                formatted_message = "Client {0}: {1}".format(current_client.address, received_data)

        current_client_last_message = received_data
        print(formatted_message)

        for socket_connection in connections:
            if socket_connection != current_client:
                socket_connection.connection.sendall(str(len(formatted_message)).zfill(4).encode())
                socket_connection.connection.sendall(formatted_message.encode())

    connections.remove(current_client)
    current_client.connection.close()


last_message = ''
connections = []


class Connection:
    connection = ''
    address = ''

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address


is_continue_chat = True

while is_continue_chat:
    print("Await connection")
    connection, address_client = sock.accept()
    new_connection = Connection(connection, address_client)
    connections.append(new_connection)
    print("{} connected".format(new_connection.address))

    worker = threading.Thread(target=listen_client, args=(new_connection,))
    worker.setDaemon(True)
    worker.start()

    message = raw_input("message: \n").strip()
    if message == 'disconnect':
        is_continue_chat = False

sock.close()
