import asyncio
import websockets
import json
import traceback
import socket
import concurrent.futures

connected_clients = {}
executor = concurrent.futures.ThreadPoolExecutor()

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
        loop = asyncio.get_event_loop()
        while True:
            await loop.run_in_executor(executor, asyncio.sleep, 99999)  # Adjust this delay as needed
            # Send a dummy JSON message to keep the connection alive
            await loop.run_in_executor(executor, websocket.ping)
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
    ip_address = input("Enter your damn ip address: ") 
    async with websockets.serve(handle_client, ip_address, 8765):
        print(f"Server started at ws://{ip_address}:8765")
        
        # Connect to another instance as client
        other_ip = input("Enter the IP address of the other device: ")
        async with websockets.connect(f"ws://{other_ip}:8765") as websocket:
            print(f"Connected to {other_ip}")
            send_future = asyncio.create_task(send_message_forever(websocket))
            receive_future = asyncio.create_task(receive_message_forever(websocket))

            await asyncio.wait([send_future, receive_future], return_when=asyncio.FIRST_COMPLETED)

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
