import socket
import threading

# Function to handle receiving messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("\n[Friend]: " + message)
        except:
            # If an error occurs, assume connection is lost
            print("Connection lost :(")
            break

# Function to handle sending messages
def send_messages(client_socket):
    while True:
        message = input("[You]: ")
        client_socket.send(message.encode())

# Function to start the chat as a server
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get the IP address from the user
    ip_address = input("Enter your IP address: ")

    # Bind the socket to a random port
    server_socket.bind((ip_address, 44444))
    
    # Start listening for incoming connections
    server_socket.listen()
    
    print(f"Server is listening on {ip_address}:44444")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Create threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        # Start the threads
        receive_thread.start()
        send_thread.start()

# Function to start the chat as a client
def start_client():
    # Get the IP address from the user
    ip_address = input("Enter your IP address: ")

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the friend's socket
        client_socket.connect((ip_address, 44444))
        print("Connected successfully! You can start chatting :)")
        
        # Create threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        
        # Start the threads
        receive_thread.start()
        send_thread.start()
    except:
        print("Failed to connect :(")

# Main function
if __name__ == "__main__":
    choice = input("Enter your choice (1 for server, 2 for client): ")

    if choice == '1':
        start_server()
    elif choice == '2':
        start_client()
    else:
        print("Invalid choice. Please try again.")
