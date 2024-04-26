import asyncio
import websockets
import json
import traceback
import threading

connected_clients = {}
lock = threading.Lock()

async def handle_client(websocket, path):
    try:
        client_id = id(websocket)
        with lock:
            connected_clients[client_id] = websocket
            print(f"Client {client_id} connected.")

        receive_thread = threading.Thread(target=receive_messages, args=(websocket, client_id))
        receive_thread.start()

    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
        traceback.print_exc()
    finally:
        with lock:
            if client_id in connected_clients:
                del connected_clients[client_id]

async def receive_messages(websocket, client_id):
    try:
        while True:
            message = await websocket.recv()
            if not message:
                break
            data = json.loads(message)
            print(f"Received message from client {client_id}: {data}")
            if 'to' in data and 'message' in data:
                recipient_id = data['to']
                send_message_to_client(recipient_id, data['message'])
            else:
                broadcast_message(message, client_id)
    except Exception as e:
        print(f"Error processing message from client {client_id}: {e}")
        traceback.print_exc()

def send_message_to_client(recipient_id, message):
    with lock:
        if recipient_id in connected_clients:
            recipient_websocket = connected_clients[recipient_id]
            try:
                recipient_websocket.send(json.dumps({"from": "server", "message": message}))
            except websockets.exceptions.ConnectionClosedError:
                print(f"Client {recipient_id} is disconnected. Failed to send message.")
        else:
            print(f"Client {recipient_id} not found. Failed to send message.")

def broadcast_message(message, sender_id):
    with lock:
        for client_id, client_websocket in connected_clients.items():
            if client_id != sender_id:  # Avoid sending the message back to the sender
                try:
                    client_websocket.send(message)
                except websockets.exceptions.ConnectionClosedError:
                    print(f"Client {client_id} is disconnected. Failed to send message.")

async def main():
    ip_address = input("Enter your damn ip address: ")
    async with websockets.serve(handle_client, ip_address, 8765):
        print(f"Server started at ws://{ip_address}:8765")

        while True:
            choice = input("Do you want to connect to another instance? (yes/no): ").lower()
            if choice != 'yes':
                break
            other_ip = input("Enter the IP address of the other device: ")
            async with websockets.connect(f"ws://{other_ip}:8765") as websocket:
                print(f"Connected to {other_ip}")

                send_thread = threading.Thread(target=send_message_forever, args=(websocket,))
                send_thread.start()

                receive_thread = threading.Thread(target=receive_message_forever, args=(websocket,))
                receive_thread.start()

def send_message_forever(websocket):
    while True:
        message = input("Enter your message: ")
        if message == "/exit":
            print("Exiting...")
            break
        data = {"type": "message", "content": message}
        send_message(websocket, data)

def receive_message_forever(websocket):
    while True:
        response = await websocket.recv()
        if not response:
            break
        print(f"Received from server: {response}")

def send_message(websocket, message):
    websocket.send(json.dumps(message))

asyncio.run(main())
#final
