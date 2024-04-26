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
        send_task = asyncio.create_task(send_message_forever(websocket))

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
            await broadcast_message(message)  # Broadcast message to all clients
        except Exception as e:
            print(f"Error processing message from client {client_id}: {e}")
            traceback.print_exc()

async def broadcast_message(message):
    for client_id, client_websocket in connected_clients.items():
        try:
            await client_websocket.send(message)
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
                send_task = asyncio.create_task(send_message_forever(websocket))
                receive_task = asyncio.create_task(receive_message_forever(websocket))

                await asyncio.gather(send_task, receive_task)

async def send_message_forever(websocket):
    while True:
        message = input("Enter your message: ")
        if message == "/exit":
            print("Exiting...")
            break
        data = {"type": "message", "content": message}
        await send_message(websocket, data)

async def receive_message_forever(websocket):
    while True:
        response = await websocket.recv()
        print(f"Received from server: {response}")

async def send_message(websocket, message):
    await websocket.send(json.dumps(message))

asyncio.run(main())
