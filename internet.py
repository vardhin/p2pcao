from pyp2p.net import *
import threading
import time

# Function to handle receiving messages
def receive_messages(con):
    while True:
        try:
            for reply in con:
                print("\n[Friend]: " + reply)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to handle sending messages
def send_messages(con):
    while True:
        try:
            message = input("[You]: ")
            con.send_line(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            break

# Function to start the chat as a server
def start_server(passive_ip, passive_port):
    try:
        print("Starting server...")

        # Setup server's p2p node.
        server = Net(passive_bind=passive_ip, passive_port=passive_port, node_type="passive", debug=1)
        server.start()
        server.bootstrap()
        server.advertise()

        print(f"Server started successfully! Waiting for connections on {passive_ip}:{passive_port}...")

        # Event loop.
        while True:
            for con in server:
                threading.Thread(target=receive_messages, args=(con,)).start()
                threading.Thread(target=send_messages, args=(con,)).start()
            time.sleep(1)
    except Exception as e:
        print(f"Error starting server: {e}")

# Function to start the chat as a client
def start_client(passive_ip, passive_port):
    try:
        print("Starting client...")

        # Setup client's p2p node.
        client = Net(passive_bind=passive_ip, passive_port=passive_port, node_type="passive", debug=1)
        client.start()
        client.bootstrap()
        client.advertise()

        print(f"Client started successfully! Connecting to {passive_ip}:{passive_port}...")

        # Event loop.
        while True:
            for con in client:
                threading.Thread(target=receive_messages, args=(con,)).start()
                threading.Thread(target=send_messages, args=(con,)).start()
            time.sleep(1)
    except Exception as e:
        print(f"Error starting client: {e}")

# Main function
if __name__ == "__main__":
    try:
        choice = input("Enter your choice (1 for server, 2 for client): ")

        if choice == '1':
            print("\nTo start the server, you need to specify the IP address and port to listen on.")
            passive_ip = input("Enter the passive IP address of this machine: ")
            passive_port = int(input("Enter the passive port number to listen on: "))
            start_server(passive_ip, passive_port)
        elif choice == '2':
            print("\nTo start the client, you need to specify the IP address and port of the server you want to connect to.")
            passive_ip = input("Enter the passive IP address of the server: ")
            passive_port = int(input("Enter the passive port number of the server: "))
            start_client(passive_ip, passive_port)
        else:
            print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting...")
