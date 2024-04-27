from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self):
        self.clients = set()

    def startProtocol(self):
        self.transport.getHost().host, self.transport.getHost().port
        print(f"Server started on {self.transport.getHost().host}:{self.transport.getHost().port}")

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if datagram == "ready":
            addresses = "\n".join([str(x) for x in self.clients])
            self.transport.write(addresses.encode("utf-8"), addr)
            self.clients.add(addr)

if __name__ == '__main__':
    reactor.listenUDP(0, Server())
    print("Server started")
    reactor.run()
