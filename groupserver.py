import asyncio
import websockets

# create an empty list to store clients
clients = []
fastest_time = 0

# define a function to handle incoming messages from clients
async def handle_message(websocket, path):
    global clients
    global fastest_time
    print("~~~~~~~~~SafeTalkzzz~~~~~~~~~~")
    print("~~~~~~~~~ServerSide~~~~~~~~~~~")
    print("1. Lets chat")
    print("2. Exit")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    option = int(input("Select: "))
    done = False
    while not done:
        if (option == 1):
            chatting = True
            while(chatting):
                message = input("Type: ")
                if(":exit:" in message):
                    print("exitting...")
                    done = True
                    break
                await send_message(websocket, message)  # Use await here as well
                print(await recieve_message(websocket))  # Use await here
        elif (option == 2):
            done = True

async def send_message(websocket, message):
    await websocket.send(message)

async def recieve_message(websocket):
    message = await websocket.recv()
    return message

# start the websocket server
async def start_server():
    async with websockets.serve(handle_message, "localhost", 8765):
        print('Websockets Server Started')
        await asyncio.Future()

# run the server
asyncio.run(start_server())
