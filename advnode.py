import asyncio
import websockets
import json
import traceback
import socket

connected_clients = {}

async def handle_client(websocket, path):
    try:
        client_id = id(websocket)
        connected_clients[client_id] = websocket
        print(f"Client {client_id} connected.")

        receive_task = asyncio.create_task(receive_messages(websocket, client_id))
        send_task = asyncio.create_task(send_messages(websocket, client_id))
        await asyncio.wait([receive_task, send_task], return_when=asyncio.FIRST_COMPLETED)

    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
        traceback.print_exc()
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]

async def receive_messages(websocket, client_id):
    async for message in websocket:
        try:
            data = json.loads(message)
            print(f"Received message from client {client_id}: {data}")
            if 'to' in data and 'message' in data:
                recipient_id = data['to']
                await send_message_to_client(recipient_id, data['message'])
        except Exception as e:
            print(f"Error processing message from client {client_id}: {e}")
            traceback.print_exc()

async def send_messages(websocket, client_id):
    try:
        while True:
            await asyncio.sleep(5)  # Adjust this delay as needed
            # Send a dummy JSON message to keep the connection alive
            await websocket.ping()
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected during send operation.")
    except Exception as e:
        print(f"Error sending message to client {client_id}: {e}")
        traceback.print_exc()

async def send_message_to_client(recipient_id, message):
    if recipient_id in connected_clients:
        recipient_websocket = connected_clients[recipient_id]
        try:
            await recipient_websocket.send(json.dumps({"from": "server", "message": message}))
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {recipient_id} is disconnected. Failed to send message.")
    else:
        print(f"Client {recipient_id} not found. Failed to send message.")

async def disconnect_from_client(client_id):
    if client_id in connected_clients:
        client_websocket = connected_clients[client_id]
        try:
            await client_websocket.close()
            print(f"Disconnected from client {client_id}")
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {client_id} is already disconnected.")
    else:
        print(f"Client {client_id} not found.")

async def main():
    # Get the IP address of the machine on the LAN
    ip_address = socket.gethostbyname(socket.gethostname())
    async with websockets.serve(handle_client, ip_address, 8765):
        print(f"Server started at ws://{ip_address}:8765")
        
        # Connect to another instance as client
        other_ip = input("Enter the IP address of the other device: ")
        async with websockets.connect(f"ws://{other_ip}:8765") as websocket:
            print(f"Connected to {other_ip}")
            await websocket.send(json.dumps({"to": "server", "message": "Hello from client"}))
            response = await websocket.recv()
            print(f"Received from server: {response}")

        await asyncio.Future()

asyncio.run(main())
