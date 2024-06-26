import asyncio
import argparse
import websockets
from prompt_toolkit import prompt


class P2PChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(f"ws://{self.host}:{self.port}")
            print("Connected to the chat server!")
            await self.receive_messages()
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")
        except Exception as e:
            print(f"Error: {e}")

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                print("\nFriend:", message)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed by the server.")

    async def send_message(self, message):
        await self.websocket.send(message)


async def connect_to_friend():
    host = input("Enter the server's IP address or hostname: ")
    port = input("Enter the port number (default is 8765): ") or 8765

    client = P2PChatClient(host, port)
    await client.connect()

    while True:
        try:
            message = prompt("> ")
            await client.send_message(message)
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break


async def start_server(port):
    async def chat_server(websocket, path):
        async for message in websocket:
            print("\nFriend:", message)

    try:
        server = await websockets.serve(chat_server, "localhost", port)
        print(f"Server is running on ws://localhost:{port}")
        await server.wait_closed()
    except OSError:
        print("Error: Another server is already running on this port.")


async def main():
    parser = argparse.ArgumentParser(description="P2P Chat System")
    parser.add_argument("-p", "--port", type=int, default=8765, help="Port number")
    args = parser.parse_args()

    print("Welcome to the P2P Chat System!")
    print("Choose an option:")
    print("1. Host a server")
    print("2. Connect to a server")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        await start_server(args.port)
    elif choice == "2":
        await connect_to_friend()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
