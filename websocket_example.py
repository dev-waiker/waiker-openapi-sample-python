import asyncio
import websockets
import jwt
class JWTGenerator:
    def __init__(self, user_key=None, secret_key=None):
        self.user_key = user_key
        self.secret_key = secret_key
        self.algorithm = 'HS256'
        self.payload = {'userKey': f'{self.user_key}'}
    def get_auth_token(self):
        jwt_token = jwt.encode(self.payload, self.secret_key, self.algorithm)
        auth_token = f'Bearer {jwt_token}'
        return auth_token

class WaikerNewsStompClient:
    def __init__(self, ws_url, waiker_product_key, jwt_token, region_code):
        self.ws_url = ws_url
        self.waiker_product_key = waiker_product_key
        self.jwt_token = jwt_token
        self.region_code = region_code
        self.ws = None

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url, extra_headers=self.get_headers())
        print(f"Connected to WebSocket: {self.ws_url}")

        await self.send_connect_frame()
        await self.send_subscribe_frame()
        await self.receive_messages()

    def get_headers(self):
        return {
            'Waiker-Product-Key': f'{self.waiker_product_key}',
            'Authorization': f'{self.jwt_token}'
        }

    async def send_connect_frame(self):
        connect_frame = (
            "CONNECT\n"
            "accept-version:1.2\n"
            f"host:{self.ws_url}\n"
            f"Authorization:{self.jwt_token}\n"
            "\n\0"
        )
        await self.ws.send(connect_frame)
        print("Sent CONNECT frame")

    async def send_subscribe_frame(self):
        subscribe_frame = (
            "SUBSCRIBE\n"
            f"destination:/news/{self.region_code}\n"
            "id:1\n"
            "ack:auto\n"
            f"Waiker-Product-Key:{self.waiker_product_key}\n"
            f"Authorization:{self.jwt_token}\n"
            "\n\0"
        )
        await self.ws.send(subscribe_frame)
        print(f"Sent SUBSCRIBE frame to /news/{self.region_code}")

    async def receive_messages(self):
        try:
            async for message in self.ws:
                self.handle_message(message)
        except websockets.ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error: {e}")

    def handle_message(self, message):
        print(f"Received message: {message}")

async def main(user_key, secret_key, waiker_product_key):

    jwt_generator = JWTGenerator(user_key=user_key, secret_key=secret_key)
    jwt_token = jwt_generator.get_auth_token()

    ws_url = "wss://oapi.waiker.ai/v2/center-ws"
    region_code = "us"

    print(f"Connecting to {ws_url}")
    print(f'jwt_token: {jwt_token}')
    client = WaikerNewsStompClient(ws_url, waiker_product_key, jwt_token, region_code)
    await client.connect()

if __name__ == '__main__':
    user_key = "발급 받은 User Key"
    secret_key = "발급 받은 Secret Key"
    waiker_product_key = "발급 받은 Product Key"
    asyncio.run(main(user_key, secret_key, waiker_product_key))
