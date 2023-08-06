# LlamaAPI.py

import aiohttp
import asyncio

hostname = 'https://llama-api3.fly.dev'

class LlamaAPI:

    def __init__(self, api_token):
        self.hostname = hostname
        self.api_token = api_token
        self.headers = {'Llama-API-Token': self.api_token}

    async def _run(self, api_request_json):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.hostname}/api/chat", headers=self.headers, json=api_request_json) as resp:
                async for chunk in resp.content.iter_any():
                    yield chunk.decode('utf-8')

    def run(self, api_request_json):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._run(api_request_json))
