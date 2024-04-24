import asyncio
import websockets
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class WebSocketClientApp(App):
    async def start_client(self):
        async with websockets.connect("ws://localhost:8765") as websocket:
            done = False
            while not done:
                await asyncio.sleep(0.1)
                if self.key_pressed == "space":
                    await websocket.send("buzz")
                    message = await websocket.recv()
                    print(message)
                    done = True

    def on_key_down(self, keyboard, keycode, text, modifiers):
        self.key_pressed = text

    def build(self):
        self.key_pressed = None
        Window.bind(on_key_down=self.on_key_down)
        asyncio.ensure_future(self.start_client())
        return Label(text="Press space to send 'buzz' message to the WebSocket server")

if __name__ == '__main__':
    WebSocketClientApp().run()
