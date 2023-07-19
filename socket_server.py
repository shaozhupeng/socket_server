import asyncio
import websockets

# 保存已连接的WebSocket客户端和对应的用户名
connected_clients = {}

async def handle_connection(websocket, path):
    try:
        print("start websockets")
        # 用户认证
        await websocket.send("Please enter your username:")
        username = await websocket.recv()
        connected_clients[username] = websocket
        print(f"{username} connected.")

        # 广播新用户加入的消息
        for client in connected_clients.values():
            await client.send(f"{username} has joined the chat.")

        while True:
            # 接收客户端消息
            message = await websocket.recv()
            
            # 广播消息给所有连接的客户端
            for client in connected_clients.values():
                await client.send(f"{username}: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        # 客户端断开连接，删除该客户端信息
        del connected_clients[username]
        print(f"{username} disconnected.")

# 启动WebSocket服务器
start_server = websockets.serve(handle_connection, "127.0.0.1", 9006)

# 运行服务器，接收连接
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
