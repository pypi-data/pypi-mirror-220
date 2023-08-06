# LlamaAPI.py

import aiohttp
import asyncio
import requests
from threading import Thread
from queue import Queue

hostname = 'https://llama-api3.fly.dev'

class LlamaAPI:
    def __init__(self, api_token):
        self.hostname = hostname
        self.api_token = api_token
        self.headers = {'Llama-API-Token': self.api_token}

    async def _run_stream(self, api_request_json, queue):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.hostname}/api/chat", headers=self.headers, json=api_request_json) as resp:
                async for chunk in resp.content.iter_any():
                    queue.put(chunk.decode('utf-8'))
        queue.put(None)  # Signal the end of the iterator

    def run_stream(self, api_request_json):
        queue = Queue()

        def target():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._run_stream(api_request_json, queue))
            loop.close()

        Thread(target=target).start()
        return iter(queue.get, None)

    def run_simple(self, api_request_json):
        response = requests.post(f"{self.hostname}/api/chat", headers=self.headers, json=api_request_json)
        if response.status_code != 200:
            raise Exception(f"POST {response.status_code}")
        return response.json()  # assuming server responds with JSON

    def run(self, api_request_json):
        if api_request_json.get('stream', False):
            return self.run_stream(api_request_json)
        else:
            return self.run_simple(api_request_json)
