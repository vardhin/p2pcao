import websockets
import json
import traceback
import concurrent.futures
from collections import defaultdict
import datetime
import emoji
import threading

user_typing = defaultdict(bool)

connected_clients = {}
message_history = defaultdict(list)
executor = concurrent.futures.ThreadPoolExecutor()

def handle_client(websocket, path):
    client_id = None  # Initialize client_id to None
    try:
        client_id = id(websocket)
        connected_clients[client_id] = {"socket": websocket, "nickname": "", "status": "online"}
        print(f"Client {client_id} connected.")

        # Send message history to the newly connected client
        send_message_history(websocket)

        receive_task = executor.submit(receive_messages, websocket, client_id)
        send_task = executor.submit(send_messages, websocket, client_id)
        concurrent.futures.wait([receive_task, send_task], return_when=concurrent.futures.FIRST_COMPLETED)

    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
        traceback.print_exc()
    finally:
        if client_id in connected_clients:
            connected_clients[client_id]['status'] = "offline"

def receive_messages(websocket, client_id):
    while True:
        try:
            message = websocket.recv()
            data = json.loads(message)
            print(f"Received message from client {client_id}: {data}")
            if 'command' in data:
                handle_command(data['command'], websocket, client_id)
            elif 'message' in data:
                if 'to' in data:
                    send_private_message(data['to'], data['message'], client_id)
                else:
                    broadcast_message(client_id, data['message'])
            elif 'typing' in data:
                handle_typing(client_id)
        except Exception as e:
            print(f"Error processing message from client {client_id}: {e}")
            traceback.print_exc()

def send_messages(websocket, client_id):
    try:
        while True:
            # Send a dummy JSON message to keep the connection alive
            websocket.ping()
            # Adjust this delay as needed
            threading.sleep(99999)
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected during send operation.")
    except Exception as e:
        print(f"Error sending message to client {client_id}: {e}")
        traceback.print_exc()
    finally:
        user_typing[client_id] = False

def broadcast_message(sender_id, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {connected_clients[sender_id]['nickname']}: {message}"
    for client_id, client_info in connected_clients.items():
        if client_id != sender_id:
            try:
                client_info['socket'].send(json.dumps({"from": "server", "message": emoji.emojize(formatted_message)}))
            except websockets.exceptions.ConnectionClosedError:
                print(f"Client {client_id} is disconnected. Failed to send message.")

def send_private_message(recipient_nickname, message, sender_id):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {connected_clients[sender_id]['nickname']}: {message}"
    recipient_found = False
    for client_id, client_info in connected_clients.items():
        if client_info['nickname'] == recipient_nickname:
            try:
                client_info['socket'].send(json.dumps({"from": "server", "message": emoji.emojize(formatted_message)}))
                recipient_found = True
                break
            except websockets.exceptions.ConnectionClosedError:
                print(f"Client {client_id} is disconnected. Failed to send message.")
    if not recipient_found:
        # Inform the sender that the recipient was not found
        try:
            connected_clients[sender_id]['socket'].send(json.dumps({"from": "server", "message": "Recipient not found."}))
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {sender_id} is disconnected. Failed to inform sender.")

def handle_typing(client_id):
    user_typing[client_id] = True
    for client_id, client_info in connected_clients.items():
        try:
            client_info['socket'].send(json.dumps({"from": "server", "typing": user_typing[client_id]}))
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {client_id} is disconnected. Failed to send typing indicator.")

def handle_command(command, websocket, client_id):
    if command.startswith('/nick'):
        set_nickname(command.split(' ', 1)[1], websocket, client_id)
    elif command == '/list':
        list_connected_clients()

def set_nickname(nickname, websocket, client_id):
    connected_clients[client_id]['nickname'] = nickname
    try:
        websocket.send(json.dumps({"from": "server", "message": f"Your nickname is set to {nickname}"}))
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} is disconnected. Failed to send message.")

def list_connected_clients():
    clients = ", ".join([client_info['nickname'] for client_info in connected_clients.values() if client_info['nickname']])
    print(f"Connected clients: {clients}")

def send_message_history(websocket):
    for message in message_history.values():
        try:
            websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosedError:
            print("Client is disconnected. Failed to send message history.")

def set_status(status, client_id):
    connected_clients[client_id]['status'] = status
    print(f"Client {client_id} status changed to {status}.")

def main():
    # Get the IP address of the machine on the LAN
    ip_address = input("Enter the IP address of your device: ")
    server = websockets.serve(handle_client, ip_address, 8765)
    print(f"Server started at ws://{ip_address}:8765")

    try:
        while True:
            command = input("Enter command: ")
            if command == "/exit":
                print("Exiting...")
                server.close()  # Close the server before exiting
                break
            # Handle other commands here if needed
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt...")
        server.close()

if __name__ == "__main__":
    main()
