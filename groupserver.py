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
        del connected_clients[client_id]

async def receive_messages(websocket, client_id):
    async for message in websocket:
        try:
            data = json.loads(message)
            print(f"Received message from client {client_id}: {data}")
            # Process the received JSON data
        except Exception as e:
            print(f"Error processing message from client {client_id}: {e}")
            traceback.print_exc()

async def send_messages(websocket, client_id):
    try:
        while True:
            await asyncio.sleep(10)  # Adjust this delay as needed
            # Send a dummy JSON message to keep the connection alive
            await websocket.ping()
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client {client_id} disconnected during send operation.")
    except Exception as e:
        print(f"Error sending message to client {client_id}: {e}")
        traceback.print_exc()

async def main():
    # Get the IP address of the machine on the LAN
    ip_address = socket.gethostbyname(socket.gethostname())
    async with websockets.serve(handle_client, ip_address, 8765):
        print(f"Server started at ws://{ip_address}:8765")
        await asyncio.Future()

asyncio.run(main())
