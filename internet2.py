#other attempt
from pyp2p.net import *
import time

# Function to handle receiving messages
def receive_messages(con):
    while True:
        for reply in con:
            print("\n[Friend]: " + reply)

# Function to handle sending messages
def send_messages(con):
    while True:
        message = input("[You]: ")
        con.send_line(message)

# Function to start the chat as a server
def start_server():
    # Get the IP address from the user
    ip_address = input("Enter your IP address: ")

    # Setup server's p2p node.
    server = Net(passive_bind=ip_address, passive_port=44444, interface="eth0", node_type="passive", debug=1)
    server.start()
    server.bootstrap()
    server.advertise()

    # Event loop.
    while 1:
        for con in server:
            receive_messages(con)
            send_messages(con)
        time.sleep(1)

# Function to start the chat as a client
def start_client():
    # Get the IP address from the user
    ip_address = input("Enter your IP address: ")

    # Setup client's p2p node.
    client = Net(passive_bind=ip_address, passive_port=44445, interface="eth0", node_type="passive", debug=1)
    client.start()
    client.bootstrap()
    client.advertise()

    # Event loop.
    while 1:
        for con in client:
            receive_messages(con)
            send_messages(con)
        time.sleep(1)

# Main function
if __name__ == "__main__":
    choice = input("Enter your choice (1 for server, 2 for client): ")

    if choice == '1':
        start_server()
    elif choice == '2':
        start_client()
    else:
        print("Invalid choice. Please try again.")
