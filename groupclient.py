import asyncio
import websockets
import json

async def receive_messages():
    ipaddress = input("Enter IP address of the server: ")
    uri = f"ws://{ipaddress}:8765"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received message from server: {data}")

async def send_message():
    ipaddress = input("Enter IP address of the server: ")
    uri = f"ws://{ipaddress}:8765"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        while True:
            data = {"type": "message", "content": input("Enter your message: ")}
            await websocket.send(json.dumps(data))

async def main():
    receive_task = asyncio.create_task(receive_messages())
    send_task = asyncio.create_task(send_message())
    await asyncio.wait([receive_task, send_task], return_when=asyncio.FIRST_COMPLETED)

asyncio.run(main())
