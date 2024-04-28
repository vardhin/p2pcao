from twisted.internet import reactor, protocol
from twisted.protocols import basic

class ChatProtocol(basic.LineReceiver):
    """
    Protocol for handling communication between the server and clients.
    """

    def __init__(self, factory):
        """
        Initialize the protocol with a reference to its factory.

        Args:
            factory (ChatFactory): The factory creating this protocol instance.
        """
        self.factory = factory

    def connectionMade(self):
        """
        Called when a new client connection is established.
        Prints client and server information and adds the client to the list of connected clients.
        """
        peer = self.transport.getPeer()
        print(f"Client connected from {peer.host}:{peer.port}")
        print(f"Server running on {self.factory.server_ip}:{self.factory.server_port}")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        """
        Called when a client disconnects from the server.
        Prints a message indicating client disconnection and removes the client from the list of connected clients.
        """
        print("Client disconnected")
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        """
        Called when a line of data is received from a client.
        Prints the received message and broadcasts it to all other connected clients.
        """
        print(f"Received message: {line}")
        for client in self.factory.clients:
            if client != self:
                client.sendLine(line.encode('utf-8'))

class ChatFactory(protocol.Factory):
    """
    Factory for creating instances of the ChatProtocol class.
    """

    def __init__(self, server_ip, server_port):
        """
        Initialize the factory with an empty list of clients and server IP and port.

        Args:
            server_ip (str): The IP address of the server.
            server_port (int): The port number of the server.
        """
        self.clients = []
        self.server_ip = server_ip
        self.server_port = server_port

    def buildProtocol(self, addr):
        """
        Called when a new connection is made to the server.
        Creates and returns a new instance of the ChatProtocol class.

        Args:
            addr: The address of the connecting client.

        Returns:
            ChatProtocol: A new instance of the ChatProtocol class.
        """
        return ChatProtocol(self)

def main():
    """
    Entry point of the program.
    Starts the chat server on the specified IP address and port.
    """
    server_ip = '127.0.0.1'  # Change this to your server's IP address
    server_port = 9999
    reactor.listenTCP(server_port, ChatFactory(server_ip, server_port))
    print(f"Chat server started on {server_ip}:{server_port}")
    reactor.run()

if __name__ == "__main__":
    main()
