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
    
    # Bind the socket to a random port
    server_socket.bind(('0.0.0.0', 0))
    
    # Get the IP address and port
    host_ip = socket.gethostbyname(socket.gethostname())
    port = server_socket.getsockname()[1]
    
    # Start listening for incoming connections
    server_socket.listen()
    
    print(f"Server is listening on {host_ip}:{port}. Tell your friend to connect using this address.")

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
    # Get the IP address and port to connect
    target_ip = input("Enter your friend's IP address: ")
    target_port = int(input("Enter the port number: "))

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the friend's socket
        client_socket.connect((target_ip, target_port))
        print("Connected successfully! You can start chatting :)")
        
        # Create threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        
        # Start the threads
        receive_thread.start()
        send_thread.start()
    except:
        print("Failed to connect :(")

# Function to display the menu
def display_menu():
    print("\nMenu:")
    print("1. Listen for connections")
    print("2. Connect to a friend")
    print("3. Exit")

# Main function
if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            start_server()
        elif choice == '2':
            start_client()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
