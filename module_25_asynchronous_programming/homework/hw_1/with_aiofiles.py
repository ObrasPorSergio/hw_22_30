import asyncio
from pathlib import Path
import time

import aiohttp
import aiofiles

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await write_to_disk(result, idx)


async def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats(number):

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(number)]
        return await asyncio.gather(*tasks)


def main(number):
    res = asyncio.run(get_all_cats(number))
    print(len(res))


if __name__ == '__main__':
    start = time.time()
    main(10)
    print(f'Time for 10 with  aiofiles {time.time() - start}')

    start = time.time()
    main(50)
    print(f'Time for 50 with  aiofiles {time.time() - start}')

    start = time.time()
    main(100)
    print(f'Time for 100 with  aiofiles {time.time() - start}')