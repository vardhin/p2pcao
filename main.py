import socket
import threading

# Function to handle receiving messages
def receive_messages(sock):
    while True:
        message = sock.recv(1024).decode("utf-8")
        print("\nOther device:", message)

# Function to handle sending messages
def send_message(sock):
    while True:
        message = input("You: ")
        sock.send(message.encode("utf-8"))

# Main function
def main():
    # Getting IP and Port
    host = input("Enter IP of other device: ")
    port = int(input("Enter port number: "))

    # Creating a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connecting to the other device
        s.connect((host, port))
        print("Connected to", host)

        # Starting a thread to receive messages
        recv_thread = threading.Thread(target=receive_messages, args=(s,))
        recv_thread.start()

        # Starting a thread to send messages
        send_thread = threading.Thread(target=send_message, args=(s,))
        send_thread.start()

    except Exception as e:
        print("Connection failed:", e)
        s.close()

if __name__ == "__main__":
    main()
 
