import asyncio
import websockets
import json
import traceback

connected_clients = {}

async def handle_client(websocket, path):
    try:
        client_id = id(websocket)
        connected_clients[client_id] = websocket
        print(f"Client {client_id} connected.")

        receive_task = asyncio.create_task(receive_messages(websocket, client_id))
        send_task = asyncio.create_task(send_messages(websocket, client_id))
        await asyncio.gather(receive_task, send_task)

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
            else:
                await broadcast_message(message)
        except Exception as e:
            print(f"Error processing message from client {client_id}: {e}")
            traceback.print_exc()

async def send_messages(websocket, client_id):
    try:
        while True:
            message = input("Enter your message: ")
            if message == "/exit":
                print("Exiting...")
                break
            data = {"from": client_id, "message": message}
            await broadcast_message(json.dumps(data))
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected during send operation.")
    except Exception as e:
        print(f"Error sending message from client {client_id}: {e}")
        traceback.print_exc()

async def broadcast_message(message):
    for client_id, client_websocket in connected_clients.items():
        try:
            await client_websocket.send(message)
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {client_id} is disconnected. Failed to send message.")

async def send_message_to_client(recipient_id, message):
    if recipient_id in connected_clients:
        recipient_websocket = connected_clients[recipient_id]
        try:
            await recipient_websocket.send(json.dumps({"from": "server", "message": message}))
        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {recipient_id} is disconnected. Failed to send message.")
    else:
        print(f"Client {recipient_id} not found. Failed to send message.")

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
                send_task = asyncio.create_task(send_messages(websocket, "server"))
                receive_task = asyncio.create_task(receive_messages(websocket, "server"))

                await asyncio.gather(send_task, receive_task)

asyncio.run(main())
