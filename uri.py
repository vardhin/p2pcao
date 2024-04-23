import json
import Pyro4
import threading
import socket

class P2PNetwork:
    def __init__(self):
        self.your_ip = self.get_ip()
        self.your_uri = None
        self.friends = {}
        self.load_contacts()
        self.running = False

    def get_ip(self):
        return Pyro4.socketutil.getIpAddress(socket.gethostname())

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as f:
                self.friends = json.load(f)
        except FileNotFoundError:
            self.friends = {}

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump(self.friends, f)

    def show_contacts(self):
        print("Contacts:")
        for idx, alias in enumerate(self.friends, start=1):
            print(f"{idx}. {alias}")

    def show_my_uri(self):
        if self.your_uri:
            print(f"Your URI: {self.your_uri}")
        else:
            self.assign_uri()
            if self.your_uri:
                print(f"Your URI: {self.your_uri}")
            else:
                print("Failed to assign your URI.")

    def connect_to_friend(self, index):
        alias, friend_uri = list(self.friends.items())[index]
        print(f"Connecting to {alias}...")
        self.running = True
        self.start_server_thread()

    def start_server_thread(self):
        server_thread = threading.Thread(target=self.handle_incoming)
        server_thread.daemon = True
        server_thread.start()

    def handle_incoming(self):
        daemon = Pyro4.Daemon(host=self.your_ip)
        ns = Pyro4.locateNS()
        self.your_uri = daemon.register(self)
        ns.register("p2p_network", self.your_uri)
        print(f"Server started! Listening for incoming messages... My URI: {self.your_uri}")
        daemon.requestLoop()

    def add_new_friend(self, friend_uri):
        alias = input("Enter the alias for the new contact: ")
        self.friends[alias] = friend_uri
        self.save_contacts()
        return alias

    def send_message(self, alias, message):
        friend_uri = self.friends.get(alias)
        if friend_uri:
            friend = Pyro4.Proxy(friend_uri)
            friend.receive_message(self.get_ip(), message)
        else:
            print(f"Alias '{alias}' not found.")

    def stop(self):
        self.running = False

    def receive_message(self, sender_ip, message):
        alias = self.get_alias_by_ip(sender_ip)
        print(f"Received from {alias}: {message}")

    def get_alias_by_ip(self, sender_ip):
        for alias, uri in self.friends.items():
            if uri.startswith("PYRO:") and uri.split("@")[1].split(":")[0] == sender_ip:
                return alias
        return None
    
    def assign_uri(self):
        if not self.your_uri:
            print("Assigning your URI...")
            daemon = Pyro4.Daemon(host=self.your_ip)
            self.your_uri = daemon.register(self)
            print(f"URI assigned: {self.your_uri}")

p2p_network = P2PNetwork()

while True:
    print("\nAPP:")
    print("initialized...")
    print("1. Whom do you wanna text")
    print("2. Register a new contact")
    print("3. Show my URI")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("Whom do you wanna text:")
        p2p_network.show_contacts()
        index = input("Enter the serial number of the contact you want to connect to: ")
        if index.isdigit():
            index = int(index) - 1
            if 0 <= index < len(p2p_network.friends):
                p2p_network.connect_to_friend(index)
            else:
                print("Invalid serial number.")
        else:
            print("Invalid input.")
    elif choice == '2':
        friend_uri = input("Enter the Pyro4 URI of the new contact: ")
        p2p_network.add_new_friend(friend_uri)
    elif choice == '3':
        p2p_network.show_my_uri()
    elif choice == '4':
        break
    else:
        print("Invalid input.")
