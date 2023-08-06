import asyncio
import websockets
import ssl
import uuid
import certifi
import requests

API_KEY = None
process_message = None

class Receiver:
    def _generate_unique_id():
        return str(uuid.uuid4())

    def __init__(self):
        self.websocket = None
        self.received_message = None

    async def receive_message():
        while True:
            received_message = await Receiver.websocket.recv()
            response = process_message(received_message)
            await Receiver.websocket.send(response)
        

    async def _connect_to_server(client_id=None, auto_reconnect=None):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        remote_url = 'wss://vocalhost.reiserx.com/'

        try:
            async with websockets.connect(remote_url+'ws/?client_id=' + client_id + '&api_key='+API_KEY, ssl=ssl_context) as websocket:
                print("Connected: " + client_id)
                Receiver.websocket = websocket
                await Receiver.receive_message()

        except websockets.ConnectionClosedError as e:
            print(f"Connection closed: {e.code} {e}")
            if auto_reconnect is not None:
                if e.code == 4000 or e.code == 4001 or e.code == 4002:
                    pass
                else:
                     print("Reconnecting...")
                     await asyncio.sleep(auto_reconnect)
                     await Receiver._connect_to_server(client_id=client_id, auto_reconnect=auto_reconnect)
            
    def connect(client_id=None, auto_reconnect=None):
        asyncio.run(Receiver._connect_to_server(client_id=client_id, auto_reconnect=auto_reconnect))


class Request:
    def send(message, receiver_id, timeout=60):
        receiver_id = str(receiver_id)
        url = 'https://vocalhost.reiserx.com/connect/'+ receiver_id +'/'
        
        headers = {
            'Timeout': str(timeout),
            'Authorization': API_KEY
        }
        
        response = requests.post(url, headers=headers, data=message)
        return response
    