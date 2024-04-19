import socket
import threading

# Function to handle receiving messages
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if message:
                print("\n[Received]:", message)
        except Exception as e:
            print("Error receiving message:", e)
            break

# Function to handle sending messages
def send_messages(sock):
    while True:
        message = input("[You]: ")
        sock.send(message.encode("utf-8"))

# Main function to establish connection
def main():
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Port to listen on

    # Try to become the server
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)  # Listen for one incoming connection
        print("[Server] Waiting for incoming connection...")
        client_socket, client_address = server_socket.accept()
        print("[Server] Connected to:", client_address)
    except Exception as e:
        print("Failed to become server:", e)
        print("[Client] Trying to connect to server...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("[Client] Connected to server")

    # Create threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    # Start threads
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()
