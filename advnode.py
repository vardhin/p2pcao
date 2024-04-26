import asyncio
import websockets
import json
import traceback
import concurrent.futures

connected_clients = {}
executor = concurrent.futures.ThreadPoolExecutor()

async def handle_client(websocket, path):
    try:
        client_id = id(websocket)
        connected_clients[client_id] = websocket
        print(f"Client {client_id} connected.")

        receive_task = asyncio.create_task(receive_messages(websocket, client_id))
        await asyncio.wait([receive_task], return_when=asyncio.FIRST_COMPLETED)

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
    # Get the IP address of the machine on the LAN
    ip_address = input("Enter your damn ip address: ") 
    async with websockets.serve(handle_client, ip_address, 8765):
        print(f"Server started at ws://{ip_address}:8765")
        
        await asyncio.Future()  # Just to keep the server running

asyncio.run(main())
