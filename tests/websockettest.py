import asyncio
import websockets

async def websocket_client(uri, message, client_id):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)

        print(f"Client {client_id} received:")
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                print(f"\nClient {client_id} completed.\n")
                break
            else:
                print(f"{response}")
        # Explicitly close the connection
        await websocket.close()
        print(f"Client {client_id} connection closed.")

async def main():
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/require2SPLForm"
    message = "High school math tutor to help students solve math problems and provide detailed instruction."
    client_count = 1  # Number of concurrent clients

    tasks = [websocket_client(uri, message, i) for i in range(client_count)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
