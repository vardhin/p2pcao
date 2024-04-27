from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from random import randint

class Client(DatagramProtocol):
    def __init__(self, server_host, server_port, client_host, client_port):
        self.id = client_host, client_port
        self.address = None
        self.server = server_host, server_port
        print("Working on id:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')

        if addr == self.server:
            print("Choose a client from these\n", datagram)
            input_host = input("Enter the client's IP address: ")
            input_port = int(input("Enter the client's port number: "))
            self.address = input_host, input_port
            reactor.callInThread(self.send_msg)

        print(addr, ":", datagram)

    def send_msg(self):
        while True:
            self.transport.write(input("Enter message: ").encode('utf-8'), self.address)

if __name__ == '__main__':
    input_server_host = input("Enter the server's IP address: ")
    input_server_port = int(input("Enter the server's port number: "))
    input_client_host = input("Enter your IP address: ")
    input_client_port = int(input("Enter your port number: "))
    port = randint(1000, 5000)
    reactor.listenUDP(port, Client(input_server_host, input_server_port, input_client_host, input_client_port))
    reactor.run()
