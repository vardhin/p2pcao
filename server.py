from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self, host):
        self.host = host
        self.clients = set()

    def startProtocol(self):
        print(f"Server started on {self.host}:{self.transport.getHost().port}")

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if datagram == "ready":
            addresses = "\n".join([str(x) for x in self.clients])
            self.transport.write(addresses.encode("utf-8"), addr)
            self.clients.add(addr)

if __name__ == '__main__':
    server_host = input("Enter the server's IP address: ")
    reactor.listenUDP(9999, Server(server_host))
    print("Server started")
    reactor.run()
