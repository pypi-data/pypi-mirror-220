# LlamaAPI.py

import aiohttp
import asyncio
import requests
import nest_asyncio

hostname = 'https://llama-api3.fly.dev'

class LlamaAPI:
    def __init__(self, api_token):
        self.hostname = hostname
        self.api_token = api_token
        self.headers = {'Llama-API-Token': self.api_token}

        # Apply nest_asyncio to enable nested usage of asyncio's event loop
        nest_asyncio.apply()

    async def _run_stream(self, api_request_json):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.hostname}/api/chat", headers=self.headers, json=api_request_json) as resp:
                async for chunk in resp.content.iter_any():
                    yield chunk.decode('utf-8')

    def run_stream(self, api_request_json):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._run_stream(api_request_json))

    def run_simple(self, api_request_json):
        response = requests.post(f"{self.hostname}/api/chat", headers=self.headers, json=api_request_json)
        if response.status_code != 200:
            raise Exception(f"POST {response.status_code}")
        return response

    def run(self, api_request_json):
        if api_request_json.get('stream', False):
            return self.run_stream(api_request_json)
        else:
            return self.run_simple(api_request_json)
