import asyncio
import websockets
from kivy.app import App
from kivy.uix.label import Label

# Create an empty list to store clients
clients = []

# Define a function to handle incoming messages from clients
async def handle_message(websocket, path):
    global clients
    global fastest_time
    message = await websocket.recv()
    if message == "buzz":
        response_time = asyncio.get_event_loop().time()
        clients.append([websocket, response_time])
        if len(clients) == 1:
            await websocket.send("First place!")
            fastest_time = response_time
        else:
            t = round(response_time - fastest_time, 2)
            await websocket.send(f"Response time: {t} sec slower.")

class WebSocketServerApp(App):
    async def start_server(self):
        async with websockets.serve(handle_message, "localhost", 8765):
            print('Websockets Server Started')
            await asyncio.Future()

    async def on_start(self):
        asyncio.create_task(self.start_server())

    def build(self):
        return Label(text="WebSocket server running...")

if __name__ == '__main__':
    WebSocketServerApp().run()
