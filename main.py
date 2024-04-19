import socket
import threading

# Function to handle receiving messages
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if message:
                print("\nOther person:", message)
        except Exception as e:
            print("Error receiving message:", e)
            break
    print("Connection closed.")
    sock.close()

# Function to handle sending messages
def send_message(sock):
    while True:
        try:
            message = input("You: ")
            sock.send(message.encode("utf-8"))
        except Exception as e:
            print("Error sending message:", e)
            break
    print("Connection closed.")
    sock.close()

# Main function
def main():
    # Getting own IP and Port
    own_ip = input("Enter your IP address: ")
    own_port = int(input("Enter your port number: "))
    
    # Getting other person's IP and Port
    other_ip = input("Enter other person's IP address: ")
    other_port = int(input("Enter other person's port number: "))

    # Creating a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connecting to the other person
        print("Trying to connect to", other_ip, "on port", other_port)
        s.connect((other_ip, other_port))
        print("Connected to", other_ip)

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
