class Network():

    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port

    def connect_to_server(self, client_socket):
        client_socket.connect((self.host_ip, self.port))

    def send_to_server(self, client_socket, message):
        #message sent to server
        client_socket.send(message.encode('ascii'))

    def send_to_clients(self, list_clients, message):
        #list_client = liste contennat tout les sockets des clients

        #message to all clients
        for client in list_clients:
            cli