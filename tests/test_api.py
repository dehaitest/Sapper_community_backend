import asyncio
import socket
import threading
import json
import websockets

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 0
server_socket.bind((host, port))

url = "{{url}}"

server_socket.listen(5)

print("等待客户端连接...")

async def dealReceiveMessage(receiveMessage: str, url: str) -> str:
    async with websockets.connect(url) as websocket:
        while True:
            message = input()
            await websocket.send(message)
            response = await websocket.recv()
            print(f"{response}")
            if message == "exit":
                break
        await websocket.close()

def messageTranslate(message: str, clientSocket) -> None:
    try:
        # 为了契合Android客户端的接收逻辑，这里加上换行符
        replayMessage = message + "\\n"
        clientSocket.send(replayMessage.encode('utf-8'))
    except Exception as e:
        print(f"发送消息时发生错误: {str(e)}")
        clientSocket.send(b'Transfer complete')

def handle_client(clientSocket, clientAddress):
    print(f"连接来自 {clientAddress} 的客户端")
    while True:
        try:
            receiveMessage = clientSocket.recv(1024).decode('utf-8')
            if not receiveMessage:
                # 如果客户端断开连接，则退出循环
                print(f"客户端 {clientAddress[0]} 断开连接")
                break
            else:
                print(f"来自 {clientAddress[0]} 的消息: {receiveMessage}")

                replayMessage = asyncio.run(dealReceiveMessage(receiveMessage, url))
                replayMessage = replayMessage[:-len("__END_OF_RESPONSE__")]

                messageTranslate(replayMessage, clientSocket)

        except ConnectionResetError:
            # 如果连接被重置，说明客户端断开连接
            print(f"客户端 {clientAddress[0]} 断开连接")
            break

    clientSocket.close()



# 主循环，等待客户端连接
while True:
    clientSocket, clientAddress = server_socket.accept()
    # 每个客户端连接都创建一个新线程来处理
    client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
    client_thread.start()
