# Add necessary imports at the top
import threading

# Update the Server and Client classes to handle multiple connections
class Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.conn_array = []

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            self.conn_array.append(conn)
            threading.Thread(target=self.client_handler, args=(conn,)).start()

    def client_handler(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            self.broadcast(data)

    def broadcast(self, message):
        for conn in self.conn_array:
            conn.send(message)

class Client(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            print(data.decode())

# Update the broadcast function in the main code
def placeText(text):
    writeToScreen(text, username)
    netThrow(text)

def netThrow(message):
    for conn in conn_array:
        conn.send(message.encode())
