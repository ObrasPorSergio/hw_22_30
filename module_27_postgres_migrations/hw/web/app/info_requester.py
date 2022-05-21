import asyncio
import json
import aiohttp


async def get_api_info(request_path: str, number: int) -> list:
    data = []
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(25)) as client:
        for _ in range(number):
            async with client.get(request_path) as response:
                reply = await response.text()
                data.append(json.loads(reply))

    return data


def get_data(url: str, quantity: int) -> list:
    return asyncio.run(get_api_info(url, quantity))
