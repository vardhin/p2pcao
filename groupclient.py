import asyncio
import websockets

# start the websocket client
async def start_client():
    async with websockets.connect("ws://localhost:8765") as websocket:
        done = False
        while not done:
            print("~~~~~~~~~SafeTalkzzz~~~~~~~~~~")
            print("~~~~~~~~~ClientSide~~~~~~~~~~~")
            print("1. Lets chat")
            print("2. Exit")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            option = int(input("Select: "))
            if option == 1:
                chatting = True
                while chatting:
                    message = input("Type: ")
                    if ":exit:" in message:
                        print("exiting...")
                        done = True
                        break
                    await send_message(websocket, message)  # Use await here
                    print(await recieve_message(websocket))  # Use await here
            elif option == 2:
                done = True

async def send_message(websocket, message):
    await websocket.send(message)
    response = await websocket.recv()
    print(response)

async def recieve_message(websocket):
    message = await websocket.recv()
    return message

# run the client
asyncio.run(start_client())
